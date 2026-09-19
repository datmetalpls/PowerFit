# Levantamiento de requerimientos — Sistema PowerFit

## 1. Antecedentes

Este documento reúne el intercambio de correos utilizado para levantar y aclarar los requerimientos del sistema de gestión de PowerFit. La comunicación se divide en tres partes:

1. Solicitud inicial del cliente.
2. Preguntas de aclaración realizadas por el equipo de desarrollo.
3. Respuestas del cliente a las preguntas planteadas.

---

## 2. Correo inicial de requerimiento

**Remitente:** Cliente PowerFit  
**Destinatario:** Equipo de desarrollo  
**Asunto:** Requerimientos para el sistema de gestión de PowerFit

Hola:

En PowerFit ofrecemos tres tipos de clase: Yoga, Spinning y Crossfit. Cada una tiene un cupo máximo y una duración distintos, y el cálculo de cuántos socios más pueden inscribirse depende del tipo de clase.

Tenemos dos tipos de trabajador: el instructor, que dicta las clases y marca la asistencia, y la recepcionista, que inscribe socios nuevos y cobra las mensualidades, pero no puede crear ni modificar clases.

Cada socio se inscribe con su RUT y necesitamos que el sistema valide que esté bien formado antes de crear la ficha.

Cuando un socio se inscribe para el mes, generalmente reserva varias clases —por ejemplo, Yoga los lunes y Crossfit los miércoles— y todo eso debe quedar bajo una misma inscripción mensual, con el detalle de cada clase reservada.

No queremos que se pueda inscribir a alguien en una clase que ya tiene el cupo lleno ni que se deje entrar al gimnasio a un socio con la membresía vencida.

Vendemos suplementos importados en el mesón y esos productos los cotizamos según el dólar del día, porque los compramos en esa moneda.

Quedo atento a sus dudas, pero la propuesta final debe ser subida al espacio habilitado en el Ambiente de Aprendizaje.

Saludos.

---

## 3. Respuesta del equipo y preguntas de aclaración

**Remitente:** Equipo de desarrollo  
**Destinatario:** Cliente PowerFit  
**Asunto:** Consultas para precisar los requerimientos del sistema PowerFit

Hola, Sr. Cliente:

Esperamos que se encuentre bien.

A continuación, queremos plantearle algunas dudas relevantes sobre los servicios que PowerFit ofrece actualmente. Sus respuestas nos permitirán comprender mejor el modelo de negocio, delimitar el alcance de la propuesta y desarrollar una solución adecuada.

1. ¿PowerFit trabajará únicamente con las disciplinas mencionadas —Yoga, Spinning y Crossfit— o el sistema deberá permitir incorporar posteriormente otras actividades, como Pilates, entrenamiento funcional o fuerza?
2. ¿El gimnasio contará solamente con clases dirigidas o también tendrá una sala de máquinas, espacios para ejercicios funcionales y áreas de entrenamiento libre?
3. ¿PowerFit tendrá una sola sede o debemos diseñar el sistema considerando un posible crecimiento hacia múltiples sedes o sucursales?
4. ¿PowerFit ofrecerá solamente una membresía mensual o contará con diferentes planes, packs de clases y modalidades de acceso?
5. En el requerimiento se mencionan dos tipos de trabajadores: instructor y recepcionista. ¿También debemos considerar perfiles como administrador, personal administrativo, personal de aseo o encargados de mantenimiento? De ser así, ¿alguno de estos trabajadores deberá utilizar el sistema?
6. ¿El RUT será el identificador principal del socio o también se le asignará un número de matrícula? En caso de que el socio pueda acceder al sistema, ¿qué dato utilizará como nombre de usuario: RUT, correo electrónico, matrícula u otro identificador?
7. ¿Qué datos personales necesitan recopilar de los socios para su registro y gestión? ¿Cuentan actualmente con una ficha de inscripción o algún formato definido?
8. ¿Existe alguna normativa legal, política interna o requisito que determine qué datos deben solicitarse, durante cuánto tiempo deben conservarse y quiénes podrán acceder a ellos? En caso de recopilar información de salud, lesiones, contactos de emergencia u otros datos sensibles, ¿se requerirá alguna autorización o consentimiento específico del socio?
9. Respecto de los suplementos alimenticios, ¿se venderán como productos completos —por ejemplo, tarros de proteína o creatina—, como porciones individuales, packs o preparaciones listas para consumir, como batidos?
10. ¿La venta de suplementos deberá incluir control y descuento de inventario? Además, ¿las ventas se realizarán únicamente de manera presencial o también se contempla una modalidad de comercio electrónico?

Estas respuestas nos ayudarán a definir correctamente el modelo de negocio y el alcance del sistema que debemos diseñar e implementar.

Junto con José Luis Arriagada Concha, quedamos atentos a sus comentarios y a cualquier información adicional que considere relevante.

Saludos.

---

## 4. Respuesta del cliente

**Remitente:** Cliente PowerFit  
**Destinatario:** Equipo de desarrollo  
**Asunto:** Respuestas a consultas sobre el sistema PowerFit

Hola, equipo:

Les respondo en orden:

