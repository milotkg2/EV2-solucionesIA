# Revisión de avance según la rúbrica EVA2

**Equipo:** Eder Valdivia y Camilo Romero  
**Asignatura:** Ingeniería de Soluciones con IA (ISY0101)  
**Revisión documental:** 6 de noviembre de 2026

## Propósito y alcance

Esta matriz contrasta la pauta oficial `RUBRICA_EVA2.docx` con el código, la documentación y las evidencias disponibles en el repositorio. Es una revisión de avance para orientar el trabajo; **no es una calificación ni reemplaza la evaluación docente**. “Implementado” significa que hay código o documentación visible; “evidencia pendiente” significa que aún falta demostrarlo con una ejecución de EVA2 o incorporarlo a la entrega final.

La línea base de siete escenarios y 34/34 verificaciones corresponde a EVA1; no se cuenta como ejecución de EVA2. Entre el 3 y el 6 de noviembre de 2026 se añadieron la verificación determinista de tracking/planner/memoria y cinco casos con evidencia en Streamlit: seguimiento M02 en la misma sesión, código inexistente, entrega tardía M01, atraso M04 de cinco días con gestión aprobada y M07 no localizable. Se recuperaron ocho fragmentos por consulta. La reapertura en una conexión separada y la cobertura completa de 12 escenarios siguen pendientes. Los resultados están en `evidencias/eva2/EJECUCION_STREAMLIT_ADICIONAL.md`; las capturas se anexan al informe.

## Matriz por indicador

| Indicador | Peso | Avance respaldado por el repositorio | Pendiente para cerrar el indicador | Estado documental |
|---|---:|---|---|---|
| **IE1. Herramientas dentro del agente** | 10% | La demo Streamlit utilizó tracking, RAG y generación Groq, y registró/aprobó una gestión simulada. | Demostrar en la interfaz la consulta posterior a la aprobación y el control de duplicados. | **Integración demostrada en casos representativos; seguimiento posterior pendiente.** |
| **IE2. Frameworks, escalabilidad y compatibilidad** | 10% | El stack integra LlamaIndex para RAG, Streamlit para interfaz, SQLite y Groq como proveedor configurable; las dependencias están en `requirements.txt`. | Explicar y justificar por el equipo el rol de cada framework y sus límites. La orquestación del agente está implementada en Python propio; documentar cómo esa decisión satisface el requisito de framework y qué implicaría escalarla. | **Parcial; falta justificación y validación integral.** |
| **IE3. Memoria de contenido y continuidad** | 10% | `src/memory.py` conserva turnos y envío activo. En Streamlit se consultó M02 y luego se preguntó por intentos sin repetir el código; la memoria mantuvo `LR-2026-005271`. | Reabrir la misma sesión en una conexión nueva y demostrar recuperación después de reiniciar la interfaz. | **Continuidad entre turnos demostrada; recuperación en conexión nueva pendiente.** |
| **IE4. Recuperación semántica del contexto** | 10% | La aplicación recuperó ocho fragmentos por consulta; la respuesta usó referencias a fuentes. El seguimiento M02 conservó el código y el contexto entre dos preguntas. Los turnos se recuperan por recencia; RAG busca en documentos. | Probar una pregunta general independiente dentro de la misma sesión y comprobar que no herede el caso. | **RAG y seguimiento contextual demostrados; separación de consulta independiente pendiente.** |
| **IE5. Planificación y prioridades** | 10% | Se demostraron planes distintos para M02, M01, M04 y M07. En M04, una propuesta urgente quedó pendiente, se aprobó en la interfaz y SQLite la mostró como `REGISTRADA`. | Volver a consultar la gestión registrada y demostrar el seguimiento sin duplicados; ampliar condiciones. | **Planificación adaptativa y aprobación/registro en interfaz demostrados parcialmente.** |
| **IE6. Informe técnico, diagramas y flujos** | 10% | El informe incorpora resultados nuevos y ocho capturas seleccionadas como anexo. Incluye ejemplos orientativos para que cada integrante los complete según sus aportes reales. | Revisar la extensión formal; reescribir los ejemplos de reflexión, y completar justificación y conclusiones propias antes de entregar. | **Evidencia y modelos de redacción presentes; texto final de autoría del equipo pendiente.** |
| **IE7. Demostración de decisiones adaptativas** | 10% | Cinco escenarios tienen resultado documentado: M02 con seguimiento, no encontrado, entrega M01, atraso M04 y paquete M07. La gestión M04 pasó por aprobación humana y registro. | Ejecutar los escenarios restantes y ensayar la exposición; no afirmar que la matriz completa ya está cubierta. | **Demostración parcial en Streamlit; 5 de 12 casos documentados.** |
| **IE8. Diagrama de orquestación y README en GitHub** | 10% | El repositorio tiene `README.md`, diagramas resumido y detallado y ahora enlaza el informe y la evidencia de EVA2. | Revisar el README como guía autónoma para una persona evaluadora: añadir enlace visible al diagrama, verificar los pasos de instalación/ejecución y scripts, y confirmar que GitHub refleja la versión final. | **Recursos presentes; falta revisión final de publicación y ejecución.** |
| **IE9. Justificación de componentes y referencias** | 10% | Hay decisiones de diseño descritas en `docs/tools.md`, `docs/reglas.md` y `arquitectura/README.md`; el borrador del informe ya incluye referencias técnicas en formato autor-fecha APA. | `docs/reglas.md` deja pendiente el fundamento técnico redactado por el equipo. Explicar la alineación entre cada componente y la necesidad operativa, validar las referencias internas y completar bibliografía si corresponde. | **Parcial; referencias incorporadas al borrador y justificación propia pendiente.** |
| **IE10. Comunicación técnica basada en evidencia** | 10% | La guía de estudio y los registros de verificación reúnen conceptos, arquitectura y ejemplos para preparar la exposición. | Preparar y ensayar exposición y preguntas. Ambos integrantes deben explicar decisiones con ejemplos ejecutados y evidencias concretas; no se puede evaluar este indicador solo con el repositorio. | **Pendiente de presentación.** |

