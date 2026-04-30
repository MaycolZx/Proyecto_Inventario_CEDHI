# Analisis de datos iniciales

Fecha de revision: 2026-04-27

## Archivos revisados

```text
apps/inventario_cedhi/datos_iniciales/2do TECNICAS 2.xlsx
apps/inventario_cedhi/datos_iniciales/3. SALA DE COMPUTO.xlsx
apps/inventario_cedhi/datos_iniciales/INVENTARIO DE LICORES.xlsx
apps/inventario_cedhi/datos_iniciales/lista de insumos gastronomia.xlsx
```

Nota: `ABARROTES 2026.xlsx` fue retirado de la carpeta para evitar confusion. Queda documentado solo porque fue comparado previamente.

## Comparacion: ABARROTES 2026 vs lista de insumos gastronomia

`ABARROTES 2026.xlsx` parece ser un catalogo simple de insumos:

- Nombre de insumo
- Unidad de medida
- 311 registros

`lista de insumos gastronomia.xlsx` parece ser el catalogo maestro actualizado:

- Codigo Articulo
- Grupo
- Categoria
- Marca
- Unidad Medida
- Presentacion
- Proveedor de Referencia
- Nombre Insumo
- Perecedero(SI/NO)
- Medida
- %Desperdicio
- Cantidad Minima
- Precio
- 882 registros

Resultado de comparacion por nombre normalizado:

- Abarrotes 2026: 311 registros
- Lista de insumos gastronomia: 882 registros
- Coincidencias encontradas: 290
- Registros de abarrotes no encontrados en la lista nueva: 21
- Registros nuevos/no presentes en abarrotes: 590

Decision recomendada:

```text
Usar lista de insumos gastronomia.xlsx como fuente principal para el catalogo de cocina.
```

`ABARROTES 2026.xlsx` queda como referencia historica o archivo auxiliar, no como fuente principal.

Archivo preparado para importacion:

```text
apps/inventario_cedhi/datos_iniciales/csv/import_articulos_gastronomia.csv
```

Este CSV contiene 882 registros mapeados al DocType `Articulo de Inventario`, con:

- `Modulo`: Gastronomia
- `Estado`: Activo
- `Ubicacion`: Cocina Principal
- `Asignacion`: Cocina Principal
- `Stock actual`: 0
- Datos de catalogo desde `lista de insumos gastronomia.xlsx`

Estado de carga en Frappe:

- Importado correctamente: 882 registros
- Fuente marcada en Frappe: `lista de insumos gastronomia.xlsx`

## Registros de ABARROTES no encontrados en la lista nueva

- CAMARON SECO
- CUAJO
- ESENCIA DE ALMENDRAS
- ESENCIA DE CHANCAY
- ESENCIA DE CHIRIMOYA
- ESENCIA DE FRESA
- FIDEOS CABELLO DE ANGEL
- FIDEOS TORNILLO
- HARINA DE ARROZ
- HARINA PAN
- HARINA PANADERA
- HARINA PREMIUN
- JAMON PAISA
- LEVADURA SECA
- NUES CAJU
- PASTA DE MACARRON CHUSCO
- QUESO SUISO
- SALSA BBQ
- SALSA CHARSIU
- SALSA MENSI
- YOGURT GRIEGO

Estos deben revisarse manualmente porque pueden ser diferencias de escritura, productos retirados o faltantes reales en el archivo actualizado.

## Grupos detectados en lista de insumos gastronomia

- ABARROTES: 564
- VERDURAS: 141
- CARNICO: 80
- FRUTA: 49
- CARNICOP: 33
- Sin grupo: 15

## Perecederos detectados

- NO: 470
- SI: 394
- Sin dato: 18

## Sala de computo

Archivo:

```text
apps/inventario_cedhi/datos_iniciales/3. SALA DE COMPUTO.xlsx
```

Estructura util detectada:

- Hoja
- Numero de fila/origen
- Cantidad
- Descripcion del bien
- Modelo y/o serie
- Marca
- Ubicacion
- Fecha de adquisicion
- Estado original

Resumen:

- Registros limpios: 227
- Hoja `CEDHI`: 155 registros
- Hoja `Copia de CEDHI`: 72 registros
- Cantidad: todos los registros tienen cantidad 1
- Estado original: todos figuran como `B`
- Fechas: 2025-12-22 y 2025-12-16
- Ubicaciones detectadas: Laboratorio de computo, Almacen Soldadura y una variante con error de escritura (`Laboraorio de computo`)

Archivo preparado para importacion:

```text
apps/inventario_cedhi/datos_iniciales/csv/import_articulos_ti_sala_computo.csv
```

