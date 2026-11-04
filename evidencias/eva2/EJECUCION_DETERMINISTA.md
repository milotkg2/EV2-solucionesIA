# Evidencia de ejecución determinista de EVA2

**Fecha de ejecución:** 3 de noviembre de 2026  
**Integrantes:** Eder Valdivia y Camilo Romero  
**Comando reproducible:** `python scripts/verificar_eva2_sin_llm.py`

La salida íntegra de la corrida está guardada en [`resultado_verificacion_determinista.json`](resultado_verificacion_determinista.json).

## Alcance

Esta evidencia ejercita código real de tracking, planner, agente y memoria con datos simulados. Se usa una base SQLite temporal y se bloquea la llamada generativa en el caso de código inexistente. No se realizaron llamadas a Groq, Gemini ni a un modelo local. Las referencias de política entregadas al planner son referencias de control; esta ejecución no verifica el recuperador RAG ni la calidad de redacción de un LLM.

## Resultados observados

| Caso | Observación | Resultado |
|---|---|---|
| Sesión | Se guardaron dos turnos y se recuperaron el código activo `LR-2026-005317` y los dos turnos. | Correcto en SQLite temporal. |
| Código inexistente | `LR-2026-999999` produjo `envio_no_encontrado`; el contador de invocaciones al LLM permaneció en cero. | Correcto. |
| Atraso de tres días | `LR-2026-005317` produjo propuesta de compensación con estado `PENDIENTE_APROBACION` y aprobador Supervisor de Servicio al Cliente. | Correcto según regla implementada. |
| Seguimiento de gestión | La planificación posterior a la gestión pendiente indicó seguimiento y evitó otra solicitud. Tras marcarla `REGISTRADA`, indicó consultar el resultado. | Correcto. |
| Cierre y duplicados | Después de cerrar la gestión, el planner indicó no duplicar la misma acción y devolvió estado `CERRADA`. | Correcto. |
| Entrega con atraso de hasta 24 horas | `LR-2026-008477` ya estaba entregado; el plan indicó informar la entrega y no ofrecer compensación económica ni reprogramar. | Correcto. |

## Límites y evidencia pendiente

- La ejecución prueba componentes desde Python; no constituye una demostración de la interfaz Streamlit.
- No prueba recuperación semántica RAG ni generación con Groq. El índice local está disponible, pero Ollama no respondió en el momento de esta ejecución.
- Faltan capturas de pantalla de la interfaz y evidencia de los restantes escenarios de la matriz EVA2.
- Las pruebas históricas de `evidencias/escenarios/` pertenecen a EVA1 y no se presentan como resultados de EVA2.

## Resultado íntegro

El script imprime un objeto JSON con las acciones y estados observados al ejecutarse. La base temporal se elimina automáticamente al terminar; la base local del proyecto no se usa.
