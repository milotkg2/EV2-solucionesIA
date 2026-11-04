# Revisión de avance según la rúbrica EVA2

**Equipo:** Eder Valdivia y Camilo Romero  
**Asignatura:** Ingeniería de Soluciones con IA (ISY0101)  
**Revisión documental:** 3 de noviembre de 2026

## Propósito y alcance

Esta matriz contrasta la pauta oficial `RUBRICA_EVA2.docx` con el código, la documentación y las evidencias disponibles en el repositorio. Es una revisión de avance para orientar el trabajo; **no es una calificación ni reemplaza la evaluación docente**. “Implementado” significa que hay código o documentación visible; “evidencia pendiente” significa que aún falta demostrarlo con una ejecución de EVA2 o incorporarlo a la entrega final.

La línea base de siete escenarios y 34/34 verificaciones corresponde a EVA1. No se cuenta como ejecución de los escenarios de EVA2. La verificación local previa de memoria, planner y RAG usó una respuesta simulada para el LLM. La nueva evidencia del 3 de noviembre comprobó tracking, planner y estados de memoria con una base temporal; no ejecutó Streamlit ni hizo llamadas a un LLM.

## Matriz por indicador

| Indicador | Peso | Avance respaldado por el repositorio | Pendiente para cerrar el indicador | Estado documental |
|---|---:|---|---|---|
| **IE1. Herramientas dentro del agente** | 10% | Hay consulta determinista de tracking, recuperación documental, memoria SQLite, planner y registro simulado de gestiones. La nueva evidencia reprodujo planificación y escritura/actualización de una gestión con datos temporales. | Ejecutar los flujos desde Streamlit y guardar capturas de consulta, planificación, escritura y manejo de errores. | **Implementación y evidencia parcial; demostración en interfaz pendiente.** |
| **IE2. Frameworks, escalabilidad y compatibilidad** | 10% | El stack integra LlamaIndex para RAG, Streamlit para interfaz, SQLite y Groq como proveedor configurable; las dependencias están en `requirements.txt`. | Explicar y justificar por el equipo el rol de cada framework y sus límites. La orquestación del agente está implementada en Python propio; documentar cómo esa decisión satisface el requisito de framework y qué implicaría escalarla. | **Parcial; falta justificación y validación integral.** |
| **IE3. Memoria de contenido y continuidad** | 10% | `src/memory.py` conserva turnos, envío activo e historial de gestiones en SQLite. La evidencia nueva recuperó dos turnos, el envío activo y las transiciones de gestión en una base temporal. | Comprobar desde Streamlit la continuidad entre consultas y al reabrir la sesión. Guardar capturas o fichas de evidencia. | **Implementado y comprobación técnica parcial; demo pendiente.** |
| **IE4. Recuperación semántica del contexto** | 10% | La base incluye recuperación híbrida densa y BM25 para documentos. El agente reutiliza contexto reciente y envío activo; la verificación integrada confirmó que una consulta general no hereda el caso anterior. | Demostrar continuidad y separación de consultas en la aplicación. Precisar en el informe que los turnos de sesión se recuperan por recencia, mientras que la búsqueda semántica se aplica a documentos; no afirmar que existe búsqueda semántica sobre toda la memoria conversacional si no se implementa. | **Parcial; falta evidencia de interfaz y delimitar el mecanismo.** |
| **IE5. Planificación y prioridades** | 10% | `src/planner.py` prioriza reglas operativas, estado del envío, tramo de atraso e historial. La evidencia nueva cubre aprobación pendiente, seguimiento, registro, cierre, prevención de duplicados y entrega completada. | Ejecutar los mismos flujos desde la interfaz y ampliar la demostración a distintos motivos y condiciones. | **Implementación y evidencia funcional parcial; demo integral pendiente.** |
| **IE6. Informe técnico, diagramas y flujos** | 10% | Se preparó un informe técnico de cinco páginas con diagrama, componentes, flujo y evidencia registrada. Hay además documentación de alcance, reglas, contratos, guía viva y diagramas resumido y detallado. | Revisar el informe, completar justificaciones, conclusiones y reflexiones propias, y adjuntar las capturas de interfaz que faltan. | **Borrador técnico presente; autoría y evidencia final pendientes.** |
| **IE7. Demostración de decisiones adaptativas** | 10% | `docs/escenarios_eva2.md` define doce escenarios y criterios esperados. | Ejecutar los casos en vivo o registrar una demostración reproducible con varios resultados distintos. Los escenarios diseñados no equivalen a resultados demostrados. | **Pendiente de demostración EVA2.** |
| **IE8. Diagrama de orquestación y README en GitHub** | 10% | El repositorio tiene `README.md`, diagramas resumido y detallado y ahora enlaza el informe y la evidencia de EVA2. | Revisar el README como guía autónoma para una persona evaluadora: añadir enlace visible al diagrama, verificar los pasos de instalación/ejecución y scripts, y confirmar que GitHub refleja la versión final. | **Recursos presentes; falta revisión final de publicación y ejecución.** |
| **IE9. Justificación de componentes y referencias** | 10% | Hay decisiones de diseño descritas en `docs/tools.md`, `docs/reglas.md` y `arquitectura/README.md`; el borrador del informe ya incluye referencias técnicas en formato autor-fecha APA. | `docs/reglas.md` deja pendiente el fundamento técnico redactado por el equipo. Explicar la alineación entre cada componente y la necesidad operativa, validar las referencias internas y completar bibliografía si corresponde. | **Parcial; referencias incorporadas al borrador y justificación propia pendiente.** |
| **IE10. Comunicación técnica basada en evidencia** | 10% | La guía de estudio y los registros de verificación reúnen conceptos, arquitectura y ejemplos para preparar la exposición. | Preparar y ensayar exposición y preguntas. Ambos integrantes deben explicar decisiones con ejemplos ejecutados y evidencias concretas; no se puede evaluar este indicador solo con el repositorio. | **Pendiente de presentación.** |

## Pendientes prioritarios

1. **Completar evidencia de ejecución de EVA2.** Recorrer la aplicación con los escenarios representativos y anotar resultados observados; separar siempre esos resultados de la línea base de EVA1.
2. **Cerrar la demostración de memoria y gestiones.** Mostrar continuidad de sesión, seguimiento de aprobación y cierre sin duplicar acciones.
3. **Preparar el informe de hasta cinco páginas.** Incluir arquitectura, flujo, evidencia, decisiones y referencias APA. El equipo debe redactar sus propias justificaciones y conclusiones.
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
- `informe/Informe_Tecnico_EVA2_LogiRuta.docx`: borrador técnico de cinco páginas; requiere completar las secciones de autoría del equipo.
- `evidencias/escenarios/RESUMEN.md` y `evidencias/REPRODUCCION.md`: resultados de referencia de EVA1, no de EVA2.
- `RUBRICA_EVA2.docx`: instrucciones, aspectos formales e indicadores IE1–IE10.

## Actualización del estado

Actualizar esta matriz cuando se ejecute una prueba, se agregue evidencia o se prepare una sección de la entrega. Para cada caso, anotar fecha, resultado observado, diferencias respecto de lo esperado y vínculo a la evidencia correspondiente.
