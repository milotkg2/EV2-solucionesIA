# Evidencia de ejecución determinista de EVA2

**Fecha de ejecución:** 3 de noviembre de 2026  
**Integrantes:** Eder Valdivia y Camilo Romero  
**Ejecución determinista:** `python scripts/verificar_eva2_sin_llm.py`
**Demostración Streamlit:** consulta real a Groq y recuperación RAG el 3 de noviembre de 2026.

La salida íntegra de la corrida determinista está guardada en [`resultado_verificacion_determinista.json`](resultado_verificacion_determinista.json). La demostración ampliada en Streamlit del 6 de noviembre está descrita en [`EJECUCION_STREAMLIT_ADICIONAL.md`](EJECUCION_STREAMLIT_ADICIONAL.md); sus capturas están en [`capturas/`](capturas/) y en el anexo del informe técnico.

## Alcance

La corrida determinista ejercita código real de tracking, planner, agente y memoria con datos simulados. Se usa una base SQLite temporal y se bloquea la llamada generativa en el caso de código inexistente. Por separado, una demostración en Streamlit volvió a ejecutar la recuperación RAG con `nomic-embed-text` local y generó una respuesta real mediante Groq (`openai/gpt-oss-120b`).

## Resultados observados

| Caso | Observación | Resultado |
|---|---|---|
| Sesión | Se guardaron dos turnos y se recuperaron el código activo `LR-2026-005317` y los dos turnos. | Correcto en SQLite temporal. |
| Código inexistente | `LR-2026-999999` produjo `envio_no_encontrado`; el contador de invocaciones al LLM permaneció en cero. | Correcto. |
| Atraso de tres días | `LR-2026-005317` produjo propuesta de compensación con estado `PENDIENTE_APROBACION` y aprobador Supervisor de Servicio al Cliente. | Correcto según regla implementada. |
| Seguimiento de gestión | La planificación posterior a la gestión pendiente indicó seguimiento y evitó otra solicitud. Tras marcarla `REGISTRADA`, indicó consultar el resultado. | Correcto. |
| Cierre y duplicados | Después de cerrar la gestión, el planner indicó no duplicar la misma acción y devolvió estado `CERRADA`. | Correcto. |
| Entrega con atraso de hasta 24 horas | `LR-2026-008477` ya estaba entregado; el plan indicó informar la entrega y no ofrecer compensación económica ni reprogramar. | Correcto. |

## Demostración Streamlit, RAG y LLM

Se consultó el envío simulado `LR-2026-005317` con la pregunta sobre la compensación que corresponde. La interfaz mostró el índice RAG disponible, configuración Groq y embeddings locales. La recuperación devolvió 8 fragmentos. Groq generó el diagnóstico en 8,34 s tras 14,17 s de recuperación; la respuesta citó siete fuentes (`F1`–`F7`), reconoció que los intentos restantes no se podían determinar con el respaldo documental y propuso un cupón de despacho gratis sujeto a aprobación humana. La fecha de operación fija de la demo era 23 de septiembre de 2026.

En una sesión nueva se consultó el código inexistente `LR-2026-999999`. El resultado fue “No encontrado”, con cero fragmentos, 0,0 s de recuperación y 0,0 s de generación; la interfaz informó que no se llamó al LLM. Esto confirma que el diagnóstico no se genera sin hechos de tracking.

| Archivo | Evidencia |
|---|---|
| [`EV2-01-generacion-groq.png`](capturas/EV2-01-generacion-groq.png) | Respuesta generada y citada por Groq. |
| [`EV2-02-fuentes-rag.png`](capturas/EV2-02-fuentes-rag.png) | Fragmentos recuperados por RAG. |
| [`EV2-03-hechos-tracking.png`](capturas/EV2-03-hechos-tracking.png) | Hechos calculados desde tracking. |
| [`EV2-04-codigo-inexistente.png`](capturas/EV2-04-codigo-inexistente.png) | Código inexistente, sin invocación al LLM. |

## Límites y evidencia pendiente

- La demo verifica una consulta generativa y el manejo de un código inexistente; no cubre todos los escenarios de `docs/escenarios_eva2.md` ni reemplaza la defensa en vivo.
- La latencia corresponde a una sola consulta y puede variar según el proveedor, la red y el estado del servicio.
- La respuesta generada se cotejó con sus fuentes visibles; la evidencia no constituye una evaluación estadística de precisión para todos los documentos y consultas.
- Las pruebas históricas de `evidencias/escenarios/` pertenecen a EVA1 y no se presentan como resultados de EVA2.

## Resultado íntegro

El script imprime un objeto JSON con las acciones y estados observados al ejecutarse. La base temporal se elimina automáticamente al terminar; la base local del proyecto no se usa.
