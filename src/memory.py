"""Memoria local persistente para sesiones y gestiones simuladas de EVA2."""

from __future__ import annotations

import json
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "memoria_eva2.sqlite3"
ESTADOS_GESTION = {
    "PROPUESTA",
    "PENDIENTE_APROBACION",
    "REGISTRADA",
    "CERRADA",
}


def _ahora() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _conectar() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conexion = sqlite3.connect(DB_PATH, timeout=10)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def inicializar_memoria() -> None:
    """Crea el esquema local si aún no existe."""
    with _conectar() as conexion:
        conexion.executescript(
            """
            CREATE TABLE IF NOT EXISTS sesiones (
                session_id TEXT PRIMARY KEY,
                codigo_activo TEXT,
                actualizada_en TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS turnos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL REFERENCES sesiones(session_id),
                rol TEXT NOT NULL CHECK (rol IN ('user', 'assistant')),
                contenido TEXT NOT NULL,
                codigo_seguimiento TEXT,
                creado_en TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_turnos_sesion_fecha
                ON turnos(session_id, id DESC);
            CREATE TABLE IF NOT EXISTS gestiones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo_seguimiento TEXT NOT NULL,
                accion TEXT NOT NULL,
                responsable TEXT NOT NULL,
                prioridad TEXT NOT NULL,
                estado TEXT NOT NULL,
                requiere_aprobacion INTEGER NOT NULL DEFAULT 0,
                referencias_json TEXT NOT NULL DEFAULT '[]',
                creada_en TEXT NOT NULL,
                actualizada_en TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_gestiones_codigo_fecha
                ON gestiones(codigo_seguimiento, id DESC);
            """
        )


def nueva_session_id() -> str:
    """Genera un identificador opaco para una sesión de interfaz."""
    return str(uuid.uuid4())


def guardar_turno_sesion(
    session_id: str,
    rol: str,
    contenido: str,
    codigo: str | None = None,
) -> int:
    """Guarda un turno y actualiza el envío activo cuando se entrega su código."""
    rol = (rol or "").strip().lower()
    if rol not in {"user", "assistant"}:
        raise ValueError("El rol debe ser 'user' o 'assistant'.")
    if not session_id or not contenido.strip():
        raise ValueError("La sesión y el contenido del turno son obligatorios.")

    inicializar_memoria()
    ahora = _ahora()
    with _conectar() as conexion:
        conexion.execute(
            """INSERT INTO sesiones(session_id, codigo_activo, actualizada_en)
               VALUES (?, ?, ?)
               ON CONFLICT(session_id) DO UPDATE SET
                   codigo_activo = COALESCE(excluded.codigo_activo, sesiones.codigo_activo),
                   actualizada_en = excluded.actualizada_en""",
            (session_id, codigo.upper() if codigo else None, ahora),
        )
        cursor = conexion.execute(
            """INSERT INTO turnos(session_id, rol, contenido, codigo_seguimiento, creado_en)
               VALUES (?, ?, ?, ?, ?)""",
            (session_id, rol, contenido.strip(), codigo.upper() if codigo else None, ahora),
        )
        return int(cursor.lastrowid)


def obtener_contexto_sesion(session_id: str, limite: int = 8) -> dict[str, Any]:
    """Recupera código activo y turnos recientes en orden cronológico."""
    inicializar_memoria()
    limite = max(1, min(int(limite), 30))
    with _conectar() as conexion:
        sesion = conexion.execute(
            "SELECT codigo_activo FROM sesiones WHERE session_id = ?", (session_id,)
        ).fetchone()
        filas = conexion.execute(
            """SELECT rol, contenido, codigo_seguimiento, creado_en
               FROM turnos WHERE session_id = ? ORDER BY id DESC LIMIT ?""",
            (session_id, limite),
        ).fetchall()
    return {
        "session_id": session_id,
        "codigo_activo": sesion["codigo_activo"] if sesion else None,
        "turnos": [dict(fila) for fila in reversed(filas)],
    }


