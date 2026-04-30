# Sistema de Inventario CEDHI Nueva Arequipa

Aplicacion Frappe/ERPNext para gestionar el inventario del CEDHI Nueva Arequipa. El MVP organiza articulos por modulo:

- TI
- Gastronomia
- General

El proyecto incluye carga inicial desde Excel/CSV, roles del PRD, permisos por modulo, reportes iniciales y un workspace de trabajo dentro de Frappe.

## Que se sube a este repo

Este repositorio contiene solo la app custom:

```text
apps/inventario_cedhi
```

No se debe subir todo `my-bench`. Las carpetas `env`, `sites`, `logs`, `config`, `apps/frappe` y `apps/erpnext` son parte de la instalacion local o dependencias externas.

## Requisitos

- Frappe Bench instalado
- ERPNext instalado en el bench
- Python, Node, Redis y MariaDB configurados segun la guia oficial de Frappe/ERPNext

## Instalacion en un bench existente

Desde la carpeta del bench:

```bash
cd ~/frappe/my-bench
bench get-app https://github.com/aaabriceno/Proyecto_Inventario_CEDHI.git --branch develop
bench --site inventario.local install-app inventario_cedhi
```

Si el sitio todavia no existe, primero crear e instalar ERPNext:

```bash
bench new-site inventario.local
bench --site inventario.local install-app erpnext
bench --site inventario.local install-app inventario_cedhi
```

## Configuracion inicial del MVP

Ejecutar estos comandos desde la raiz del bench:

```bash
bench --site inventario.local execute inventario_cedhi.setup_inventory.add_gastronomy_catalog_fields
bench --site inventario.local execute inventario_cedhi.setup_inventory.add_import_traceability_fields
bench --site inventario.local execute inventario_cedhi.setup_inventory.configure_module_specific_article_form
bench --site inventario.local execute inventario_cedhi.setup_inventory.create_alerta_inventario_doctype
bench --site inventario.local execute inventario_cedhi.setup_inventory.create_basic_inventory_reports
bench --site inventario.local execute inventario_cedhi.setup_inventory.configure_inventory_list_views
bench --site inventario.local execute inventario_cedhi.setup_inventory.create_inventory_workspace
bench --site inventario.local execute inventario_cedhi.setup_inventory.configure_inventory_role_permissions
bench --site inventario.local clear-cache
```

Si `bench start` estaba corriendo, reiniciarlo despues de cambios en `hooks.py`.

## Datos iniciales

Los Excel originales estan en:

```text
datos_iniciales/
```

Los CSV preparados para importar estan en:

```text
datos_iniciales/csv/
```

Archivos principales:

- `import_articulos_gastronomia.csv`
- `import_articulos_gastronomia_licores.csv`
- `import_articulos_ti_sala_computo.csv`

La importacion se realiza desde Frappe en:

```text
Importacion de Datos
```

Tipo de documento:

```text
Articulo de Inventario
```

Tipo de importacion:

```text
Insertando nuevos registros
```

No usar archivos dentro de `sites/inventario.local/private/files` como fuente del repo. Esos son archivos locales cargados en un sitio.

## Roles del sistema

Roles definidos para el MVP:

- `SuperAdministrador Inventario`: acceso total al inventario y usuarios del proyecto.
- `Admin TI`: gestiona solo articulos del modulo TI.
- `Admin Cocina`: gestiona solo articulos del modulo Gastronomia.
- `Admin General`: edita General y puede visualizar los otros modulos.
- `Revisor`: solo lectura.

Las reglas por modulo estan en:

```text
inventario_cedhi/permissions.py
```

Los hooks de permisos estan en:

```text
inventario_cedhi/hooks.py
```

## Usuarios de prueba

Para pruebas locales se pueden crear usuarios desde Frappe y asignarles roles. Como los correos `@cedhi.local` no existen realmente, la contrasena temporal se puede establecer desde consola:

```bash
bench --site inventario.local execute frappe.utils.password.update_password --args '["usuario@cedhi.local", "Cedhi12345"]'
```

No guardar contrasenas reales en codigo ni en documentacion.

## Reportes y workspace

Workspace:

```text
Inventario CEDHI
```

Reportes iniciales:

- `Resumen Inventario por Modulo`
- `Stock Critico Gastronomia`
- `Inventario TI por Ubicacion`
- `Gastronomia sin Stock Critico`

## Flujo de trabajo con Git

La rama compartida principal del proyecto es:

```bash
develop
```

Antes de trabajar:

```bash
git checkout develop
git pull
```

Crear una rama por tarea:

```bash
git checkout -b feature/nombre-de-la-tarea
```

Ejemplos:

```text
feature/dashboard-inventario
feature/alertas-stock
feature/reportes-gastronomia
feature/documentacion-video
```

Al terminar:

```bash
git add .
git commit -m "Descripcion breve del cambio"
git push -u origin feature/nombre-de-la-tarea
```

Luego abrir un Pull Request hacia `develop`.

## Documentacion del proyecto

- `docs/guia_inicio_proyecto.md`
- `docs/analisis_datos_iniciales.md`
- `PRD_ Sistema de Inventario Integral1.pdf`
- `Defincion MVP  Proyecto de Prácticas Sociales ABS 2026-01 (1).pdf`

## Licencia

MIT
