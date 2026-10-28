# Contratos de las herramientas

El agente de EVA2 amplía la base de LogiRuta de EVA1 con memoria, planificación y trazabilidad.

| Herramienta | Entrada | Salida | Estado |
|---|---|---|---|
| `consultar_envio` | `codigo_seguimiento: str` | Hechos calculados del envío, eventos y señal de encontrado | Disponible en EVA1: `src/tracking.py` |
| `recuperar_contexto_operativo` | `consultas_por_aspecto: dict[str, str]` | Fragmentos con texto, fuente, sección, aspecto y puntaje | Se reutiliza el recuperador híbrido de `src/retrieval.py` |
| `obtener_contexto_sesion` | `session_id: str` | Mensajes recientes y código de envío activo | Implementada en `src/memory.py`; usada por agente e interfaz |
| `guardar_turno_sesion` | `session_id: str`, `rol: str`, `contenido: str`, `codigo: str` | Identificador y confirmación del turno | Implementada en `src/memory.py`; SQLite |
| `consultar_gestiones_previas` | `codigo_seguimiento: str` | Gestiones anteriores ordenadas por fecha, con acción, estado y responsable | Implementada en `src/memory.py`; SQLite |
| `planificar_accion` | Hechos, historial y referencias recuperadas | Acción, prioridad, responsable, aprobación requerida y fuentes | Implementada en `src/planner.py`; reglas deterministas |
| `registrar_gestion` | Código, acción, responsable, estado y referencias de respaldo | Identificador y confirmación del registro | Implementada en `src/memory.py`; escritura simulada en SQLite |

## Decisiones de diseño

- Se usa SQLite, incluido en Python, para conservar turnos y gestiones. La base local se guarda en `data/memoria_eva2.sqlite3` y no se sube al repositorio.
- Streamlit conserva un `session_id` UUID en la URL; al reabrir la misma URL se pueden recuperar los últimos turnos de esa sesión.
- Las gestiones se consultarán por código de envío y guardarán fecha, acción, responsable, estado, aprobación y referencias documentales.
- Estados permitidos: `PROPUESTA`, `PENDIENTE_APROBACION`, `REGISTRADA` y `CERRADA`. La interfaz no ejecuta acciones reales.
- Si una compensación requiere aprobación, la gestión queda en `PENDIENTE_APROBACION`; solo una acción humana explícita en la interfaz puede marcarla aprobada o cerrarla sin aprobación.
- Las propuestas y gestiones abiertas se muestran en el historial y el planner propone darles seguimiento; una acción cerrada tampoco se vuelve a registrar si los hechos llevan a la misma acción. Hechos nuevos permiten una nueva evaluación.
- El planner es determinista y devuelve las reglas/fuentes asociadas. Si faltan hechos o no se recuperan fragmentos documentales, deriva el caso a revisión humana.

Estas decisiones describen la implementación actual de EVA2. Actualizar la tabla si cambian contratos o estados de herramientas.
