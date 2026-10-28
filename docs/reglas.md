# Reglas de decisión operativa

Estas reglas preliminares se basan en el SOP-OPS-014, CAT-OPS-007, POL-COM-003 y SLA-COM-002 de la EVA1. Para determinar si corresponde una compensación y bajo qué condiciones, POL-COM-003 (tabla detallada) es la referencia principal. El SOP orienta la gestión operativa y se interpreta de forma compatible con esa política. El planner debe devolver la primera acción aplicable junto con sus hechos y referencias.

| Prioridad | Condición | Acción propuesta | Fuente |
|---:|---|---|---|
| 1 | El código de envío no existe en los registros | Detener el diagnóstico y solicitar verificar el código; no generar diagnóstico con hechos inexistentes | Comportamiento existente en `src/agent.py` |
| 2 | Paquete perdido o dañado (M07) | Abrir incidente simulado y escalar; aplicar compensación solo según política y aprobación correspondiente | CAT-OPS-007 M07; POL-COM-003 §§2–4 |
| 3 | Tres o más intentos fallidos | Proponer devolución al origen y notificación al retailer el mismo día hábil | SOP-OPS-014 §6 |
| 4 | Dirección incompleta (M03) | Contactar para validar la dirección; si no hay respuesta en 48 horas, proponer devolución al origen; sin compensación | SOP-OPS-014 §6; CAT-OPS-007 M03; POL-COM-003 §2 |
| 5 | Cliente ausente (M02) | Proponer hasta tres intentos separados por 24 a 48 horas hábiles; sin compensación | SOP-OPS-014 §4; CAT-OPS-007 M02; POL-COM-003 §2 |
| 6 | Rechazo del consumidor (M05) | No reprogramar; proponer devolución al origen; sin compensación | SOP-OPS-014 §4; CAT-OPS-007 M05; POL-COM-003 §2 |
| 7 | Zona de riesgo o acceso restringido (M06) | Proponer hasta dos intentos en horario diurno; revisar manualmente cualquier excepción de compensación | SOP-OPS-014 §4; CAT-OPS-007 M06; POL-COM-003 §2 |
| 8 | Retraso atribuible a LogiRuta de hasta 24 horas | Proponer reprogramación al siguiente día hábil e informar una nueva fecha solo tras confirmación de Planificación; no ofrecer compensación económica | POL-COM-003 §2; SOP-OPS-014 §6 y §8 |
| 9 | Retraso atribuible a LogiRuta de más de 24 y hasta 72 horas | Priorizar el caso, informar al retailer y evaluar la compensación permitida por POL-COM-003, con la aprobación exigida | POL-COM-003 §2; SOP-OPS-014 §§6–7; SLA-COM-002 §4 |
| 10 | Retraso atribuible a LogiRuta superior a 72 horas | Escalar a Operaciones y tramitar la compensación que corresponda según POL-COM-003 y las aprobaciones requeridas | POL-COM-003 §2; SOP-OPS-014 §7; SLA-COM-002 §4 |
| 11 | Responsabilidad, estado o evidencia insuficiente para aplicar una regla | No inventar una acción; solicitar antecedentes o dejar el caso pendiente de revisión humana | SOP-OPS-014 §§5, 8–9 |

## Criterio adoptado para compensaciones

El equipo define POL-COM-003 como referencia principal para decidir elegibilidad, tipo y condiciones de compensación. Las menciones del SOP a compensación obligatoria se ejecutan dentro de lo permitido por esa política y los SLA aplicables; no habilitan por sí solas un beneficio que POL-COM-003 excluya. En particular, los retrasos de hasta 24 horas no reciben compensación económica. Cuando la política requiera evaluación o aprobación, el planner debe dejar el caso pendiente de aprobación y no afirmar que la compensación ya fue autorizada.

Esta precedencia es una decisión de diseño del equipo para resolver la diferencia entre documentos de EVA1; debe quedar explicada en la entrega y verificarse con los fragmentos fuente recuperados en cada caso.

## Fundamento técnico del diseño

**Pendiente de redactar por el equipo**, según las instrucciones de la EVA2 sobre justificaciones técnicas.