1. Por ahora trabajamos solo con Yoga, Spinning y Crossfit. No tenemos un plan concreto de agregar otras disciplinas, pero sería conveniente que el sistema permita sumar una clase nueva sin mayores dificultades.
2. Por ahora, el sistema es solo para las clases con cupo e instructor. La sala de máquinas y el área libre son de acceso abierto para quienes tengan la membresía al día y no necesitan ser gestionadas en el sistema.
3. Tenemos una sola sede y no estamos pensando en abrir otra por ahora.
4. Por ahora ofrecemos únicamente una membresía mensual. No tenemos packs ni otras modalidades, así que no es necesario que el sistema las contemple.
5. Solo el instructor y la recepcionista utilizarán el sistema. También contamos con personal de aseo y mantenimiento, pero no necesita acceder a este.
6. El RUT es el dato con el que identificamos a los socios. Los socios no acceden al sistema, por lo que no requieren nombre de usuario ni contraseña; esas credenciales son solo para el instructor y la recepcionista.
7. Para la ficha del socio necesitamos su nombre y su RUT. No tenemos un formato definido más allá de esos datos, por eso les estamos solicitando una propuesta.
8. No tenemos ninguna normativa especial que cumplir ni manejamos datos de salud de los socios. Es suficiente con validar correctamente el RUT.
9. Los suplementos se venden como productos completos, por ejemplo, tarros de proteína o creatina. No vendemos porciones ni preparamos batidos.
10. Cada venta debe descontar las unidades correspondientes del stock. Todas las ventas se realizan presencialmente en el mesón; no tenemos venta en línea.

Saludos.

---

## 5. Requerimientos consolidados

### 5.1. Alcance general

- El sistema gestionará una sola sede de PowerFit.
- El alcance incluirá clases dirigidas, socios, membresías mensuales, asistencia y venta presencial de suplementos.
- La sala de máquinas y el área de entrenamiento libre quedan fuera de la gestión del sistema, salvo la validación de que el socio tenga su membresía vigente para ingresar.
- No se contemplan comercio electrónico, múltiples sedes, packs de clases ni otros planes de membresía.

### 5.2. Clases

- Las disciplinas iniciales serán Yoga, Spinning y Crossfit.
- Cada tipo de clase tendrá una duración y un cupo máximo propios.
- El sistema deberá calcular los cupos disponibles de acuerdo con el tipo de clase y las reservas existentes.
- No se podrá reservar una clase cuyo cupo esté completo.
- El diseño deberá facilitar la incorporación futura de nuevos tipos de clase.

### 5.3. Usuarios y permisos

- El sistema tendrá dos tipos de usuario: instructor y recepcionista.
- El instructor podrá consultar las clases que dicta y registrar la asistencia.
- La recepcionista podrá registrar socios, gestionar inscripciones mensuales, cobrar mensualidades y realizar ventas presenciales de suplementos.
- La recepcionista no podrá crear ni modificar clases.
- Los socios no accederán directamente al sistema y, por tanto, no tendrán credenciales.
- El personal de aseo y mantenimiento no utilizará el sistema.

### 5.4. Socios y membresías

- Cada socio se identificará mediante su RUT.
- Antes de crear una ficha, el sistema deberá validar que el RUT esté correctamente formado.
- La ficha del socio contendrá, como mínimo, nombre y RUT.
- La modalidad disponible será exclusivamente la membresía mensual.
- El sistema deberá impedir el ingreso al gimnasio cuando la membresía del socio se encuentre vencida.

### 5.5. Inscripciones y reservas

- Una inscripción mensual podrá agrupar varias reservas de clases.
- Cada inscripción deberá conservar el detalle de las clases reservadas por el socio.
- Antes de agregar una reserva, el sistema deberá verificar la disponibilidad de cupos.

### 5.6. Suplementos e inventario

- Se venderán productos completos, como tarros de proteína o creatina.
- No se venderán porciones individuales ni preparaciones listas para consumir.
- Las ventas serán exclusivamente presenciales y se realizarán en el mesón.
- Cada venta deberá descontar automáticamente las unidades vendidas del stock.
- El precio de los suplementos importados se calculará utilizando el valor del dólar del día.

## 6. Reglas de negocio identificadas

| Código | Regla de negocio |
|---|---|
| RN-01 | El RUT debe ser válido antes de registrar a un socio. |
| RN-02 | El RUT identifica de manera única a cada socio. |
| RN-03 | Una reserva solo puede realizarse si la clase tiene cupos disponibles. |
| RN-04 | Los cupos disponibles corresponden al cupo máximo de la clase menos las reservas vigentes. |
| RN-05 | Varias reservas pueden formar parte de una misma inscripción mensual. |
| RN-06 | Un socio con membresía vencida no puede ingresar al gimnasio. |
| RN-07 | La recepcionista no puede crear ni modificar clases. |
| RN-08 | El instructor puede registrar la asistencia de las clases que dicta. |
| RN-09 | Toda venta de suplementos debe disminuir el stock correspondiente. |
| RN-10 | El valor de venta de un suplemento importado se calcula según el dólar del día. |

## 7. Fuera de alcance

- Gestión de múltiples sedes.
- Comercio electrónico.
- Acceso de socios al sistema.
- Gestión de la sala de máquinas o de áreas de entrenamiento libre.
- Planes distintos de la membresía mensual.
- Venta de porciones individuales o preparación de batidos.
- Gestión de personal de aseo o mantenimiento.
- Registro de información médica o datos de salud.

## 8. Pendientes de definición

Los siguientes puntos no quedaron definidos explícitamente en el intercambio y podrían requerir validación antes de implementar el sistema:

- Quién estará autorizado para crear o modificar las clases, dado que la recepcionista no puede hacerlo.
- Fuente del valor diario del dólar y frecuencia con que deberá actualizarse.
- Fórmula final para convertir el costo en dólares al precio de venta en pesos, incluyendo margen, impuestos y redondeo.
- Datos y credenciales requeridos para registrar a instructores y recepcionistas.
- Procedimiento para cancelar reservas y devolver cupos.
- Tratamiento de inasistencias y posibilidad de reservar dos clases en horarios coincidentes.
- Datos mínimos de cada suplemento, niveles mínimos de stock y manejo de productos agotados.
- Comprobante o registro que deberá generar el cobro de una mensualidad o la venta de un suplemento.

