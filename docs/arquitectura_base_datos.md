# Arquitectura de Base de Datos

## Enfoque general

El proyecto usa Frappe/ERPNext sobre MariaDB.

En Frappe, la base de datos no se disena creando tablas manualmente desde cero. La arquitectura se define principalmente mediante **DocTypes**. Cada DocType genera una tabla en MariaDB con el prefijo `tab`.

Ejemplo:

```text
DocType: Articulo de Inventario
Tabla MariaDB: tabArticulo de Inventario
```

Los datos reales no viven en GitHub ni dentro de la carpeta `apps/inventario_cedhi`. Viven en MariaDB, en la base asociada al sitio:

```text
sites/inventario.local
```

El archivo `sites/inventario.local/site_config.json` solo contiene credenciales y configuracion de conexion, no contiene los datos.

## Capas de la arquitectura

```text
Usuario / Navegador
        |
        v
Interfaz Frappe Desk
        |
        v
DocTypes, permisos, validaciones y hooks
        |
        v
ORM / API de Frappe
        |
        v
MariaDB
```

## Tablas principales

### Articulo de Inventario

Tabla:

```text
tabArticulo de Inventario
```

Es la tabla central del sistema. Guarda los bienes, insumos y activos del inventario.

Campos principales:

- `name`: identificador interno de Frappe.
- `nombre_articulo`: nombre visible del articulo.
- `descripcion`: descripcion general.
- `modulo`: TI, Gastronomia o General.
- `ubicacion`: enlace a `Ubicacion`.
- `asignacion`: enlace a `Asignacion`.
- `estado`: Activo o Inactivo.
- `fecha_adquisicion`.
- `marca`, `modelo`, `codigo_interno`: usados principalmente en TI.
- `stock_actual`, `stock_critico`, `unidad_medida`, `es_perecible`, `fecha_vencimiento`: usados principalmente en Gastronomia.
- `pabellon`, `aula`: usados principalmente en General.
- `fuente_datos`, `hoja_origen`, `numero_origen`: trazabilidad de importacion.

Cantidad actual de registros:

```text
Gastronomia: 924
TI: 227
General: 1
```

### Ubicacion

Tabla:

```text
tabUbicacion
```

Representa lugares fisicos donde se encuentran articulos.

Ejemplos:

- Laboratorio de computo.
- Almacen Soldadura.
- Cocina Principal.
- Aula General 201.

Campos principales:

- `name`: identificador interno.
- `nombre_ubicacion`: nombre visible.
- `modulo`: TI, Gastronomia o General.
- `pabellon`.
- `aula`.
- `activo`.

### Asignacion

Tabla:

```text
tabAsignacion
```

Representa el responsable, area o destino funcional asociado a un articulo.

Campos principales:

- `name`.
- `nombre_asignacion`.
- `modulo`.
- `activo`.

### Alerta de Inventario

Tabla:

```text
tabAlerta de Inventario
```

Registra incidencias, reportes o avisos creados por usuarios reportantes.

Campos principales:

- `articulo`: enlace a `Articulo de Inventario`.
- `tipo_alerta`: Stock bajo, Danado, Perdido, Vencido, Ajuste de stock u Otro.
- `modulo`: se obtiene desde el articulo.
- `ubicacion`: se obtiene desde el articulo.
- `estado_alerta`: Pendiente, Verificado, Ajustado o Rechazado.
- `fecha_reporte`.
- `reportado_por`: usuario que crea la alerta.
- `observacion`.
- `accion_tomada`.
- `fecha_resolucion`.

### User

Tabla:

```text
tabUser
```

Es una tabla estandar de Frappe. Se usa para usuarios del sistema.

Se agregaron campos personalizados para usuarios reportantes:

- `inventario_modulo_asignado`.
- `inventario_ubicacion_asignada`.

Esto permite que un punto de reporte, por ejemplo una PC del laboratorio de computo, solo pueda crear alertas sobre articulos de su ubicacion.

Ejemplo:

```text
Usuario: lab.computacion01@cedhi.local
Rol: Reportante
Modulo asignado: TI
Ubicacion asignada: Laboratorio de computo
```

## Relaciones principales

```text
Ubicacion 1 ──── * Articulo de Inventario

Asignacion 1 ──── * Articulo de Inventario

Articulo de Inventario 1 ──── * Alerta de Inventario

Ubicacion 1 ──── * Alerta de Inventario

User 1 ──── * Alerta de Inventario
```

Diagrama textual:

```text
tabUbicacion
  name
  nombre_ubicacion
        ^
        |
        | ubicacion
        |
tabArticulo de Inventario
  name
  nombre_articulo
  modulo
  ubicacion
  asignacion
        ^
        |
        | articulo
        |
tabAlerta de Inventario
  name
  articulo
  modulo
  ubicacion
  reportado_por
        |
        | reportado_por
        v
tabUser
  name
  full_name
  inventario_modulo_asignado
  inventario_ubicacion_asignada
```

## Seguridad y permisos

La seguridad no depende solo de MariaDB. Se aplica desde Frappe usando:

- Roles.
- DocPerms.
- Hooks de permisos en `inventario_cedhi/permissions.py`.
- Eventos de documento en `inventario_cedhi/alerts.py`.

Roles principales:

- `SuperAdministrador Inventario`: acceso total al inventario.
- `Admin TI`: gestiona articulos y alertas de TI.
- `Admin Cocina`: gestiona articulos y alertas de Gastronomia.
- `Admin General`: edita General y puede visualizar otros modulos.
- `Revisor`: lectura.
- `Reportante`: crea alertas desde una ubicacion asignada.

## Como ver la base de datos

Entrar a MariaDB desde el bench:

```bash
cd /home/anthonybq/frappe/my-bench
bench --site inventario.local mariadb
```

Comandos utiles dentro de MariaDB:

```sql
select database();
show tables like 'tabArticulo%';
show tables like 'tabUbicacion%';
show tables like 'tabAlerta%';
```

Consultar articulos:

```sql
select
  name,
  nombre_articulo,
  modulo,
  estado
from `tabArticulo de Inventario`
limit 10;
```

Contar articulos por modulo:

```sql
select
  modulo,
  count(*) as total
from `tabArticulo de Inventario`
group by modulo;
```

Ver articulos por ubicacion:

```sql
select
  u.nombre_ubicacion,
  a.modulo,
  count(*) as total
from `tabArticulo de Inventario` a
left join `tabUbicacion` u on u.name = a.ubicacion
group by u.nombre_ubicacion, a.modulo
order by a.modulo, u.nombre_ubicacion;
```

## Importante para GitHub

GitHub contiene:

- Codigo de la app.
- Scripts de configuracion.
- CSV/Excel fuente.
- Documentacion.

GitHub no contiene:

- La base MariaDB.
- Usuarios creados localmente.
- Articulos ya importados en el sitio local.
- Contrasenas o sesiones.

Para que otro integrante tenga datos, debe importar los CSV o restaurar un backup de la base.
