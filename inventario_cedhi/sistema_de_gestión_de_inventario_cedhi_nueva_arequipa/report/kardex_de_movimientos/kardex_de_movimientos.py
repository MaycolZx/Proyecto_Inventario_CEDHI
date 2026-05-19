import frappe
from frappe import _

from inventario_cedhi.permissions import article_report_condition


def execute(filters=None):
	filters = frappe._dict(filters or {})
	return get_columns(), get_data(filters)


def get_columns():
	return [
		{
			"label": _("Movimiento"),
			"fieldname": "name",
			"fieldtype": "Link",
			"options": "Movimiento de Inventario",
			"width": 170,
		},
		{"label": _("Fecha"), "fieldname": "fecha", "fieldtype": "Date", "width": 110},
		{"label": _("Tipo"), "fieldname": "tipo_movimiento", "fieldtype": "Data", "width": 100},
		{"label": _("Cantidad"), "fieldname": "cantidad", "fieldtype": "Float", "width": 100},
		{
			"label": _("Articulo"),
			"fieldname": "articulo",
			"fieldtype": "Link",
			"options": "Articulo de Inventario",
			"width": 160,
		},
		{"label": _("Nombre articulo"), "fieldname": "nombre_articulo", "fieldtype": "Data", "width": 220},
		{"label": _("Modulo"), "fieldname": "modulo", "fieldtype": "Data", "width": 110},
		{
			"label": _("Ubicacion"),
			"fieldname": "ubicacion",
			"fieldtype": "Link",
			"options": "Ubicacion",
			"width": 150,
		},
		{"label": _("Estado actual"), "fieldname": "estado_actual", "fieldtype": "Data", "width": 120},
		{"label": _("Stock actual"), "fieldname": "stock_actual_articulo", "fieldtype": "Float", "width": 120},
		{
			"label": _("Responsable"),
			"fieldname": "responsable",
			"fieldtype": "Link",
			"options": "User",
			"width": 180,
		},
		{"label": _("Motivo"), "fieldname": "motivo", "fieldtype": "Data", "width": 260},
	]


def get_data(filters):
	conditions = [article_report_condition(table_alias="art")]
	values = {}

	if filters.get("modulo"):
		conditions.append("art.modulo = %(modulo)s")
		values["modulo"] = filters.modulo
	if filters.get("ubicacion"):
		conditions.append("art.ubicacion = %(ubicacion)s")
		values["ubicacion"] = filters.ubicacion
	if filters.get("articulo"):
		conditions.append("m.articulo = %(articulo)s")
		values["articulo"] = filters.articulo
	if filters.get("tipo_movimiento"):
		conditions.append("m.tipo_movimiento = %(tipo_movimiento)s")
		values["tipo_movimiento"] = filters.tipo_movimiento
	if filters.get("fecha_desde"):
		conditions.append("m.fecha >= %(fecha_desde)s")
		values["fecha_desde"] = filters.fecha_desde
	if filters.get("fecha_hasta"):
		conditions.append("m.fecha <= %(fecha_hasta)s")
		values["fecha_hasta"] = filters.fecha_hasta

	return frappe.db.sql(
		f"""
		select
			m.name,
			m.fecha,
			m.tipo_movimiento,
			m.cantidad,
			m.articulo,
			art.nombre_articulo,
			art.modulo,
			art.ubicacion,
			coalesce(m.estado_actual, art.estado) as estado_actual,
			coalesce(m.stock_actual_articulo, art.stock_actual) as stock_actual_articulo,
			m.responsable,
			m.motivo
		from `tabMovimiento de Inventario` m
		inner join `tabArticulo de Inventario` art on art.name = m.articulo
		where {" and ".join(conditions)}
		order by m.fecha desc, m.creation desc
		""",
		values,
		as_dict=1,
	)
