import frappe
from frappe import _

from inventario_cedhi.permissions import alert_report_condition


def execute(filters=None):
	filters = frappe._dict(filters or {})
	return get_columns(), get_data(filters)


def get_columns():
	return [
		{
			"label": _("Alerta"),
			"fieldname": "name",
			"fieldtype": "Link",
			"options": "Alerta de Inventario",
			"width": 160,
		},
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
		{"label": _("Tipo"), "fieldname": "tipo_alerta", "fieldtype": "Data", "width": 130},
		{"label": _("Estado"), "fieldname": "estado_alerta", "fieldtype": "Data", "width": 120},
		{"label": _("Fecha reporte"), "fieldname": "fecha_reporte", "fieldtype": "Date", "width": 120},
		{
			"label": _("Reportado por"),
			"fieldname": "reportado_por",
			"fieldtype": "Link",
			"options": "User",
			"width": 180,
		},
		{"label": _("Observacion"), "fieldname": "observacion", "fieldtype": "Data", "width": 280},
		{"label": _("Accion tomada"), "fieldname": "accion_tomada", "fieldtype": "Data", "width": 220},
	]


def get_data(filters):
	conditions = [alert_report_condition(table_alias="al")]
	values = {}

	if filters.get("modulo"):
		conditions.append("al.modulo = %(modulo)s")
		values["modulo"] = filters.modulo
	if filters.get("ubicacion"):
		conditions.append("al.ubicacion = %(ubicacion)s")
		values["ubicacion"] = filters.ubicacion
	if filters.get("tipo_alerta"):
		conditions.append("al.tipo_alerta = %(tipo_alerta)s")
		values["tipo_alerta"] = filters.tipo_alerta
	if filters.get("estado_alerta"):
		conditions.append("al.estado_alerta = %(estado_alerta)s")
		values["estado_alerta"] = filters.estado_alerta
	if filters.get("fecha_desde"):
		conditions.append("al.fecha_reporte >= %(fecha_desde)s")
		values["fecha_desde"] = filters.fecha_desde
	if filters.get("fecha_hasta"):
		conditions.append("al.fecha_reporte <= %(fecha_hasta)s")
		values["fecha_hasta"] = filters.fecha_hasta

	return frappe.db.sql(
		f"""
		select
			al.name,
			al.articulo,
			art.nombre_articulo,
			al.modulo,
			al.ubicacion,
			al.tipo_alerta,
			al.estado_alerta,
			al.fecha_reporte,
			al.reportado_por,
			al.observacion,
			al.accion_tomada
		from `tabAlerta de Inventario` al
		left join `tabArticulo de Inventario` art on art.name = al.articulo
		where {" and ".join(conditions)}
		order by
			case al.estado_alerta
				when 'Pendiente' then 1
				when 'En revision' then 2
				else 3
			end,
			al.fecha_reporte desc,
			al.modified desc
		""",
		values,
		as_dict=1,
	)
