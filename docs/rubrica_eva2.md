# Revisión de avance según la rúbrica EVA2

**Equipo:** Eder Valdivia y Camilo Romero  
**Asignatura:** Ingeniería de Soluciones con IA (ISY0101)  
**Revisión documental:** 2 de noviembre de 2026

## Propósito y alcance

Esta matriz contrasta la pauta oficial `RUBRICA_EVA2.docx` con el código, la documentación y las evidencias disponibles en el repositorio. Es una revisión de avance para orientar el trabajo; **no es una calificación ni reemplaza la evaluación docente**. “Implementado” significa que hay código o documentación visible; “evidencia pendiente” significa que aún falta demostrarlo con una ejecución de EVA2 o incorporarlo a la entrega final.

La línea base de siete escenarios y 34/34 verificaciones corresponde a EVA1. No se cuenta como ejecución de los escenarios de EVA2. La verificación local de memoria, planner y RAG está descrita como parcial y usó una respuesta simulada para el LLM.

## Matriz por indicador

| Indicador | Peso | Avance respaldado por el repositorio | Pendiente para cerrar el indicador | Estado documental |
|---|---:|---|---|---|
| **IE1. Herramientas dentro del agente** | 10% | Hay consulta determinista de tracking, recuperación documental, memoria SQLite, planner y registro simulado de gestiones. Los contratos están descritos en `docs/tools.md`. | Ejecutar los flujos desde Streamlit y guardar evidencia de consulta, planificación y escritura de una gestión. Confirmar en pantalla las transiciones y el manejo de errores. | **Implementación presente; demostración EVA2 pendiente.** |
| **IE2. Frameworks, escalabilidad y compatibilidad** | 10% | El stack integra LlamaIndex para RAG, Streamlit para interfaz, SQLite y Groq como proveedor configurable; las dependencias están en `requirements.txt`. | Explicar y justificar por el equipo el rol de cada framework y sus límites. La orquestación del agente está implementada en Python propio; documentar cómo esa decisión satisface el requisito de framework y qué implicaría escalarla. | **Parcial; falta justificación y validación integral.** |
| **IE3. Memoria de contenido y continuidad** | 10% | `src/memory.py` conserva turnos, envío activo e historial de gestiones en SQLite. Se comprobó localmente guardar/recuperar sesión y avanzar estados de gestión. | Ejecutar en la interfaz una consulta seguida de una pregunta sin código; reabrir la sesión y comprobar que se recuperan turnos y envío activo. Guardar capturas o fichas de evidencia. | **Implementado y comprobación técnica parcial; demo pendiente.** |
| **IE4. Recuperación semántica del contexto** | 10% | La base incluye recuperación híbrida densa y BM25 para documentos. El agente reutiliza contexto reciente y envío activo; la verificación integrada confirmó que una consulta general no hereda el caso anterior. | Demostrar continuidad y separación de consultas en la aplicación. Precisar en el informe que los turnos de sesión se recuperan por recencia, mientras que la búsqueda semántica se aplica a documentos; no afirmar que existe búsqueda semántica sobre toda la memoria conversacional si no se implementa. | **Parcial; falta evidencia de interfaz y delimitar el mecanismo.** |
| **IE5. Planificación y prioridades** | 10% | `src/planner.py` prioriza reglas operativas, estado del envío, tramo de atraso e historial. Evita proponer reprogramación de envíos ya entregados y duplicar una gestión cerrada equivalente. | Ejecutar escenarios distintos y cambiantes en la interfaz: aprobación pendiente, gestión registrada/cerrada, envío entregado, código inexistente y motivo operativo. Registrar resultado esperado y observado. | **Diseño e implementación presentes; evidencia de escenarios pendiente.** |
| **IE6. Informe técnico, diagramas y flujos** | 10% | Hay documentación de alcance, reglas, contratos, guía viva, diagramas resumido y detallado, y flujo Mermaid. | Preparar el informe formal de máximo cinco páginas requerido por la pauta, seleccionar los diagramas legibles e incorporar evidencia y decisiones de diseño. Completar las justificaciones técnicas con redacción propia del equipo. | **Documentación de apoyo presente; informe formal pendiente.** |
| **IE7. Demostración de decisiones adaptativas** | 10% | `docs/escenarios_eva2.md` define doce escenarios y criterios esperados. | Ejecutar los casos en vivo o registrar una demostración reproducible con varios resultados distintos. Los escenarios diseñados no equivalen a resultados demostrados. | **Pendiente de demostración EVA2.** |
| **IE8. Diagrama de orquestación y README en GitHub** | 10% | El repositorio tiene `README.md`, `arquitectura/diagrama_arquitectura.*` y una versión detallada; se explican módulos y flujo. | Revisar el README como guía autónoma para una persona evaluadora: incluir enlace visible al diagrama, pasos completos de instalación/ejecución y cómo validar scripts. Confirmar que la versión publicada en GitHub coincide con el repositorio local. | **Mayormente presente; falta revisión de completitud y publicación final.** |
| **IE9. Justificación de componentes y referencias** | 10% | Hay decisiones de diseño descritas en `docs/tools.md`, `docs/reglas.md` y `arquitectura/README.md`; la precedencia de POL-COM-003 está documentada. | `docs/reglas.md` deja expresamente pendiente el fundamento técnico del equipo. Incorporar referencias bibliográficas de frameworks en formato APA y explicar la alineación entre cada componente y la necesidad operativa. | **Parcial; justificación propia y bibliografía APA pendientes.** |
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
- `evidencias/escenarios/RESUMEN.md` y `evidencias/REPRODUCCION.md`: resultados de referencia de EVA1, no de EVA2.
- `RUBRICA_EVA2.docx`: instrucciones, aspectos formales e indicadores IE1–IE10.

## Actualización del estado

Actualizar esta matriz cuando se ejecute una prueba, se agregue evidencia o se prepare una sección de la entrega. Para cada caso, anotar fecha, resultado observado, diferencias respecto de lo esperado y vínculo a la evidencia correspondiente.
