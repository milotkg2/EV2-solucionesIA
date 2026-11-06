# Guion para la presentación EVA2 LogiRuta

**Duración objetivo:** 10 minutos  
**Equipo:** Camilo Romero y Eder Valdivia  
**Orden:** comienza Camilo; Eder presenta la segunda mitad y cierra.  
**Apoyo visual:** `Presentacion_EVA2_LogiRuta_10min.pptx`  
**Evidencia de la demostración:** `evidencias/eva2/EJECUCION_STREAMLIT_ADICIONAL.md` y sus capturas.

> Ensayen con cronómetro. Los textos sirven como base oral: personalicen frases y mencionen solo acciones que cada uno realmente realizó. La demo usa envíos simulados y no ejecuta operaciones reales.

## Distribución

| Tiempo | Diapositiva | Presenta |
|---|---|---|
| 0:00–1:10 | 1. LogiRuta | Camilo |
| 1:10–2:20 | 2. El reto | Camilo |
| 2:20–3:40 | 3. Arquitectura | Camilo |
| 3:40–5:00 | 4. RAG y controles | Camilo |
| 5:00–6:15 | 5. Escenarios ejecutados | Eder |
| 6:15–7:30 | 6. Aprobación humana | Eder |
| 7:30–8:50 | 7. Demostración Streamlit | Eder |
| 8:50–10:00 | 8. Cierre | Eder |

## Camilo

### Diapositiva 1 · LogiRuta · 1:10

Buenos días. Somos Camilo Romero y Eder Valdivia, estudiantes de Ingeniería de Soluciones con IA. Hoy presentamos LogiRuta, nuestro proyecto EVA2: un asistente para apoyar la atención de consultas relacionadas con entregas de última milla.

El problema que tomamos es concreto. Cuando una entrega presenta atraso, reintentos o un paquete que no se puede localizar, una respuesta genérica puede omitir información importante o sugerir una acción que no corresponde. Por eso el asistente combina el estado del envío con políticas de operación y el contexto de la conversación.

En estos diez minutos presentaremos la arquitectura, algunos resultados observados en Streamlit y los límites de la evidencia actual. La demostración utiliza datos simulados: no consulta una empresa real, no emite pagos y no cambia un sistema logístico externo. Al final resumiremos qué falta comprobar.

### Diapositiva 2 · El reto · 1:10

La pregunta del cliente puede parecer similar, pero los hechos cambian la respuesta. Una entrega que ya llegó con un día de atraso necesita información clara y una disculpa. Si un envío todavía espera un nuevo intento, la persona puede preguntar cuántos reintentos quedan. Y si el paquete no se localiza, el equipo de operaciones necesita revisar el caso con mayor prioridad.

El objetivo del proyecto es generar una recomendación trazable y proporcional. Primero necesitamos saber qué ocurrió con el envío. Después consultamos las políticas pertinentes y usamos el motivo de incidencia para proponer el siguiente paso.

En los casos que podrían implicar una compensación, el asistente no debe tomar una decisión económica por sí solo. La propuesta debe indicar quién tiene que revisarla. Este criterio de control aparece en los escenarios de atraso prolongado y paquete no localizable que mostraremos más adelante.

### Diapositiva 3 · Arquitectura · 1:20

La arquitectura tiene cinco etapas. Streamlit recibe el código del envío y la consulta. El módulo de tracking consulta los hechos de nuestro conjunto simulado, como estado, fecha y motivo de incidencia. Luego el componente RAG busca información relacionada en los documentos de política.

La búsqueda es híbrida. LlamaIndex organiza la recuperación y combina la búsqueda por términos de BM25 con similitud semántica usando embeddings locales de `nomic-embed-text`. La capa de memoria conserva los turnos de conversación en SQLite. Esto permite que una pregunta posterior mantenga el contexto dentro de la sesión.

El planner aplica reglas para asignar prioridad y sugerir acciones. Por último, Groq con `openai/gpt-oss-120b` redacta la respuesta a partir de los hechos y el contexto recuperado. La decisión operativa se mantiene en reglas y controles; el LLM ayuda a expresar la respuesta. Esa separación permite explicar por qué el agente responde de una determinada manera.

### Diapositiva 4 · RAG y controles · 1:20

En las ejecuciones registradas, cada consulta válida recuperó ocho fragmentos de contexto. La interfaz permite revisar las fuentes que apoyan la respuesta. RAG significa generación aumentada por recuperación: antes de redactar, el sistema busca información pertinente y la agrega como contexto para el modelo.

También probamos un código inexistente. En ese caso, el sistema respondió que no fue encontrado y detuvo el flujo antes de recuperar fragmentos o llamar al LLM. Ese control evita que el modelo invente el estado de un envío que no existe en la base de demostración.