Mapeo:

- `Modulo`: TI
- `Nombre del articulo`: descripcion del bien
- `Marca`: marca del Excel
- `Modelo`: modelo/serie del Excel
- `Codigo interno`: modelo/serie del Excel
- `Cantidad`: cantidad del Excel
- `Estado`: Activo
- `Estado de conservacion`: estado original del Excel (`B`)
- `Ubicacion` y `Asignacion`: Laboratorio de computo o Almacen Soldadura
- `Fuente de datos`, `Hoja origen` y `Numero origen`: trazabilidad de importacion

Estado de carga en Frappe:

- Importado correctamente: 227 registros
- Fuente marcada en Frappe: `3. SALA DE COMPUTO.xlsx`

## Licores

Archivo:

```text
apps/inventario_cedhi/datos_iniciales/INVENTARIO DE LICORES.xlsx
```

Estructura util detectada:

- Tipo/categoria de licor
- Marca
- Cantidad
- Total por grupo, usado como subtotal visual del Excel

Resumen:

- Registros: 41
- Stock total: 59 unidades
- Categoria con mas variantes: WHISKY

Archivo preparado para importacion:

```text
apps/inventario_cedhi/datos_iniciales/csv/import_articulos_gastronomia_licores.csv
```

Mapeo:

- `Modulo`: Gastronomia
- `Grupo`: LICORES
- `Categoria`: tipo de licor
- `Marca`: marca del Excel
- `Nombre del articulo`: tipo de licor + marca
- `Stock actual`: cantidad
- `Cantidad`: no se usa para Gastronomia; queda reservada para activos fisicos de TI/General
- `Unidad de medida`: U
- `Es perecible`: No
- `Estado`: Activo
- `Ubicacion` y `Asignacion`: Cocina Principal
- `Fuente de datos`, `Hoja origen` y `Numero origen`: trazabilidad de importacion

Estado de carga en Frappe:

- Importado correctamente: 41 registros
- Fuente marcada en Frappe: `INVENTARIO DE LICORES.xlsx`

## Estado actual de carga

Total de registros en `Articulo de Inventario`: 1153

Por fuente:

- `lista de insumos gastronomia.xlsx`: 882
- `3. SALA DE COMPUTO.xlsx`: 227
- `INVENTARIO DE LICORES.xlsx`: 41
- Registros manuales previos: 3

Por modulo:

- Gastronomia: 924
- TI: 228
- General: 1

## 2do TECNICAS 2

Este archivo no debe entrar al MVP como carga principal, segun indicacion de la profesora.

Uso recomendado:

```text
Feature futuro: kardex diario / pedidos por clase / consumo por curso.
```

Estructura observada:

- Hojas de diseno y pedidos por sesion (`P1`, `P2`, etc.)
- Hoja `INSUMOS`, muy similar al catalogo maestro de gastronomia
- Hoja `CODIGOS`
- Aproximadamente 412 filas de pedidos en hojas `P*`
- Aproximadamente 119 insumos unicos usados en pedidos

Campos utiles para un futuro DocType `Pedido de Cocina` o `Movimiento Kardex`:

- Curso
- Chef
- Tema
- Pedido/sesion
- Insumo
- Unidad
- Cantidad
- Precio
- Observaciones
- Total

## Implicancia para Frappe

No se recomienda insertar datos directamente en MariaDB. Frappe ya usa MariaDB por debajo, pero la carga debe hacerse mediante DocTypes/importaciones para respetar validaciones, permisos y estructura.

DocTypes actuales:

- `Ubicacion`
- `Asignacion`
- `Articulo de Inventario`

Ajustes recomendados para `Articulo de Inventario`:

- `Stock actual`
- `Stock critico`
- `Unidad de medida`
- `Es perecible`
- `Fecha de vencimiento`
- `Grupo`
- `Categoria`
- `Proveedor de referencia`
- `Presentacion`
- `Precio referencial`
- `% Desperdicio`

Estado actual: estos campos ya fueron agregados al DocType `Articulo de Inventario`.

Para el MVP, los campos indispensables son:

- Nombre del articulo
- Modulo
- Ubicacion
- Estado
- Unidad de medida
- Stock actual
- Stock critico
- Es perecible

Nota sobre `Cantidad` vs `Stock actual`:

- Para Gastronomia, la cantidad disponible se guarda en `Stock actual`.
- Para TI/General, `Cantidad` conserva el valor de cantidad del Excel, aunque normalmente cada fila representa un activo fisico individual.
- El formulario oculta `Cantidad` cuando `Modulo` es `Gastronomia` para evitar duplicidad visual.
