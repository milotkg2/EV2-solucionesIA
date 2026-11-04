# Revisión de avance según la rúbrica EVA2

**Equipo:** Eder Valdivia y Camilo Romero  
**Asignatura:** Ingeniería de Soluciones con IA (ISY0101)  
**Revisión documental:** 3 de noviembre de 2026

## Propósito y alcance

Esta matriz contrasta la pauta oficial `RUBRICA_EVA2.docx` con el código, la documentación y las evidencias disponibles en el repositorio. Es una revisión de avance para orientar el trabajo; **no es una calificación ni reemplaza la evaluación docente**. “Implementado” significa que hay código o documentación visible; “evidencia pendiente” significa que aún falta demostrarlo con una ejecución de EVA2 o incorporarlo a la entrega final.

La línea base de siete escenarios y 34/34 verificaciones corresponde a EVA1; no se cuenta como ejecución de EVA2. El 3 de noviembre de 2026 se añadieron dos evidencias de EVA2: verificación determinista de tracking, planner y memoria con una base temporal, y demostración en Streamlit con recuperación de ocho fragmentos RAG y generación real mediante Groq. También se probó que el código inexistente no invoque al LLM. Las capturas están en `evidencias/eva2/capturas/` y anexadas al informe.

## Matriz por indicador

| Indicador | Peso | Avance respaldado por el repositorio | Pendiente para cerrar el indicador | Estado documental |
|---|---:|---|---|---|
| **IE1. Herramientas dentro del agente** | 10% | Hay consulta determinista de tracking, recuperación documental, memoria SQLite, planner y registro simulado de gestiones. La demo Streamlit verificó tracking, recuperación y generación; la evidencia determinista reprodujo planificación y estados de gestión. | Completar una demostración de escritura/aprobación de gestión desde la interfaz y guardar esa captura. | **Implementación; evidencia de consulta/RAG/LLM presente; flujo de gestión en interfaz pendiente.** |
| **IE2. Frameworks, escalabilidad y compatibilidad** | 10% | El stack integra LlamaIndex para RAG, Streamlit para interfaz, SQLite y Groq como proveedor configurable; las dependencias están en `requirements.txt`. | Explicar y justificar por el equipo el rol de cada framework y sus límites. La orquestación del agente está implementada en Python propio; documentar cómo esa decisión satisface el requisito de framework y qué implicaría escalarla. | **Parcial; falta justificación y validación integral.** |
| **IE3. Memoria de contenido y continuidad** | 10% | `src/memory.py` conserva turnos, envío activo e historial de gestiones en SQLite. La verificación determinista recuperó turnos y envío activo; la demo usó sesiones aisladas para los casos observados. | Demostrar continuidad entre turnos y al reabrir la misma sesión desde Streamlit. | **Implementado y evidencia técnica; continuidad en interfaz pendiente.** |
| **IE4. Recuperación semántica del contexto** | 10% | La aplicación recuperó ocho fragmentos y los mostró en Streamlit; la respuesta usó referencias `[F1]`–`[F7]`. La búsqueda híbrida opera sobre documentos; los turnos de memoria se recuperan por recencia y envío activo. | Demostrar en la interfaz seguimiento entre varios turnos y separación de consultas generales en una misma sesión. | **RAG en interfaz verificado; memoria contextual en interfaz pendiente.** |
| **IE5. Planificación y prioridades** | 10% | `src/planner.py` prioriza reglas operativas, estado del envío, tramo de atraso e historial. La evidencia determinista cubre aprobación pendiente, seguimiento, registro, cierre, prevención de duplicados y entrega completada. | Capturar el flujo de plan, aprobación, registro y seguimiento en Streamlit; ampliar a otros motivos y condiciones. | **Implementación y evidencia funcional parcial; flujo de gestión en interfaz pendiente.** |
| **IE6. Informe técnico, diagramas y flujos** | 10% | Se preparó el informe técnico con diagrama, componentes, flujo y resultados; el anexo incorpora cuatro capturas de Streamlit (respuesta Groq, RAG, hechos y código inexistente). Hay además documentación de alcance, reglas, contratos, guía viva y diagramas resumido y detallado. | Revisar la extensión formal exigida y completar justificaciones, conclusiones y reflexiones propias. | **Informe y anexo de evidencias presentes; autoría del equipo pendiente.** |
| **IE7. Demostración de decisiones adaptativas** | 10% | `docs/escenarios_eva2.md` define doce escenarios. La demo en interfaz muestra diagnóstico de atraso/compensación y rechazo seguro de un código inexistente. | Completar en vivo o registrar más escenarios adaptativos, incluido el flujo de gestión y varios estados/motivos. Los dos casos demostrados no equivalen a cubrir la matriz completa. | **Demostración parcial; falta amplitud de escenarios.** |
| **IE8. Diagrama de orquestación y README en GitHub** | 10% | El repositorio tiene `README.md`, diagramas resumido y detallado y ahora enlaza el informe y la evidencia de EVA2. | Revisar el README como guía autónoma para una persona evaluadora: añadir enlace visible al diagrama, verificar los pasos de instalación/ejecución y scripts, y confirmar que GitHub refleja la versión final. | **Recursos presentes; falta revisión final de publicación y ejecución.** |
| **IE9. Justificación de componentes y referencias** | 10% | Hay decisiones de diseño descritas en `docs/tools.md`, `docs/reglas.md` y `arquitectura/README.md`; el borrador del informe ya incluye referencias técnicas en formato autor-fecha APA. | `docs/reglas.md` deja pendiente el fundamento técnico redactado por el equipo. Explicar la alineación entre cada componente y la necesidad operativa, validar las referencias internas y completar bibliografía si corresponde. | **Parcial; referencias incorporadas al borrador y justificación propia pendiente.** |
| **IE10. Comunicación técnica basada en evidencia** | 10% | La guía de estudio y los registros de verificación reúnen conceptos, arquitectura y ejemplos para preparar la exposición. | Preparar y ensayar exposición y preguntas. Ambos integrantes deben explicar decisiones con ejemplos ejecutados y evidencias concretas; no se puede evaluar este indicador solo con el repositorio. | **Pendiente de presentación.** |

