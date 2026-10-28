# Matriz de escenarios EVA2 — LogiRuta

**Estado:** diseñados, aún no ejecutados.  
**Fecha de diseño:** 27 de octubre de 2026.  
**Propósito:** planificar la demostración y reunir evidencia de memoria, planner y trazabilidad sin mezclar estos resultados con la línea base de EVA1.

> Los casos de abajo son criterios esperados, no resultados observados. La evidencia de EVA1 conserva su propio resumen de 7 escenarios y 34/34 verificaciones; no cuenta como ejecución de EVA2.

## Requisitos previos para la ejecución

- Usar el entorno virtual del proyecto y tener Ollama disponible con `nomic-embed-text` para la recuperación local.
- Construir el índice local con `python -m src.ingest` si todavía no existe.
- Confirmar el plan y los límites de la cuenta de Groq antes de una demostración que genere respuestas. No capturar ni compartir claves o enlaces de sesión.
- Usar la fecha operacional del proyecto (`FECHA_OPERACION=2026-09-23`) para que los tramos de atraso sean reproducibles.
- Antes de cada caso que depende de historial vacío, confirmar en la interfaz que no haya una gestión abierta previa para ese envío. No borrar la base de datos local para reiniciar un escenario.
- Guardar en cada evidencia el código consultado, hechos mostrados, plan, referencias recuperadas, estado de gestiones y resultado. Ocultar la barra de URL si contiene el `session_id`.

## Casos propuestos

| ID | Capacidad | Envío / entrada | Resultado esperado | Evidencia que guardar |
|---|---|---|---|---|
| EV2-01 | Memoria de sesión y contexto | Primero consultar `LR-2026-005271`; después preguntar “¿Y cuántos reintentos quedan?” sin repetir el código | La segunda pregunta recupera el envío activo, conserva el contexto M02 y responde con base en los dos intentos registrados y la regla de intentos. Sin compensación y sin contradicción entre la respuesta y el plan | Captura de ambas consultas; hechos del envío en la segunda; plan, prompt y referencias a SOP-OPS-014/CAT-OPS-007 |
| EV2-02 | Recuperación de sesión | Reabrir la misma URL de la sesión usada en EV2-01 en una nueva conexión del navegador | Se recuperan el mismo `session_id`, los turnos recientes y el código activo. Una sesión nueva sin el parámetro `session_id` crea una conversación distinta | Capturas de memoria antes/después de reabrir, sin mostrar la URL completa |
| EV2-03 | Control de código inexistente | Consultar `LR-2026-999999` | Indica que el envío no existe; no se llama al LLM para el diagnóstico ni se produce un plan basado en hechos inventados | Captura de respuesta y panel de hechos indicando no encontrado |
| EV2-04 | Entrega completada en hasta 24 horas | Consultar `LR-2026-008477` | Reconoce que ya fue entregado un día tarde; no propone reprogramación ni compensación económica. La Mesa de Control valida la disculpa y comunicación | Captura de fecha promesa/entrega, tramo y acción; referencia a POL-COM-003 §2 |
| EV2-05 | Tramo mayor de 24 y hasta 72 horas | Consultar `LR-2026-005317` | Reconoce tres días de atraso; propone cupón de despacho gratis para próxima compra, pendiente de aprobación del Supervisor de Servicio al Cliente | Captura de hechos, estado `PENDIENTE_APROBACION`, aprobador indicado y fuente POL-COM-003 §2 |
| EV2-06 | Tramo mayor de 72 horas y hasta 5 días | Consultar `LR-2026-007362` | Reconoce cinco días de atraso; propone reembolso del despacho más cupón, pendiente de aprobación del Jefe de Operaciones | Captura de hechos, plan, aprobador y fuente POL-COM-003 §2 |
| EV2-07 | Tramo mayor de 5 días | Consultar `LR-2026-004182` sin gestiones previas abiertas | Reconoce más de cinco días; propone escalar a Gerencia Comercial y gestionar reposición o reembolso del producto con el retailer más reembolso del despacho. No confirma el beneficio antes de aprobación | Captura de hechos, tramo `mas_de_5_dias`, prioridad, estado pendiente y referencias |
| EV2-08 | Memoria de gestiones y aprobación | En EV2-05 registrar la gestión simulada; consultar de nuevo; luego marcar aprobada desde la interfaz | La primera consulta posterior propone dar seguimiento y no duplica el cupón. Tras aprobación aparece como `REGISTRADA`; no se afirma que el cupón se haya emitido en un sistema real | Capturas antes/después de guardar y aprobar, con estados e IDs de gestión |
| EV2-09 | Cierre y nueva planificación | Cerrar la gestión registrada de EV2-08; volver a consultar el envío | La gestión queda `CERRADA`; el planner vuelve a evaluar hechos y reglas, y no permite registrar de nuevo una acción idéntica con los mismos hechos. Un cambio de hechos permite una nueva propuesta | Capturas del estado cerrado y de la acción bloqueada; si se cambian los hechos, guardar el nuevo plan |
| EV2-10 | Paquete no localizable | Consultar `LR-2026-009011` | Abre incidente simulado y escala a Operaciones; propone reposición o reembolso con el retailer más reembolso del despacho, sujeto a aprobación de Gerencia Comercial | Captura del motivo M07, acción, aprobación y referencias CAT-OPS-007 / POL-COM-003 |
| EV2-11 | Tercer intento fallido | Consultar `LR-2026-006152` | Propone devolución al origen y notificación al retailer el mismo día hábil; no propone compensación por causa M02 | Captura del número de intentos, estado del plan y referencias SOP-OPS-014 / CAT-OPS-007 |
| EV2-12 | Separación de consultas | Después de EV2-01, preguntar “¿Qué significa RRF?” sin código de envío | Resuelve la pregunta como consulta documental; no agrega el envío activo ni turnos previos no relacionados al prompt | Captura del flujo de políticas, consultas RAG y prompt enviado |

## Protocolo de registro

Para cada caso, completar esta ficha después de ejecutarlo:

```text
ID del escenario:
Fecha y persona que lo ejecutó:
Estado: Pendiente / Ejecutado / Corregido
Resultado esperado:
Resultado observado:
¿Coincidieron?:
Hechos de tracking visibles:
Plan y estado de gestión:
Referencias recuperadas:
Captura o archivo de evidencia:
Observaciones y corrección necesaria:
```

Guardar evidencias nuevas en `evidencias/eva2/`, con nombres como `EV2-01-memoria-sesion.md` y las capturas asociadas. Crear esa carpeta solo cuando empiece la ejecución; esta matriz no certifica casos todavía no corridos.

## Aspectos que deben confirmarse al ejecutar

1. Que las fuentes relevantes aparezcan en la recuperación híbrida y que las citas que entrega el LLM correspondan a los fragmentos mostrados.
2. Que el contexto de sesión no se aplique a una pregunta independiente que no sea un seguimiento.
3. Que un envío entregado nunca reciba una acción de reprogramación.
4. Que los tramos y tipos de compensación coincidan con la tabla de POL-COM-003, incluyendo los cargos que deben aprobarlos.
5. Que el historial dé seguimiento a gestiones abiertas y evite registrar otra vez una acción idéntica ya cerrada; comprobar que hechos nuevos produzcan una nueva evaluación.
6. Que el flujo de código inexistente evite la generación con LLM.

