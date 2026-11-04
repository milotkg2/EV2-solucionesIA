from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt, RGBColor

ROOT = Path(__file__).resolve().parents[1]
DOCX = ROOT / "informe" / "Informe_Tecnico_EVA2_LogiRuta.docx"
CAPTURAS = ROOT / "evidencias" / "eva2" / "capturas"

doc = Document(DOCX)

replacements = {
    "El proyecto amplía el asistente de la Mesa de Control de LogiRuta con memoria persistente, planificación de acciones y registro simulado de gestiones. El tracking se calcula mediante reglas deterministas; la recuperación híbrida aporta documentos operativos y el LLM redacta respuestas usando esos antecedentes. La evidencia ejecutada el 3 de noviembre confirma los flujos de código inexistente, planificación y estados de gestión en una base temporal. La demostración completa en Streamlit y la generación real con Groq aún requieren evidencia adicional.":
    "El proyecto amplía el asistente de la Mesa de Control de LogiRuta con memoria persistente, planificación de acciones y registro simulado de gestiones. El tracking se calcula mediante reglas deterministas; la recuperación híbrida aporta documentos operativos y Groq redacta respuestas con esos antecedentes. La evidencia del 3 de noviembre confirma los flujos de código inexistente, estados de gestión en SQLite temporal y una demostración Streamlit con ocho fragmentos RAG y generación real citada.",
    "La verificación reproducible se ejecutó con el entorno Python del proyecto mediante python scripts/verificar_eva2_sin_llm.py. El registro completo está en evidencias/eva2/EJECUCION_DETERMINISTA.md.":
    "La verificación reproducible se ejecutó con el entorno Python del proyecto mediante python scripts/verificar_eva2_sin_llm.py. Además, una sesión nueva de Streamlit consultó el envío simulado LR-2026-005317, recuperó ocho fragmentos RAG y generó una respuesta real con Groq openai/gpt-oss-120b. El registro y las capturas están en evidencias/eva2/EJECUCION_DETERMINISTA.md y su carpeta capturas.",
    "La verificación parcial existente registró tracking y planner para seis envíos, control de un código inexistente, estados SQLite y una integración RAG con generación simulada. En esa integración se recuperó el envío activo para un seguimiento y una pregunta general sobre RRF no heredó el caso anterior. Los detalles y límites están en evidencias/eva2/VERIFICACION_TECNICA.md (Valdivia & Romero, 2026).":
    "La verificación parcial anterior registró tracking y planner para seis envíos y una integración RAG con generación simulada. La nueva demostración obtuvo ocho fragmentos, presentó siete referencias documentales en la respuesta y mostró los hechos verificados del envío. Los detalles están en evidencias/eva2/VERIFICACION_TECNICA.md y evidencias/eva2/EJECUCION_DETERMINISTA.md.",
    "La verificación nueva cubre funciones desde Python; no se capturó la interfaz Streamlit porque el navegador abierto no pudo validarse con seguridad.":
    "La demostración de Streamlit se capturó en una sesión aislada del navegador. Se verificaron una consulta con RAG y Groq, y un código inexistente que detuvo el flujo antes de llamar al modelo.",
    "No se llamó a Groq, Gemini ni a un LLM local; por tanto, no se evalúa calidad de respuesta generada ni latencia de generación.":
    "La generación real se verificó en una consulta; sus 8,34 s de latencia son una observación puntual, no una medición de rendimiento general.",
    "La recuperación RAG y citas no se volvieron a ejecutar en esta corrida. Las capturas de interfaz y los escenarios restantes siguen pendientes.":
    "La recuperación devolvió ocho fragmentos y la respuesta citó las fuentes F1–F7. La evidencia no cubre todos los escenarios de la matriz EVA2; quedan pendientes la continuidad de memoria en la interfaz y el flujo de aprobación/registro de gestiones desde Streamlit.",
    "En la preparación de este borrador, Codex apoyó la revisión documental, la ejecución de una verificación técnica acotada y la organización del texto. Los integrantes deben revisar y validar la información, completar cualquier otro uso de IA realizado durante el proyecto y redactar por sí mismos las justificaciones y reflexiones. El LLM configurado para la aplicación no se invocó en la evidencia ejecutada el 3 de noviembre.":
    "En la preparación de este borrador, Codex apoyó la revisión documental, la ejecución de verificaciones técnicas, la demostración de la aplicación y la organización del texto. Los integrantes deben revisar y validar la información, completar cualquier otro uso de IA realizado durante el proyecto y redactar por sí mismos las justificaciones y reflexiones. La aplicación usó Groq para la consulta documentada en este informe.",
}

for paragraph in doc.paragraphs:
    if paragraph.text in replacements:
        paragraph.text = replacements[paragraph.text]

def page_heading(text):
    p = doc.add_paragraph()
    p.paragraph_format.page_break_before = True
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.space_after = Pt(5)
    r = p.add_run(text)
    r.bold = True
    r.font.name = "Arial"
    r.font.size = Pt(15)
    r.font.color.rgb = RGBColor(17, 38, 63)

def add_capture(filename, caption):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(str(CAPTURAS / filename), width=Inches(6.65))
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_after = Pt(4)
    cap.paragraph_format.keep_with_next = True
    run = cap.add_run(caption)
    run.font.name = "Arial"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(65, 80, 98)

for p in list(doc.paragraphs):
    if p.text.startswith("Anexo A  Capturas de Streamlit"):
        node = p._element
        while node.getnext() is not None:
            next_node = node.getnext()
            node.getparent().remove(node)
            node = next_node
        node.getparent().remove(node)
        break

for index, (filename, caption) in enumerate([
    ("EV2-01-generacion-groq.png", "Figura A1. Respuesta diagnóstica generada por Groq con referencias a fuentes."),
    ("EV2-02-fuentes-rag.png", "Figura A2. Fragmentos recuperados mediante RAG híbrido."),
    ("EV2-03-hechos-tracking.png", "Figura A3. Hechos verificados desde el tracking simulado."),
    ("EV2-04-codigo-inexistente.png", "Figura A4. Código inexistente; el flujo no invoca al LLM."),
]):
    page_heading(f"Anexo A  Capturas de Streamlit  {index + 1} de 4")
    add_capture(filename, caption)

doc.core_properties.comments = "Cuerpo técnico de cinco páginas más anexo de evidencias Streamlit."
doc.save(DOCX)
print(DOCX)
