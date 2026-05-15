
frappe.query_reports["Reporte Maestro de Inventario"] = {
	"filters": [
		{
			"fieldname": "modulo",
			"label": __("Módulo"),
			"fieldtype": "Select",
			"options": "\nTI\nGastronomia\nGeneral",
		},
		{
			"fieldname": "ubicacion",
			"label": __("Ubicación"),
			"fieldtype": "Link",
			"options": "Ubicacion",
		},
		{
			"fieldname": "estado",
			"label": __("Estado"),
			"fieldtype": "Select",
			"options": "\nActivo\nDe baja\nEn reparación",
		},
		{
			"fieldname": "nombre_articulo",
			"label": __("Nombre del Artículo"),
			"fieldtype": "Data",
		}
	]
};
