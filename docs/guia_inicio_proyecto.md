# Guia de inicio - Sistema de Inventario CEDHI

Esta guia resume como pasar del PRD al desarrollo en Frappe/ERPNext sin modificar el nucleo de `frappe` ni `erpnext`.

## Regla principal

El codigo propio del proyecto debe vivir en:

```text
apps/inventario_cedhi
```

No se deben editar directamente las apps base:

```text
apps/frappe
apps/erpnext
```

Los cambios funcionales se hacen desde la interfaz de Frappe, mediante DocTypes, Roles, Permisos, Workspaces, Reportes y scripts de la app personalizada.

## Aclaracion importante sobre "Modulo"

En Frappe, el campo `Module` al crear un DocType no significa TI, Gastronomia o General. Ese campo indica el modulo tecnico de la app donde se guardara el DocType.

Para este proyecto, al crear DocTypes se debe elegir:

```text
Sistema de Gestión de Inventario CEDHI Nueva Arequipa
```

Los modulos funcionales del negocio se manejaran como un campo dentro del formulario:

```text
Modulo = TI / Gastronomia / General
```

## Fuente actual del MVP

La version vigente del alcance esta en:

```text
apps/inventario_cedhi/Defincion MVP  Proyecto de Prácticas Sociales ABS 2026-01 (1).pdf
```

El PDF anterior queda como referencia, pero la implementacion debe priorizar esta definicion MVP.

## Datos iniciales recibidos

Los archivos Excel iniciales estan en:

```text
apps/inventario_cedhi/datos_iniciales
```

Archivos revisados:

- `3. SALA DE COMPUTO.xlsx`: inventario de bienes/equipos. Incluye cantidad, descripcion del bien, modelo o serie, marca y ubicacion.
- `ABARROTES 2026.xlsx`: catalogo de insumos de cocina. Incluye nombre de insumo y unidad de medida.
- `INVENTARIO DE LICORES.xlsx`: inventario de bebidas/licores. Incluye tipo de licor, marca y cantidad.

Implicancia para el modelo:

- TI/General necesitan campos de activo fisico: marca, modelo/serie, ubicacion, codigo interno y estado activo/inactivo.
- Gastronomia necesita campos de stock: cantidad/stock actual, unidad de medida, stock critico, perecible y fecha de vencimiento.
- El campo `Estado` puede mantenerse simple como `Activo` / `Inactivo`, segun decision del encargado.
- Las incidencias, daños, perdidas, vencimientos o ajustes deben manejarse con `Alerta de Inventario` y/o `Movimiento Kardex`, no necesariamente como valores adicionales de `Estado`.

## Objetivo del MVP para la primera presentacion

Para una primera entrega convincente, no intentes construir todo el PRD. El MVP recomendado es:

1. Login local funcionando en `inventario.local`.
2. Un catalogo maestro de articulos.
3. Tres tipos de inventario: TI, Gastronomia y General.
4. Estados basicos: Activo, Inactivo.
5. Motivo obligatorio cuando el estado sea Inactivo.
6. Filtro por ubicacion y estado.
7. Registro basico de alertas/incidencias enviadas al administrador.
8. Accion administrativa "Verificar y Ajustar Stock" como flujo manual inicial.
9. Exportacion basica desde la lista de Frappe.
10. Una vista o dashboard simple con conteos por estado.

Google Workspace, graficos avanzados, importacion masiva y Kardex completo pueden quedar para iteraciones posteriores.

## DocTypes recomendados

### 1. Ubicacion

Campos:

- Nombre de ubicacion
- Modulo: TI, Gastronomia, General
- Pabellon
- Aula
- Activo

Uso: alimentar listas desplegables de ubicacion.

### 2. Asignacion

Campos:

- Nombre de asignacion
- Modulo
- Activo

Ejemplos: Caritas, Eventos, Laboratorio 1, Cocina, Almacen.

### 3. Articulo de Inventario

Campos comunes:

