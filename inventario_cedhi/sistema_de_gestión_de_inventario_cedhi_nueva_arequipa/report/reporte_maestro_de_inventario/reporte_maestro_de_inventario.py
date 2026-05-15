
import frappe
from frappe import _

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
    conditions = ""
    if filters.get("modulo"):
        conditions += f" and modulo = {frappe.db.escape(filters.get('modulo'))}"
    if filters.get("ubicacion"):
        conditions += f" and ubicacion = {frappe.db.escape(filters.get('ubicacion'))}"
    if filters.get("estado"):
        conditions += f" and estado = {frappe.db.escape(filters.get('estado'))}"
    if filters.get("nombre_articulo"):
        conditions += f" and nombre_articulo like {frappe.db.escape('%' + filters.get('nombre_articulo') + '%')}"

    return frappe.db.sql(f"""
        select
            name, nombre_articulo, modulo, ubicacion, asignacion, estado,
            stock_actual, stock_critico, unidad_medida, fecha_adquisicion,
            marca, modelo, codigo_interno
        from
            `tabArticulo de Inventario`
        where
            1=1 {conditions}
        order by
            modulo, nombre_articulo
    """, as_dict=1)
