# Ejecución adicional en Streamlit

**Fecha:** 6 de noviembre de 2026
**Equipo:** Eder Valdivia y Camilo Romero
**Entorno:** Streamlit local, Groq `openai/gpt-oss-120b`, embeddings locales `nomic-embed-text`; tracking simulado y fecha operacional fija `2026-09-23`.

Esta corrida amplía la evidencia del 3 de noviembre. Las consultas usaron el agente completo de la interfaz, con tracking, recuperación híbrida, memoria SQLite, planner y generación real. Los tiempos son los que mostró Streamlit en esta sesión; la primera consulta M02 se ejecutó con componentes locales fríos.

## Escenarios y resultados observados

| Caso | Entrada | Resultado visible | Recuperación / generación | Capturas |
|---|---|---|---|---|
| EV2-01 · continuidad M02 | `LR-2026-005271`; luego “¿Cuántos reintentos quedan?” sin repetir el código | La sesión conservó el envío activo. La respuesta de seguimiento volvió a identificar M02 y señaló un intento disponible de un máximo de tres; no propone compensación. | Inicial: 47,42 s / 8,97 s. Seguimiento: 2,77 s / 4,14 s. 8 fragmentos por consulta. | [`EV2-05`](capturas/EV2-05-memoria-antes-del-seguimiento.png), [`EV2-06`](capturas/EV2-06-memoria-seguimiento.png), [`EV2-07`](capturas/EV2-07-seguimiento-respuesta.png) |
| EV2-03 · código inexistente | `LR-2026-999999` | “No encontrado”; cero fragmentos, cero generación y no se llamó al LLM. | 0,0 s / 0,0 s. | [`EV2-04`](capturas/EV2-04-codigo-inexistente.png) |
| EV2-04 · entrega tardía M01 | `LR-2026-008477`, entregado con un día de atraso | Propuso informar la entrega y registrar una disculpa formal; sin compensación económica ni reprogramación. Plan de prioridad media para Mesa de Control, con revisión humana. | 2,83 s / 4,65 s. 8 fragmentos. | [`EV2-08`](capturas/EV2-08-entrega-completada-hechos.png), [`EV2-09`](capturas/EV2-09-entrega-completada-plan.png) |
| EV2-10 · paquete M07 no localizable | `LR-2026-009011` | Plan urgente para abrir incidente y escalar a Operaciones. Propone reposición o reembolso del producto con retailer más reembolso de despacho, pendiente de aprobación de Gerencia Comercial. | 2,93 s / 4,65 s. 8 fragmentos. | [`EV2-10`](capturas/EV2-10-paquete-no-localizable-plan.png), [`EV2-11`](capturas/EV2-11-paquete-no-localizable-hechos.png) |
| EV2-06 · atraso M04 de cinco días | `LR-2026-007362`, ya entregado | Plan urgente: reembolso del despacho y cupón de despacho gratis, sujeto a aprobación del Jefe de Operaciones. | 2,97 s / 14,13 s. 8 fragmentos. | [`EV2-12`](capturas/EV2-12-cinco-dias-plan-pendiente.png) |

## Flujo de aprobación en la interfaz

Para `LR-2026-007362`, la interfaz permitió registrar la propuesta como gestión simulada **#3**, inicialmente `PENDIENTE_APROBACION`. Se pulsó **Marcar aprobada** y la aplicación confirmó que la gestión quedó aprobada y registrada. Una consulta posterior a SQLite devolvió:

```text
id=3, codigo=LR-2026-007362, estado=REGISTRADA, requiere_aprobacion=True
```

Las capturas muestran la propuesta pendiente, la acción de aprobación y la vista posterior. La marca `REGISTRADA` representa el estado de la demo; no se emitió cupón ni se modificó un sistema real.

- [`EV2-13`](capturas/EV2-13-gestion-registrada-pendiente.png): gestión #3 pendiente de decisión humana.
- [`EV2-14`](capturas/EV2-14-gestion-aprobada-registrada.png): confirmación de la acción de aprobación.
- [`EV2-15`](capturas/EV2-15-gestion-aprobada-verificada.png): vista posterior con la acción de cierre disponible; estado corroborado en SQLite.

## Alcance que sigue pendiente

- La continuidad se verificó entre consultas dentro de la misma sesión de Streamlit; no se completó una comprobación de reapertura en una conexión de navegador separada.
- El paso a `REGISTRADA` se observó para el caso de cinco días, pero no se volvió a planificar ese mismo envío para demostrar seguimiento posterior ni prevención de duplicados desde la interfaz.
- Los escenarios EV2-02, EV2-05, EV2-07, EV2-08 completo, EV2-09, EV2-11 y EV2-12, junto con otros motivos, todavía requieren su evidencia específica.
- Los tiempos reportados corresponden a una corrida puntual y no son una evaluación estadística del servicio.

La evidencia determinista de planner, memoria y estados con base SQLite temporal permanece en [`EJECUCION_DETERMINISTA.md`](EJECUCION_DETERMINISTA.md). Las capturas se anexan también al informe técnico.