- Nombre del articulo
- Descripcion
- Modulo: TI, Gastronomia, General
- Ubicacion
- Estado: Activo, Inactivo
- Fecha de adquisicion
- Asignacion
- Fotografia
- Motivo de cambio de estado
- Codigo interno

Configuracion visual:

- El campo visible principal es `Nombre del articulo`.
- Los enlaces a articulos deben mostrar el nombre del articulo y no el ID interno de Frappe.
- El ID interno queda solo como identificador tecnico de base de datos.

Campos especificos:

- Marca: obligatorio si el modulo es TI
- Modelo: obligatorio si el modulo es TI
- Codigo interno
- Pabellon: obligatorio si el modulo es General
- Aula: obligatorio si el modulo es General
- Stock actual: para Gastronomia
- Stock critico: para Gastronomia
- Unidad de medida: para Gastronomia
- Es perecible: para Gastronomia
- Fecha de vencimiento: para Gastronomia

Reglas:

- Si `Estado` es `Inactivo`, `Motivo de cambio de estado` debe ser obligatorio.
- Si `Modulo` es `General` y no hay codigo interno, se debe generar uno automaticamente.
- Si `Modulo` es `Gastronomia`, se debe mostrar stock y alerta visual cuando el stock actual sea menor o igual al stock critico.

Estado actual de formulario:

- Si `Modulo` es `TI`, se muestran los datos tecnicos y `Marca`/`Modelo` son obligatorios.
- Si `Modulo` es `Gastronomia`, se muestran `Datos de Stock` y `Datos de Catalogo Gastronomia`.
- Si `Modulo` es `General`, se muestran `Datos de Mobiliario` y `Pabellon`/`Aula` son obligatorios.
- Si `Estado` es `Inactivo`, `Motivo de cambio de estado` es obligatorio.

### 4. Movimiento Kardex

Campos:

- Articulo
- Tipo de movimiento: Entrada, Salida, Ajuste
- Cantidad
- Fecha
- Responsable
- Observacion

Uso: registrar entradas y salidas de insumos de cocina.

### 5. Alerta de Inventario

Campos:

- Articulo
- Tipo de alerta: Dañado, Perdido, Stock bajo, Caducado, Otro
- Modulo
- Ubicacion
- Reportado por
- Observacion
- Estado de alerta: Pendiente, Verificado, Ajustado, Rechazado
- Fecha de reporte

Uso: representar la bandeja central de alertas del MVP. Permite que docentes, almacen o responsables reporten problemas y que el administrador los revise.

### 6. Unidad Academica

Campos:

- Nombre de unidad
- Descripcion
- Color de tema
- Icono
- Activo

Uso: preparar el selector de contexto propuesto en los mockups. Para el primer MVP puede mapearse con TI, Gastronomia y General sin hacer pantallas personalizadas todavia.

## Roles recomendados

- Superadministrador Inventario: acceso total.
- Admin TI: edita articulos del modulo TI.
- Admin Cocina: edita articulos del modulo Gastronomia.
- Admin General: edita articulos del modulo General y puede ver otros modulos.
- Revisor Inventario: solo lectura.
- Encargado de Almacen: registra movimientos, busca inventario y reporta incidencias.
- Docente / Personal General: reporta incidencias y consulta el historial de sus reportes.

## Orden de implementacion

1. Crear los Roles.
2. Crear los DocTypes `Ubicacion`, `Asignacion` y `Articulo de Inventario`.
3. Configurar permisos por rol.
4. Agregar validaciones de campos obligatorios segun modulo.
5. Crear datos de prueba.
6. Crear `Alerta de Inventario`.
7. Crear filtros y reportes basicos.
8. Crear dashboard simple por estado, modulo y alertas pendientes.
9. Crear `Movimiento Kardex`.
10. Agregar alerta de stock critico.
11. Preparar importacion Excel y autenticacion Google.

## Vistas y filtros configurados

En la lista de `Articulo de Inventario` se configuraron como filtros principales:

