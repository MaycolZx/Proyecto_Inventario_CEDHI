
import frappe
from frappe import _
from inventario_cedhi.permissions import article_report_condition

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {
            "label": _("ID"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Articulo de Inventario",
            "width": 140
        },
        {
            "label": _("Articulo"),
            "fieldname": "nombre_articulo",
            "fieldtype": "Data",
            "width": 260
        },
        {
            "label": _("Modulo"),
            "fieldname": "modulo",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("Ubicacion"),
            "fieldname": "ubicacion",
            "fieldtype": "Link",
            "options": "Ubicacion",
            "width": 140
        },
        {
            "label": _("Asignacion"),
            "fieldname": "asignacion",
            "fieldtype": "Link",
            "options": "Asignacion",
            "width": 140
        },
        {
            "label": _("Estado"),
            "fieldname": "estado",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("Stock Actual"),
            "fieldname": "stock_actual",
            "fieldtype": "Float",
            "width": 100
        },
        {
            "label": _("Stock Critico"),
            "fieldname": "stock_critico",
            "fieldtype": "Float",
            "width": 100
        },
        {
            "label": _("Unidad"),
            "fieldname": "unidad_medida",
            "fieldtype": "Data",
            "width": 80
        },
        {
            "label": _("Fecha Adquisicion"),
            "fieldname": "fecha_adquisicion",
            "fieldtype": "Date",
            "width": 110
        },
        {
            "label": _("Marca"),
            "fieldname": "marca",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("Modelo"),
            "fieldname": "modelo",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("Codigo Interno"),
            "fieldname": "codigo_interno",
            "fieldtype": "Data",
            "width": 140
        }
    ]

def get_data(filters):
    conditions = f" and {article_report_condition(table_alias='a')}"
    if filters.get("modulo"):
        conditions += f" and a.modulo = {frappe.db.escape(filters.get('modulo'))}"
    if filters.get("ubicacion"):
        conditions += f" and a.ubicacion = {frappe.db.escape(filters.get('ubicacion'))}"
    if filters.get("estado"):
        conditions += f" and a.estado = {frappe.db.escape(filters.get('estado'))}"
    if filters.get("nombre_articulo"):
        conditions += f" and a.nombre_articulo like {frappe.db.escape('%' + filters.get('nombre_articulo') + '%')}"

    return frappe.db.sql(f"""
        select
            a.name, a.nombre_articulo, a.modulo, a.ubicacion, a.asignacion, a.estado,
            a.stock_actual, a.stock_critico, a.unidad_medida, a.fecha_adquisicion,
            a.marca, a.modelo, a.codigo_interno
        from
            `tabArticulo de Inventario` a
        where
            1=1 {conditions}
        order by
            a.modulo, a.nombre_articulo
    """, as_dict=1)