## Pendientes prioritarios

1. **Completar evidencia de ejecución de EVA2.** Cinco de doce escenarios tienen evidencia; faltan los casos de `docs/escenarios_eva2.md` todavía sin ejecutar.
2. **Cerrar la demostración de memoria y gestiones.** Reabrir una sesión en una conexión nueva y consultar la gestión `REGISTRADA` para comprobar seguimiento y prevención de duplicados desde Streamlit.
3. **Completar el texto del equipo.** Reescribir los ejemplos de Eder y Camilo a partir de sus tareas y aprendizajes reales. Añadir justificación técnica y conclusión propia según la pauta.
4. **Preparar la presentación de 20 minutos.** Distribuir participación entre Eder y Camilo y ensayar preguntas usando resultados comprobables.
5. **Declarar el uso de IA.** La pauta requiere indicar qué herramientas se usaron y cómo. Cada integrante debe escribir sin apoyo de IA su reflexión personal y las conclusiones que le correspondan.
6. **Revisar la entrega en GitHub.** Verificar README, diagramas, instrucciones de ejecución, scripts y evidencias, sin incluir `.env`, claves ni bases de datos locales.

## Evidencias consideradas

- `README.md`: alcance, estructura y avance general del proyecto.
- `docs/alcance.md`, `docs/tools.md` y `docs/reglas.md`: objetivos, contratos y reglas operativas.
- `arquitectura/README.md` y `arquitectura/diagrama_arquitectura.*`: explicación y diagramas.
- `docs/GUIA_ESTUDIO_EVA2.md`: guía de conceptos y preparación.
- `docs/escenarios_eva2.md`: matriz de 12 escenarios con cinco ejecuciones de EVA2 documentadas.
- `evidencias/eva2/VERIFICACION_TECNICA.md`: verificaciones parciales locales y sus límites.
- `scripts/verificar_eva2_sin_llm.py` y `evidencias/eva2/EJECUCION_DETERMINISTA.md`: comprobaciones reproducibles de tracking, planner y memoria del 3 de noviembre.
- `evidencias/eva2/capturas/` y anexo del informe: demostración Streamlit, respuesta real de Groq, fragmentos RAG, hechos de tracking y código inexistente.
- `evidencias/eva2/EJECUCION_STREAMLIT_ADICIONAL.md`: resultados, tiempos y límites de las ejecuciones del 6 de noviembre.
- `informe/Informe_Tecnico_EVA2_LogiRuta.docx`: borrador técnico de cinco páginas; requiere completar las secciones de autoría del equipo.
- `evidencias/escenarios/RESUMEN.md` y `evidencias/REPRODUCCION.md`: resultados de referencia de EVA1, no de EVA2.
- `RUBRICA_EVA2.docx`: instrucciones, aspectos formales e indicadores IE1–IE10.

## Actualización del estado

Actualizar esta matriz cuando se ejecute una prueba, se agregue evidencia o se prepare una sección de la entrega. Para cada caso, anotar fecha, resultado observado, diferencias respecto de lo esperado y vínculo a la evidencia correspondiente.
