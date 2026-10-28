# Codigo fuente

| Modulo | Estado | Que hace |
|---|---|---|
| `config.py` | Listo | Fabricas de LLM (groq/gemini/ollama) y embeddings |
| `ingest.py` | Listo | Indexacion RAG de fuentes internas y externas |
| `retrieval.py` | Listo | Recuperacion hibrida + fusion RRF |
| `tracking.py` | Listo | Consulta determinista del CSV y calculo de hechos |
| `prompts.py` | Listo | Carga y ensamblado de los prompts |
| `memory.py` | EVA2 | Memoria SQLite para turnos, envíos activos e historial de gestiones |
| `planner.py` | EVA2 | Planificacion determinista, aprobaciones y prevención de gestiones duplicadas |
| `agent.py` | EVA1 + EVA2 | Orquestacion: contexto, tracking, RAG, planner y LLM |
| `app.py` | EVA1 + EVA2 | Interfaz Streamlit con panel de evidencia, memoria y gestiones simuladas |
| `evaluar.py` | Línea base EVA1 | Ejecuta los siete escenarios heredados; aún no evalúa los escenarios nuevos de EVA2 |

Como instalar y probar: ver el `README.md` de la raiz del repositorio.
