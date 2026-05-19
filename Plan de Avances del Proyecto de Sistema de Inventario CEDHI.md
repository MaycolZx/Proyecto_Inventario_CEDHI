**Plan de Avances del Proyecto de Sistema de Inventario CEDHI**

**Integrantes:**

* Briceño Quiroz Anthony Angel  
* Cayo Villena Daniel Nicolás   
* Guillen Davila Marco Antonio  
* Gomez Ticona Diego Sebastian  
* Mellado Baca Cristian  
* Torres Acuña Marcelo  
* Zeballos Huayna Diego Alonso

1. **Cronograma de Entregas**  
   En esta fase específica, se demuestra que el sistema cuenta con la capacidad técnica y estructural para albergar y organizar la información base del CEDHI, asegurando la integridad de los datos y estableciendo los cimientos para las funcionalidades avanzadas.  
     
   **1.1 Presentación 1 \- 02/05/2026**  
   En esta entrega se demuestra que el sistema ya puede albergar y organizar la información base del CEDHI.  
   **Tabla 1 Entrega 1**

| Identificador | Nombre | Descripción  | Realizado |
| :---- | :---- | :---- | :---- |
| RF-C02 | Gestión de Catálogo Maestro | Capacidad operativa para crear, leer, actualizar y dar de baja artículos con sus campos obligatorios (Nombre, Ubicación, Estado, Fecha de Adquisición). | Si |
| RF-C05 | Gestión de Archivos: | Funcionalidad activa de subida de fotografías para la identificación visual de los productos registrados. | Si |
| RF-GE-03 | Modo Multivista (Solo Lectura) | Capacidad del Director General para supervisar los inventarios de TI y Gastronomía sin riesgo de alterar los datos. | Si |
|  | Gestión de Roles y Capacidades (Seguridad) | Configuración interna de permisos para Administradores, asegurando que cada rol acceda solo a las funciones permitidas según su nivel. | Si |

	**1.2 Presentación 2 \- 15/05/2026**  
El enfoque es resolver la organización del frontend y empezar con el registro de movimientos físicos.  
**Tabla 2 Entrega 2**

| Identificador | Nombre | Descripción  | Realizado |
| :---- | :---- | :---- | :---- |
| RF-C03 | Trazabilidad de Bajas y Reparaciones | Función para marcar artículos como "De Baja" o "En Reparación", solicitando el motivo obligatorio para mantener la integridad del inventario. | En proceso, ver la cantidad de opciones para la trazabilidad de los articulos |
| RF-TI-01 & RF-TI-02  | Módulo TI | Registro de campos técnicos (Marca/Modelo) y visualización especializada por Salones de Cómputo para auditorías rápidas. | Si |
| RF-C07 | Importación Masiva | Herramienta de carga inicial mediante plantillas Excel para migrar los inventarios actuales de los módulos de manera masiva. | Si |
|  | Optimización de Navegación y UX (No Funcional) | Mejora de la fluidez en las rutas del Superadmin (Definiciones). Reducción de tiempos de carga para evitar confusiones y mejorar la respuesta de la interfaz "Responsive". | Si |

	**1.3 Presentación 3 \- 22/05/2026**  
En la entrega final se presentan las herramientas de supervisión y los entregables de salida.  
**Tabla 3 Entrega 3**

| Identificador | Nombre | Descripción  |
| :---- | :---- | :---- |
| RF-C06 | Motor de Reportes y Exportación | Generación de reportes filtrados por ubicación, estado o fecha, exportables a formato Microsoft Excel (.xlsx). |
|  | Sistema de Inspecciones y Revisiones | Implementación de la lógica de "Verificar y Ajustar Stock" tras las inspecciones de materiales pendientes. |
| MK-007 | Bandeja Central de Alertas y Reportes | Interfaz donde el administrador recibe y resuelve los reportes de daños o pérdidas enviados por los docentes. |
| RF-C04 | Dashboard de Resumen | Pantalla de inicio con indicadores clave (KPIs) dinámicos que muestran el estado global del inventario según el rol del usuario. |
| RF-GE-02 | Generador de Código Interno | Asignación automática de códigos únicos para mobiliario nuevo que no posea codificación previa. |
| RF-GA-01 | Kardex Digital (Cocina) | Sustitución final del formato manual de 700 productos por la actualización rápida de existencias en el flujo diario de gastronomía. |
| RF-C01 | Autenticación vía Google Workspace | Integración final del acceso exclusivo mediante cuentas institucionales de Google, eliminando registros externos. |