- Modulo
- Grupo
- Ubicacion
- Estado
- Stock actual
- Unidad de medida
- Es perecible
- Categoria

Tambien se crearon filtros guardados:

- `Inventario TI`: muestra articulos con `Modulo = TI`.
- `Inventario Gastronomia`: muestra articulos con `Modulo = Gastronomia`.
- `Inventario General`: muestra articulos con `Modulo = General`.
- `Licores`: muestra articulos de Gastronomia con `Grupo = LICORES`.
- `Gastronomia con Stock`: muestra articulos de Gastronomia con `Stock actual > 0`.

Uso desde Frappe:

1. Abrir `Articulo de Inventario`.
2. Ir a la vista de lista.
3. Usar el menu de filtros guardados o aplicar filtros manuales desde la barra de filtros.
4. Si un filtro no aparece inmediatamente, recargar el navegador con `Ctrl + Shift + R`.

## Alertas y reportes creados

Se creo el DocType `Alerta de Inventario` para registrar incidencias o solicitudes de revision.

Campos principales:

- Articulo
- Tipo de alerta: Stock bajo, Dañado, Perdido, Vencido, Ajuste de stock, Otro
- Modulo
- Ubicacion
- Estado de alerta: Pendiente, Verificado, Ajustado, Rechazado
- Fecha de reporte
- Reportado por
- Observacion
- Accion tomada
- Fecha de resolucion

Flujo sugerido:

1. Un usuario reporta una incidencia como `Pendiente`.
2. El administrador revisa la alerta.
3. Si corresponde, ajusta el stock o marca el articulo como inactivo.
4. La alerta pasa a `Verificado`, `Ajustado` o `Rechazado`.

Reportes creados:

- `Resumen Inventario por Modulo`
- `Stock Critico Gastronomia`
- `Inventario TI por Ubicacion`
- `Gastronomia sin Stock Critico`

Uso desde Frappe:

1. Buscar el nombre del reporte en la barra superior.
2. Abrir el reporte.
3. Usar exportacion de Frappe si se necesita Excel.

## Stock critico

La alerta de stock critico usa esta regla:

```text
Modulo = Gastronomia
stock_critico > 0
stock_actual < stock_critico
```

Estado actual:

- Se definio `stock_critico = 10` como regla inicial del MVP para Gastronomia.
- Un articulo entra en stock critico cuando su stock actual es menor que 10.
- Con los datos actuales, muchos insumos aparecen criticos porque fueron importados con `stock_actual = 0`.
- Se conserva el reporte `Gastronomia sin Stock Critico` para detectar futuros registros sin minimo.

Cuando se carguen valores de `stock_critico`, se puede ejecutar la utilidad:

```bash
bench --site inventario.local execute inventario_cedhi.setup_inventory.generate_stock_critical_alerts
```

Esa utilidad crea alertas pendientes de tipo `Stock bajo` sin duplicar alertas pendientes existentes.

## Pendiente / Fuera del primer MVP funcional

- Escaner de codigos de barras o QR.
- Panel docente completo con experiencia personalizada.
- Autenticacion Google Workspace en produccion.
- Importacion masiva por plantillas Excel.
- Graficos avanzados y dashboard totalmente personalizado.
- Creacion visual completa de unidades academicas con iconos y tema.

## Guion sugerido para el video semanal

1. Presentar el problema: el instituto usa inventarios manuales y dispersos.
2. Mostrar el alcance: TI, Gastronomia y General.
3. Mostrar el PRD como base del proyecto.
4. Explicar que se usara Frappe/ERPNext con una app personalizada.
5. Mostrar el login y la app `inventario_cedhi`.
6. Crear o editar un articulo de inventario.
7. Cambiar un articulo a `Inactivo` y mostrar que exige motivo.
8. Registrar una alerta/incidencia y mostrarla como pendiente.
9. Filtrar por ubicacion, estado o modulo.
10. Mostrar el resumen o dashboard inicial.
11. Cerrar con proximos pasos: Kardex, importacion masiva, Google Workspace y paneles pendientes.