## Pendientes prioritarios

1. **Completar evidencia de ejecución de EVA2.** Ya se verificaron una consulta RAG/LLM y el rechazo de un código inexistente. Falta recorrer más escenarios de `docs/escenarios_eva2.md` y conservar separados los resultados EVA1.
2. **Cerrar la demostración de memoria y gestiones.** Mostrar desde Streamlit continuidad de sesión, seguimiento de aprobación y cierre sin duplicar acciones.
3. **Revisar el informe y su anexo.** El cuerpo técnico y las capturas están incorporados; revisar la extensión solicitada y completar justificaciones, conclusiones y reflexiones según pauta. El equipo redacta sus propias justificaciones y reflexiones.
4. **Preparar la presentación de 20 minutos.** Distribuir participación entre Eder y Camilo y ensayar preguntas usando resultados comprobables.
5. **Declarar el uso de IA.** La pauta requiere indicar qué herramientas se usaron y cómo. Cada integrante debe escribir sin apoyo de IA su reflexión personal y las conclusiones que le correspondan.
6. **Revisar la entrega en GitHub.** Verificar README, diagramas, instrucciones de ejecución, scripts y evidencias, sin incluir `.env`, claves ni bases de datos locales.

## Evidencias consideradas

- `README.md`: alcance, estructura y avance general del proyecto.
- `docs/alcance.md`, `docs/tools.md` y `docs/reglas.md`: objetivos, contratos y reglas operativas.
- `arquitectura/README.md` y `arquitectura/diagrama_arquitectura.*`: explicación y diagramas.
- `docs/GUIA_ESTUDIO_EVA2.md`: guía de conceptos y preparación.
- `docs/escenarios_eva2.md`: escenarios propuestos, todavía no ejecutados según el propio documento.
- `evidencias/eva2/VERIFICACION_TECNICA.md`: verificaciones parciales locales y sus límites.
- `scripts/verificar_eva2_sin_llm.py` y `evidencias/eva2/EJECUCION_DETERMINISTA.md`: comprobaciones reproducibles de tracking, planner y memoria del 3 de noviembre.
- `evidencias/eva2/capturas/` y anexo del informe: demostración Streamlit, respuesta real de Groq, fragmentos RAG, hechos de tracking y código inexistente.
- `informe/Informe_Tecnico_EVA2_LogiRuta.docx`: borrador técnico de cinco páginas; requiere completar las secciones de autoría del equipo.
- `evidencias/escenarios/RESUMEN.md` y `evidencias/REPRODUCCION.md`: resultados de referencia de EVA1, no de EVA2.
- `RUBRICA_EVA2.docx`: instrucciones, aspectos formales e indicadores IE1–IE10.

## Actualización del estado

Actualizar esta matriz cuando se ejecute una prueba, se agregue evidencia o se prepare una sección de la entrega. Para cada caso, anotar fecha, resultado observado, diferencias respecto de lo esperado y vínculo a la evidencia correspondiente.
