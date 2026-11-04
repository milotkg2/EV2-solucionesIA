"""Registra evidencia determinista de EVA2 sin consumir llamadas a un LLM.

Ejecutar desde la raíz del repositorio con:
    python scripts/verificar_eva2_sin_llm.py

Usa una base SQLite temporal y no modifica los datos persistentes del proyecto.
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

RAIZ = Path(__file__).resolve().parent.parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

import src.agent as agent
import src.memory as memory
from src.planner import planificar_accion
from src.tracking import consultar_envio


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="eva2-evidencia-") as carpeta_temporal:
        memory.DB_PATH = Path(carpeta_temporal) / "memoria.sqlite3"
        memory.inicializar_memoria()

        # La sesión conserva los turnos y el envío activo sin escribir en la BD real.
        session_id = memory.nueva_session_id()
        memory.guardar_turno_sesion(
            session_id, "user", "Consulta por LR-2026-005317", "LR-2026-005317"
        )
        memory.guardar_turno_sesion(
            session_id, "assistant", "Se revisará el atraso y la gestión pendiente.",
            "LR-2026-005317",
        )
        contexto = memory.obtener_contexto_sesion(session_id)
        assert contexto["codigo_activo"] == "LR-2026-005317"
        assert len(contexto["turnos"]) == 2

        # Código inexistente: el flujo debe finalizar antes de invocar cualquier LLM.
        llamadas_llm = 0

        def llm_prohibido(_prompt: str) -> str:
            nonlocal llamadas_llm
            llamadas_llm += 1
            raise AssertionError("El flujo de código inexistente invocó el LLM")

        original_llm = agent._llamar_llm
        agent._llamar_llm = llm_prohibido
        try:
            inexistente = agent.responder(
                "Revisa el envío LR-2026-999999", session_id=session_id
            )
        finally:
            agent._llamar_llm = original_llm
        assert inexistente.tipo == "envio_no_encontrado"
        assert llamadas_llm == 0

        # El planner determina la acción y su aprobación desde hechos del CSV.
        hechos = consultar_envio("LR-2026-005317")
        referencias_control = ["[F1] POL-COM-003 §2 (referencia de control)"]
        plan_inicial = planificar_accion(
            hechos, gestiones_previas=[], referencias_recuperadas=referencias_control
        )
        assert hechos.encontrado
        assert hechos.dias_retraso == 3
        assert plan_inicial.requiere_aprobacion
        assert plan_inicial.estado_sugerido == "PENDIENTE_APROBACION"
        assert "Supervisor de Servicio al Cliente" in plan_inicial.responsable

        gestion_id = memory.registrar_gestion(
            codigo_seguimiento=hechos.codigo_seguimiento,
            accion=plan_inicial.accion,
            responsable=plan_inicial.responsable,
            estado=plan_inicial.estado_sugerido,
            prioridad=plan_inicial.prioridad,
            requiere_aprobacion=plan_inicial.requiere_aprobacion,
            referencias=referencias_control,
        )

        plan_pendiente = planificar_accion(
            hechos,
            gestiones_previas=memory.consultar_gestiones_previas(hechos.codigo_seguimiento),
            referencias_recuperadas=referencias_control,
        )
        assert f"#{gestion_id}" in plan_pendiente.accion
        assert "no generar una segunda solicitud" in plan_pendiente.accion

        memory.actualizar_estado_gestion(gestion_id, "REGISTRADA")
        plan_registrada = planificar_accion(
            hechos,
            gestiones_previas=memory.consultar_gestiones_previas(hechos.codigo_seguimiento),
            referencias_recuperadas=referencias_control,
        )
        assert "Consultar el resultado" in plan_registrada.accion

        memory.actualizar_estado_gestion(gestion_id, "CERRADA")
        plan_cerrada = planificar_accion(
            hechos,
            gestiones_previas=memory.consultar_gestiones_previas(hechos.codigo_seguimiento),
            referencias_recuperadas=referencias_control,
        )
        assert plan_cerrada.estado_sugerido == "CERRADA"
        assert "No duplicar" in plan_cerrada.accion

        # Caso entregado dentro de 24 h: informar, sin reprogramar ni compensar.
        hechos_entregado = consultar_envio("LR-2026-008477")
        plan_entregado = planificar_accion(
            hechos_entregado,
            gestiones_previas=[],
            referencias_recuperadas=referencias_control,
        )
        assert hechos_entregado.fecha_entrega_real
        assert "No ofrecer compensación económica" in plan_entregado.accion
        assert "No proponer reintento ni compensación" not in plan_entregado.accion
        assert "reprogram" not in plan_entregado.accion.lower()

        print(json.dumps({
            "resultado": "OK",
            "sesion": {
                "turnos_recuperados": len(contexto["turnos"]),
                "envio_activo_recuperado": contexto["codigo_activo"],
            },
            "envio_inexistente": {
                "tipo": inexistente.tipo,
                "llamadas_llm": llamadas_llm,
                "respuesta": inexistente.respuesta,
            },
            "plan_3_dias": {
                "encontrado": hechos.encontrado,
                "dias_retraso": hechos.dias_retraso,
                "responsable_aprobador": plan_inicial.responsable,
                "estado_inicial": plan_inicial.estado_sugerido,
            },
            "gestion": {
                "id_temporal": gestion_id,
                "pendiente": plan_pendiente.accion,
                "registrada": plan_registrada.accion,
                "cerrada": plan_cerrada.accion,
                "estado_final": plan_cerrada.estado_sugerido,
            },
            "entrega_hasta_24h": {
                "fecha_entrega": hechos_entregado.fecha_entrega_real,
                "accion": plan_entregado.accion,
            },
            "alcance": [
                "Sin llamadas a Groq, Gemini ni generación local.",
                "SQLite fue temporal; no se alteró data/memoria_eva2.sqlite3.",
                "Las referencias suministradas al planner son referencias de control; este script no verifica recuperación RAG.",
            ],
        }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
