"""Planner determinista de acciones operativas para la Mesa de Control."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from src.memory import consultar_gestiones_previas
from src.tracking import HechosEnvio


@dataclass
class PlanAccion:
    codigo_seguimiento: str
    accion: str
    prioridad: str
    responsable: str
    estado_sugerido: str
    requiere_aprobacion: bool
    revision_humana: bool
    motivo: str
    referencias_regla: list[str] = field(default_factory=list)
    referencias_recuperadas: list[str] = field(default_factory=list)
    gestiones_previas: list[dict[str, Any]] = field(default_factory=list)

    def a_dict(self) -> dict[str, Any]:
        return asdict(self)


def planificar_accion(
    hechos: HechosEnvio,
    gestiones_previas: list[dict[str, Any]] | None = None,
    referencias_recuperadas: list[str] | None = None,
) -> PlanAccion:
    """Elige una acción por reglas verificables; el LLM no participa en la decisión."""
    if not hechos.encontrado:
        return PlanAccion(
            codigo_seguimiento=hechos.codigo_seguimiento,
            accion="Verificar el código de seguimiento con el cliente o el retailer.",
            prioridad="media",
            responsable="Mesa de Control",
            estado_sugerido="PROPUESTA",
            requiere_aprobacion=False,
            revision_humana=True,
            motivo="No hay un envío verificado en el tracking.",
        )

    historial = gestiones_previas
    if historial is None:
        historial = consultar_gestiones_previas(hechos.codigo_seguimiento)
    fuentes = list(dict.fromkeys(referencias_recuperadas or []))

    def crear(
        accion: str,
        prioridad: str,
        responsable: str,
        motivo: str,
        reglas: list[str],
        requiere_aprobacion: bool = False,
        revision_humana: bool = False,
    ) -> PlanAccion:
        if not fuentes:
            return PlanAccion(
                codigo_seguimiento=hechos.codigo_seguimiento,
                accion="Solicitar revisión humana antes de registrar o ejecutar una acción; "
                "no se recuperaron fragmentos documentales para respaldar la propuesta.",
                prioridad="alta",
                responsable="Mesa de Control",
                estado_sugerido="PROPUESTA",
                requiere_aprobacion=False,
                revision_humana=True,
                motivo=f"Regla candidata: {motivo}. Falta evidencia recuperada.",
                referencias_regla=reglas,
                gestiones_previas=historial,
            )
        gestion_cerrada = next(
            (
                gestion
                for gestion in historial
                if gestion.get("estado") == "CERRADA" and gestion.get("accion") == accion
            ),
            None,
        )
        if gestion_cerrada:
            return PlanAccion(
                codigo_seguimiento=hechos.codigo_seguimiento,
                accion=(
                    f"No duplicar la acción de la gestión cerrada #{gestion_cerrada['id']}. "
                    "Revisar si existen hechos nuevos antes de abrir otra gestión."
                ),
                prioridad="baja",
                responsable="Mesa de Control",
                estado_sugerido="CERRADA",
                requiere_aprobacion=False,
                revision_humana=True,
                motivo="El historial ya contiene esta misma acción en estado cerrado.",
                referencias_regla=reglas,
                referencias_recuperadas=fuentes,
                gestiones_previas=historial,
            )
        estado = "PENDIENTE_APROBACION" if requiere_aprobacion else "PROPUESTA"
        return PlanAccion(
            codigo_seguimiento=hechos.codigo_seguimiento,
            accion=accion,
            prioridad=prioridad,
            responsable=responsable,
            estado_sugerido=estado,
            requiere_aprobacion=requiere_aprobacion,
            revision_humana=revision_humana,
            motivo=motivo,
            referencias_regla=reglas,
            referencias_recuperadas=fuentes,
            gestiones_previas=historial,
        )

    solicitudes_pendientes = [
        gestion for gestion in historial if gestion.get("estado") == "PENDIENTE_APROBACION"
    ]
    if solicitudes_pendientes:
        ultima = solicitudes_pendientes[0]
        return crear(
            f"Dar seguimiento a la aprobación pendiente de la gestión #{ultima['id']}; "
            "no generar una segunda solicitud de compensación.",
            "alta",
            "Mesa de Control",
            "El historial muestra una gestión que todavía espera aprobación humana.",
            ["POL-COM-003 §2", f"Gestión previa #{ultima['id']} · PENDIENTE_APROBACION"],
            revision_humana=True,
        )

    propuestas_abiertas = [gestion for gestion in historial if gestion.get("estado") == "PROPUESTA"]
    if propuestas_abiertas:
        ultima = propuestas_abiertas[0]
        return crear(
            f"Revisar el avance de la gestión propuesta #{ultima['id']} antes de registrar "
            "otra acción para el mismo envío.",
            "media",
            str(ultima.get("responsable") or "Mesa de Control"),
            "El historial muestra una propuesta todavía abierta.",
            [f"Gestión previa #{ultima['id']} · PROPUESTA"],
            revision_humana=True,
        )

    gestiones_activas = [gestion for gestion in historial if gestion.get("estado") == "REGISTRADA"]
    if gestiones_activas:
        ultima = gestiones_activas[0]
        return crear(
            f"Consultar el resultado de la gestión registrada #{ultima['id']} y actualizar "
            "su estado antes de proponer una acción duplicada.",
            "alta",
            str(ultima.get("responsable") or "Mesa de Control"),
            "El historial indica que ya existe una gestión registrada sin cierre.",
            [f"Gestión previa #{ultima['id']} · REGISTRADA"],
            revision_humana=True,
        )

    motivo = hechos.motivo_falla or ""
    if motivo == "M07":
        observacion = (hechos.observacion or "").lower()
        no_localizable = any(
            clave in observacion for clave in ("no localizable", "perdido", "sin movimiento")
        )
        if not no_localizable:
            return crear(
                "Abrir un incidente simulado y escalarlo a Operaciones. Confirmar si el daño "
                "o pérdida está acreditado antes de proponer una compensación.",
                "alta",
                "Operaciones",
                "El motivo M07 requiere investigación; la observación no confirma que el "
                "paquete esté perdido o no localizable.",
                ["CAT-OPS-007 M07", "POL-COM-003 §§3–4"],
                revision_humana=True,
            )
        return crear(
            "Abrir un incidente simulado y escalarlo a Operaciones. Por paquete no "
            "localizable, proponer reposición o reembolso del producto con el retailer, "
            "más reembolso del despacho; requiere aprobación de Gerencia Comercial.",
            "urgente",
            "Operaciones",
            "El catálogo clasifica el paquete como perdido o dañado; POL-COM-003 §2 define "
            "la compensación para un paquete no localizable.",
            ["CAT-OPS-007 M07", "POL-COM-003 §§2–4"],
            requiere_aprobacion=True,
            revision_humana=True,
        )

    if hechos.fecha_entrega_real and motivo in {"M02", "M03", "M05"}:
        return crear(
            "Informar que el envío ya fue entregado y explicar el motivo registrado. "
            "No proponer reintento ni compensación.",
            "media",
            "Mesa de Control",
            "El tracking confirma entrega y la causa es atribuible al consumidor o retailer.",
            ["CAT-OPS-007", "POL-COM-003 §1–2"],
        )

    if hechos.fecha_entrega_real and motivo == "M06":
        return crear(
            "Informar la entrega realizada y solicitar revisión humana de cualquier "
            "excepción de compensación por zona de riesgo o acceso restringido.",
            "media",
            "Mesa de Control",
            "El tracking confirma entrega; la excepción M06 requiere revisión manual.",
            ["CAT-OPS-007 M06", "POL-COM-003 §1–2"],
            revision_humana=True,
        )

    if hechos.fecha_entrega_real and not hechos.hay_retraso_confirmado:
        return crear(
            "Cerrar el análisis como entrega realizada dentro de la fecha promesa.",
            "baja",
            "Mesa de Control",
            "El tracking confirma que la entrega se realizó sin retraso.",
            ["SOP-OPS-014 §5", "POL-COM-003 §2"],
        )

    if hechos.intentos_entrega >= 3:
        return crear(
            "Proponer devolución al origen y notificar al retailer el mismo día hábil.",
            "alta",
            "Mesa de Control",
            "Se alcanzaron tres o más intentos fallidos.",
            ["SOP-OPS-014 §6"],
        )

    if motivo == "M03":
        return crear(
            "Contactar para validar la dirección; si no hay respuesta en 48 horas, "
            "proponer devolución al origen.",
            "media",
            "Mesa de Control",
            "La dirección figura incompleta o errónea; no corresponde compensación.",
            ["SOP-OPS-014 §6", "CAT-OPS-007 M03", "POL-COM-003 §2"],
        )
    if motivo == "M02":
        return crear(
            "Coordinar el siguiente intento dentro de 24 a 48 horas hábiles, hasta el "
            "máximo permitido; no ofrecer compensación.",
            "media",
            "Planificación",
            "El motivo registrado es cliente ausente.",
            ["SOP-OPS-014 §4", "CAT-OPS-007 M02", "POL-COM-003 §2"],
        )
    if motivo == "M05":
        return crear(
            "No reprogramar y proponer devolución al origen; no ofrecer compensación.",
            "media",
            "Mesa de Control",
            "El consumidor rechazó el envío.",
            ["SOP-OPS-014 §4", "CAT-OPS-007 M05", "POL-COM-003 §2"],
        )
    if motivo == "M06":
        return crear(
            "Proponer hasta dos intentos en horario diurno y dejar cualquier excepción "
            "de compensación para revisión humana.",
            "media",
            "Planificación",
            "La zona presenta riesgo o acceso restringido.",
            ["SOP-OPS-014 §4", "CAT-OPS-007 M06", "POL-COM-003 §2"],
            revision_humana=True,
        )

    if not hechos.hay_retraso_confirmado:
        return crear(
            "Mantener seguimiento y revisar nuevamente si aparece un evento o retraso.",
            "baja",
            "Mesa de Control",
            "El tracking no confirma un retraso.",
            ["SOP-OPS-014 §5", "SLA-COM-002"],
        )

    if hechos.computa_sla is not True or hechos.responsable != "LogiRuta":
        return crear(
            "Revisar la atribución y los antecedentes antes de proponer una medida por SLA.",
            "media",
            "Mesa de Control",
            "El atraso no está confirmado como responsabilidad computable de LogiRuta.",
            ["CAT-OPS-007", "SLA-COM-002"],
            revision_humana=True,
        )

    dias = hechos.dias_retraso or 0
    entregado = bool(hechos.fecha_entrega_real)
    if dias <= 1:
        accion = (
            "Informar la entrega realizada, reconocer el retraso y registrar una disculpa "
            "formal. No ofrecer compensación económica."
            if entregado
            else "Proponer reprogramación al siguiente día hábil e informar la nueva fecha "
            "solo cuando Planificación la confirme. No ofrecer compensación económica."
        )
        return crear(
            accion,
            "media",
            "Mesa de Control" if entregado else "Planificación",
            "El retraso atribuible a LogiRuta es de hasta 24 horas.",
            ["POL-COM-003 §2", "SOP-OPS-014 §6 y §8"],
            revision_humana=True,
        )
    if dias <= 3:
        accion = (
            "Informar que el envío ya fue entregado y proponer un cupón de despacho gratis "
            "para la próxima compra en el retailer, sujeto a aprobación del Supervisor de "
            "Servicio al Cliente."
            if entregado
            else "Priorizar la reprogramación, informar al retailer y proponer un cupón de "
            "despacho gratis para la próxima compra, sujeto a aprobación del Supervisor de "
            "Servicio al Cliente."
        )
        return crear(
            accion,
            "alta",
            "Supervisor de Servicio al Cliente",
            "El retraso atribuible a LogiRuta supera 24 y no excede 72 horas.",
            ["POL-COM-003 §2", "SOP-OPS-014 §§6–7", "SLA-COM-002 §4"],
            requiere_aprobacion=True,
        )
    if dias <= 5:
        accion = (
            "Informar que el envío ya fue entregado y proponer el reembolso del despacho "
            "más un cupón de despacho gratis, sujeto a aprobación del Jefe de Operaciones."
            if entregado
            else "Escalar a Operaciones, priorizar la reprogramación e informar al retailer. "
            "Proponer el reembolso del despacho más un cupón de despacho gratis, sujeto a "
            "aprobación del Jefe de Operaciones."
        )
        return crear(
            accion,
            "urgente",
            "Jefe de Operaciones",
            "El retraso atribuible a LogiRuta supera 72 horas y no excede cinco días.",
            ["POL-COM-003 §2", "SOP-OPS-014 §7", "SLA-COM-002 §4"],
            requiere_aprobacion=True,
        )

    return crear(
        "Escalar a Gerencia Comercial y proponer reposición o reembolso del producto con "
        "el retailer, más reembolso del despacho, sujeto a aprobación. No confirmar el "
        "beneficio antes de la decisión humana.",
        "urgente",
        "Gerencia Comercial",
        "El retraso atribuible a LogiRuta supera cinco días.",
        ["POL-COM-003 §2 y §4", "SOP-OPS-014 §7", "SLA-COM-002 §4"],
        requiere_aprobacion=True,
    )
