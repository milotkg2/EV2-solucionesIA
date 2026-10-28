# Verificación técnica parcial — EVA2

**Fecha:** 28 de octubre de 2026  
**Alcance:** comprobaciones locales de tracking, planner, memoria y recuperación híbrida.  
**Estado:** parcial; no equivale a ejecutar los escenarios completos en Streamlit.

## Resultados observados

| Componente | Comprobación | Resultado |
|---|---|---|
| Tracking + planner | `LR-2026-008477`: entrega con un día de atraso, sin compensación económica | Correcto: `PROPUESTA` y acción de comunicación, sin reprogramación |
| Tracking + planner | `LR-2026-005317`: tres días de atraso | Correcto: cupón propuesto y aprobación del Supervisor de Servicio al Cliente |
| Tracking + planner | `LR-2026-007362`: cinco días de atraso | Correcto: reembolso de despacho más cupón, aprobación del Jefe de Operaciones |
| Tracking + planner | `LR-2026-004182`: más de cinco días | Correcto: escalamiento y beneficio sujeto a aprobación de Gerencia Comercial |
| Tracking + planner | `LR-2026-009011`: paquete no localizable (M07) | Correcto: incidente, escalamiento y compensación sujeta a aprobación |
| Tracking + planner | `LR-2026-006152`: tercer intento fallido (M02) | Correcto: devolución al origen, sin compensación |
| Tracking | Código `LR-2026-999999` | Correcto: envío no encontrado |
| SQLite | Guardar/recuperar sesión, registrar gestión y transiciones `PENDIENTE_APROBACION` → `REGISTRADA` → `CERRADA` | Correcto en una base temporal; no se dejaron datos de verificación en la base local del proyecto |
| RAG + agente | Consulta de `LR-2026-005271` y pregunta de seguimiento sin código | Correcto: se recuperó el envío activo y fragmentos del índice local de 43 fragmentos |
| Separación de contexto | Preguntar “¿Qué significa RRF?” en la misma sesión | Correcto: la consulta documental no heredó el envío ni los turnos del caso anterior |
| Código inexistente | Consulta desde el flujo del agente | Correcto: respuesta segura sin invocar la función de generación |
| Historial | Gestiones pendientes, registradas y cerradas | Correcto: seguimiento sin duplicar; la misma acción cerrada no se vuelve a registrar |

## Límites de esta verificación

- El flujo RAG integrado usó una respuesta simulada para aislar la recuperación y la lógica del agente. No valida la calidad de redacción de un LLM.
- Se inició una generación con `llama3.2:3b` local, pero se detuvo porque consumía demasiados recursos y tardaba. No se obtuvo ni se contabiliza una respuesta.
- No se realizaron consultas a Groq.
- No se recorrió la interfaz Streamlit ni se capturaron pantallas de los 12 escenarios de [`escenarios_eva2.md`](../../docs/escenarios_eva2.md).
- Por estas razones, estos resultados sirven como verificación técnica parcial y todavía no son evidencia de demostración final.

## Corrección realizada durante la verificación

La primera comprobación de SQLite encontró que las conexiones quedaban abiertas al terminar cada operación. Se actualizó `src/memory.py` para confirmar o revertir transacciones y cerrar siempre la conexión. La comprobación se repitió y finalizó correctamente.

