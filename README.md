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
- `evidencias/`: escenarios y evidencias de referencia de la EVA1; las evidencias nuevas de EVA2 se agregarán en `evidencias/eva2/`.
- `docs/alcance.md`: alcance y límites de la EVA2.
- `docs/tools.md`: contratos y decisiones de diseño de las herramientas.
- `docs/reglas.md`: reglas del planner y precedencia de políticas.
- `docs/GUIA_ESTUDIO_EVA2.md`: conceptos, arquitectura, stack y preparación de la defensa; se actualiza con el avance.
- `docs/escenarios_eva2.md`: matriz de escenarios propuestos y evidencia por recopilar.

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
- [ ] Ejecutar la aplicación, corregir lo que aparezca y documentar los resultados.
- [ ] Ejecutar escenarios EVA2 y guardar sus evidencias.

## Material relacionado

- [Alcance EVA2](docs/alcance.md)
- [Reglas operativas](docs/reglas.md)
- [Contratos de herramientas](docs/tools.md)
- [Guía de estudio EVA2](docs/GUIA_ESTUDIO_EVA2.md)
- [Matriz de escenarios EVA2](docs/escenarios_eva2.md)
- [Documentación técnica de EVA1](docs/documentacion_tecnica_eva1.md)