Hay otros límites operativos. Las compensaciones que requieren autorización quedan pendientes de revisión humana. Los envíos y la fecha son simulados. Por tanto, cuando hablamos de resultados hablamos de corridas locales observadas, no de una validación en producción. Ahora le paso la palabra a Eder para revisar los escenarios y mostrar el flujo en la interfaz.

## Eder

### Diapositiva 5 · Escenarios ejecutados · 1:15

Gracias, Camilo. En esta etapa dejamos evidencia de cinco escenarios de la matriz EVA2. El primero fue M02: consultamos el envío y luego preguntamos cuántos reintentos quedaban sin repetir el código. La sesión identificó el mismo envío y señaló que quedaba un intento disponible de un máximo de tres.

El segundo escenario usó un código inexistente. El sistema lo rechazó sin RAG ni generación. En M01, una entrega completada con un día de atraso, la respuesta propuso informar y disculparse, sin compensación monetaria. Para M04, con cinco días de atraso, el plan se elevó a urgente. Y para M07, un paquete no localizable, se propuso abrir un incidente y escalarlo.

Estos resultados muestran respuestas distintas según el caso, pero todavía cubren cinco de los doce escenarios. No presentamos ese número como cobertura total ni como una medición estadística.

### Diapositiva 6 · Aprobación humana · 1:15

Veamos con más detalle el caso M04, asociado al envío LR-2026-007362. El tracking indicaba que la entrega ya se había completado, pero con cinco días de atraso. El planner propuso un plan urgente: reembolsar el costo de despacho y ofrecer un cupón de despacho gratis.

La política de esta propuesta exige aprobación del Jefe de Operaciones. En Streamlit registramos una gestión simulada, que apareció inicialmente pendiente de aprobación. Luego utilizamos el control de la interfaz para marcarla como aprobada. La aplicación confirmó el cambio y la base SQLite mostró el estado `REGISTRADA`, con aprobación requerida.

La captura de esta diapositiva muestra la confirmación en la interfaz. El resultado prueba el flujo de aprobación dentro de la demo. No representa la emisión del cupón, el reembolso ni una modificación a datos de una empresa real. El paso de volver a planificar el mismo envío para comprobar prevención de duplicados aún queda pendiente.

### Diapositiva 7 · Demostración Streamlit · 1:20

Ahora mostraré el caso de continuidad. En la aplicación ingresaré el código LR-2026-005271. En pantalla revisaremos el hecho de tracking, que corresponde al motivo M02, y los fragmentos recuperados de las políticas.

Después enviaré una segunda pregunta: “¿Cuántos reintentos quedan?”. No volveré a escribir el código. La respuesta observada conservó el envío activo y señaló que quedaba un intento de un máximo de tres. En esta corrida la interfaz mostró recuperación de ocho fragmentos y generación con Groq.

Mientras observamos la pantalla, fijémonos en tres elementos: el envío al que se refiere la conversación, las fuentes RAG que aparecen y la respuesta generada. La captura incluida sirve de respaldo por si la aplicación local no estuviera disponible durante la exposición. Si eso ocurre, diremos que mostramos una captura de la corrida guardada, sin presentarla como una ejecución en vivo.

### Diapositiva 8 · Cierre · 1:10

Para cerrar, resumimos lo que ya observamos y lo que falta. Tenemos cinco escenarios con evidencia en Streamlit. Comprobamos continuidad de contexto entre preguntas de la misma sesión y registramos la aprobación de una propuesta simulada.

Queda pendiente probar la reapertura de una conexión independiente, volver a consultar desde la interfaz la gestión aprobada para revisar seguimiento y duplicados, y ejecutar los escenarios restantes. También debemos terminar las justificaciones y reflexiones personales de cada integrante antes de la entrega.

Nuestra conclusión se limita a los resultados disponibles: los componentes integrados respondieron de forma distinta en los casos representativos y el flujo de aprobación se pudo demostrar en la aplicación local. Aún no tenemos cobertura completa de la matriz ni validación en un sistema real. Gracias por su atención. Quedamos disponibles para preguntas.

## Personalización de autoría

Antes de exponer, cada integrante debe agregar una o dos frases basadas en su trabajo real. No mantengan afirmaciones de tareas que no realizaron.

- **Camilo:** «En mi parte trabajé en [componente o actividad real]. Lo comprobé con [escenario, captura o archivo] y aprendí que [aprendizaje propio]».
- **Eder:** «En mi parte trabajé en [componente o actividad real]. Lo comprobé con [escenario, captura o archivo] y aprendí que [aprendizaje propio]».

Para preguntas técnicas, usen las evidencias y cifras de `docs/rubrica_eva2.md` y `evidencias/eva2/EJECUCION_STREAMLIT_ADICIONAL.md`. Si no verificaron algo, indiquen que sigue pendiente.
