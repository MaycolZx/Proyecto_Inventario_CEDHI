import frappe


ADMIN_ALERT_ROLES = {
	"Administrator",
	"System Manager",
	"SuperAdministrador Inventario",
	"Admin TI",
	"Admin Cocina",
	"Admin General",
}


def set_alert_defaults(doc, method=None):
	"""Set reporting defaults and keep reporter-created alerts in report state."""
	if doc.articulo:
		article = frappe.db.get_value(
			"Articulo de Inventario",
			doc.articulo,
			["modulo", "ubicacion"],
			as_dict=True,
		)
		if article:
			doc.modulo = article.modulo
			doc.ubicacion = article.ubicacion

	if not doc.reportado_por:
		doc.reportado_por = frappe.session.user

	if not doc.fecha_reporte:
		doc.fecha_reporte = frappe.utils.today()

	if _is_reporter_only():
		doc.estado_alerta = "Pendiente"
		doc.accion_tomada = None
		doc.fecha_resolucion = None


def _is_reporter_only():
	if frappe.session.user == "Administrator":
		return False

	roles = set(frappe.get_roles(frappe.session.user))
	return "Reportante" in roles and not roles & ADMIN_ALERT_ROLES