def consultar_gestiones_previas(codigo_seguimiento: str, limite: int = 20) -> list[dict[str, Any]]:
    """Lista las gestiones más recientes de un envío."""
    inicializar_memoria()
    codigo = (codigo_seguimiento or "").strip().upper()
    if not codigo:
        return []
    limite = max(1, min(int(limite), 100))
    with _conectar() as conexion:
        filas = conexion.execute(
            """SELECT id, codigo_seguimiento, accion, responsable, prioridad, estado,
                      requiere_aprobacion, referencias_json, creada_en, actualizada_en
               FROM gestiones WHERE codigo_seguimiento = ? ORDER BY id DESC LIMIT ?""",
            (codigo, limite),
        ).fetchall()
    resultados = []
    for fila in filas:
        gestion = dict(fila)
        gestion["requiere_aprobacion"] = bool(gestion["requiere_aprobacion"])
        gestion["referencias"] = json.loads(gestion.pop("referencias_json"))
        resultados.append(gestion)
    return resultados


def registrar_gestion(
    codigo_seguimiento: str,
    accion: str,
    responsable: str,
    estado: str,
    referencias: list[str] | None = None,
    prioridad: str = "media",
    requiere_aprobacion: bool = False,
) -> int:
    """Registra una gestión simulada, nunca ejecuta la acción en sistemas externos."""
    codigo = (codigo_seguimiento or "").strip().upper()
    estado = (estado or "").strip().upper()
    if not codigo or not accion.strip() or not responsable.strip():
        raise ValueError("Código, acción y responsable son obligatorios.")
    if estado not in ESTADOS_GESTION:
        raise ValueError(f"Estado inválido. Usa uno de: {', '.join(sorted(ESTADOS_GESTION))}.")
    if requiere_aprobacion and estado not in {"PENDIENTE_APROBACION", "PROPUESTA"}:
        raise ValueError("Una acción que requiere aprobación debe quedar pendiente o propuesta.")

    inicializar_memoria()
    ahora = _ahora()
    with _conectar() as conexion:
        cursor = conexion.execute(
            """INSERT INTO gestiones(
                   codigo_seguimiento, accion, responsable, prioridad, estado,
                   requiere_aprobacion, referencias_json, creada_en, actualizada_en
               ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                codigo,
                accion.strip(),
                responsable.strip(),
                (prioridad or "media").strip().lower(),
                estado,
                int(requiere_aprobacion),
                json.dumps(referencias or [], ensure_ascii=False),
                ahora,
                ahora,
            ),
        )
        return int(cursor.lastrowid)


def actualizar_estado_gestion(gestion_id: int, estado: str) -> None:
    """Actualiza una gestión tras una decisión humana registrada en la interfaz."""
    estado = (estado or "").strip().upper()
    if estado not in ESTADOS_GESTION:
        raise ValueError(f"Estado inválido. Usa uno de: {', '.join(sorted(ESTADOS_GESTION))}.")
    inicializar_memoria()
    with _conectar() as conexion:
        actual = conexion.execute(
            "SELECT estado FROM gestiones WHERE id = ?", (int(gestion_id),)
        ).fetchone()
        if actual is None:
            raise ValueError(f"No existe la gestión #{gestion_id}.")
        estado_actual = actual["estado"]
        transiciones = {
            "PROPUESTA": {"REGISTRADA", "CERRADA"},
            "PENDIENTE_APROBACION": {"REGISTRADA", "CERRADA"},
            "REGISTRADA": {"CERRADA"},
            "CERRADA": set(),
        }
        if estado != estado_actual and estado not in transiciones[estado_actual]:
            raise ValueError(f"Transición no permitida: {estado_actual} → {estado}.")
        conexion.execute(
            "UPDATE gestiones SET estado = ?, actualizada_en = ? WHERE id = ?",
            (estado, _ahora(), int(gestion_id)),
        )
