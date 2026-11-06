# EVA2 — Agente operativo LogiRuta

**Integrantes:** Eder Valdivia y Camilo Romero  
**Asignatura:** Ingeniería de Soluciones con IA (ISY0101)

## Contexto

Este repositorio continúa el proyecto de la EVA1 para la Mesa de Control de LogiRuta SpA, operador simulado de última milla. La base consulta datos de tracking de forma determinista y recupera procedimientos, SLA, políticas y normativa mediante RAG híbrido.

La EVA2 amplía esa base con memoria de sesión, recuperación de gestiones anteriores, planificación de acciones y registro simulado con evidencia trazable.

## Estructura

- `src/`: agente, tracking, recuperación documental, memoria, planner e interfaz Streamlit.
- `data/`: datos simulados, fuentes operativas e índice vectorial local.
- `prompts/`: instrucciones de generación del agente.
- `evidencias/`: escenarios y evidencias de referencia de la EVA1; las evidencias nuevas de EVA2 están en `evidencias/eva2/`.
- `docs/alcance.md`: alcance y límites de la EVA2.
- `docs/tools.md`: contratos y decisiones de diseño de las herramientas.
- `docs/reglas.md`: reglas del planner y precedencia de políticas.
- `docs/GUIA_ESTUDIO_EVA2.md`: conceptos, arquitectura, stack y preparación de la defensa; se actualiza con el avance.
- `docs/escenarios_eva2.md`: matriz de escenarios propuestos y evidencia por recopilar.
- `evidencias/eva2/VERIFICACION_TECNICA.md`: verificaciones parciales locales y sus límites.

## Configuración segura

1. Crear un entorno virtual con Python 3.13 e instalar `requirements.txt`.
2. Copiar `.env.example` como `.env` y completar la clave de Groq localmente.
3. No subir `.env`, archivos con claves ni bases de datos locales al repositorio.
4. Ollama y `nomic-embed-text` se usan localmente para embeddings; Groq se usa para generar respuestas.

La guía de estudio incluye pasos iniciales de instalación y ejecución. Las acciones son simuladas: no se conecta ni modifica ningún sistema real de LogiRuta.

## Avance

- [x] Documentar el alcance y los límites de EVA2.
- [x] Definir el criterio de compensación: POL-COM-003 es la referencia principal.
- [x] Incorporar la base de código, datos y evidencias de EVA1.
- [x] Definir contratos y decisiones de arquitectura para memoria y planner.
- [x] Implementar memoria persistente de sesión e historial de gestiones en SQLite.
- [x] Implementar planner determinista e integrarlo en la interfaz.
- [x] Diseñar matriz de escenarios EVA2 y criterios de evidencia.
- [x] Verificar localmente tracking, planner, memoria y recuperación RAG con generación simulada.
- [x] Registrar evidencia reproducible de tracking, planner y memoria sin llamadas a LLM.
- [x] Ejecutar la aplicación, verificar RAG y generación con Groq, y documentar resultados.
- [x] Guardar capturas de consulta generada, fuentes RAG, tracking y manejo de código inexistente.
- [x] Ejecutar y documentar cinco escenarios EVA2 en Streamlit; quedan siete de doce por cubrir.
- [x] Demostrar seguimiento contextual y aprobación/registro simulados desde Streamlit.
- [ ] Reabrir la sesión en una nueva conexión y demostrar la planificación posterior a una gestión registrada.
- [ ] Completar justificaciones, conclusión y reflexiones del equipo con redacción propia.

## Material relacionado

- [Alcance EVA2](docs/alcance.md)
- [Reglas operativas](docs/reglas.md)
- [Contratos de herramientas](docs/tools.md)
- [Guía de estudio EVA2](docs/GUIA_ESTUDIO_EVA2.md)
- [Revisión de avance contra la rúbrica](docs/rubrica_eva2.md)
- [Informe técnico EVA2 y anexo de evidencias](informe/Informe_Tecnico_EVA2_LogiRuta.docx)
- [Presentación EVA2 LogiRuta (diseño actualizado, 10 minutos)](presentacion/LogiRuta%20%C2%B7%20Avance%20EVA2.pptx)
- [Guion de exposición para Camilo y Eder](presentacion/Guion_Presentacion_EVA2_Camilo_Eder.md)
- [Matriz de escenarios EVA2](docs/escenarios_eva2.md)
- [Verificación técnica parcial](evidencias/eva2/VERIFICACION_TECNICA.md)
- [Ejecución determinista EVA2](evidencias/eva2/EJECUCION_DETERMINISTA.md)
- [Ejecución adicional en Streamlit](evidencias/eva2/EJECUCION_STREAMLIT_ADICIONAL.md)
- [Capturas de la demostración Streamlit](evidencias/eva2/capturas/)
- [Resultado JSON de la verificación](evidencias/eva2/resultado_verificacion_determinista.json)
- [Documentación técnica de EVA1](docs/documentacion_tecnica_eva1.md)
