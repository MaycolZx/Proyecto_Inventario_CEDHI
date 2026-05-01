import frappe


SYSTEM_ACCESS_ROLES = {"Administrator", "System Manager"}
INVENTORY_SUPERADMIN_ROLE = "SuperAdministrador Inventario"
REPORTER_ROLE = "Reportante"
FULL_ACCESS_ROLES = SYSTEM_ACCESS_ROLES | {INVENTORY_SUPERADMIN_ROLE}
MODULE_WRITE_ACCESS = {
	"Admin TI": {"TI"},
	"Admin Cocina": {"Gastronomia"},
	"Admin General": {"General"},
}
READ_ALL_ROLES = FULL_ACCESS_ROLES | {"Admin General", "Revisor"}
LIMITED_USER_ROLES = {"Admin TI", "Admin Cocina", "Admin General", "Revisor", REPORTER_ROLE}
INVENTORY_USER_ROLES = LIMITED_USER_ROLES | {INVENTORY_SUPERADMIN_ROLE}


def _user_roles(user=None):
	user = user or frappe.session.user
	if user == "Administrator":
		return {"Administrator"}
	return set(frappe.get_roles(user))


def _allowed_modules_for_read(user=None):
	roles = _user_roles(user)
	if roles & READ_ALL_ROLES:
		return None

	modules = set()
	for role, role_modules in MODULE_WRITE_ACCESS.items():
		if role in roles:
			modules.update(role_modules)
	return modules


def _allowed_modules_for_write(user=None):
	roles = _user_roles(user)
	if roles & FULL_ACCESS_ROLES:
		return None

	modules = set()
	for role, role_modules in MODULE_WRITE_ACCESS.items():
		if role in roles:
			modules.update(role_modules)
	return modules


def _module_condition(doctype, modules):
	if modules is None:
		return None
	if not modules:
		return "1=0"

	escaped_modules = ", ".join(frappe.db.escape(module) for module in sorted(modules))
	return f"`tab{doctype}`.`modulo` in ({escaped_modules})"


def article_query_conditions(user=None):
	roles = _user_roles(user)
	if REPORTER_ROLE in roles:
		return None
	return _module_condition("Articulo de Inventario", _allowed_modules_for_read(user))


def alert_query_conditions(user=None):
	user = user or frappe.session.user
	roles = _user_roles(user)
	if REPORTER_ROLE in roles and not roles & (FULL_ACCESS_ROLES | set(MODULE_WRITE_ACCESS) | {"Admin General", "Revisor"}):
		return f"`tabAlerta de Inventario`.`reportado_por` = {frappe.db.escape(user)}"
	return _module_condition("Alerta de Inventario", _allowed_modules_for_read(user))


def user_query_conditions(user=None):
	user = user or frappe.session.user
	roles = _user_roles(user)
	if roles & SYSTEM_ACCESS_ROLES:
		return None
	if INVENTORY_SUPERADMIN_ROLE in roles:
		inventory_roles = ", ".join(frappe.db.escape(role) for role in sorted(INVENTORY_USER_ROLES))
		system_roles = ", ".join(frappe.db.escape(role) for role in sorted(SYSTEM_ACCESS_ROLES))
		return f"""
			exists (
				select 1
				from `tabHas Role`
				where `tabHas Role`.`parent` = `tabUser`.`name`
				  and `tabHas Role`.`role` in ({inventory_roles})
			)
			and not exists (
				select 1
				from `tabHas Role`
				where `tabHas Role`.`parent` = `tabUser`.`name`
				  and `tabHas Role`.`role` in ({system_roles})
			)
		"""
	if roles & LIMITED_USER_ROLES:
		return f"`tabUser`.`name` = {frappe.db.escape(user)}"
	return None


def article_has_permission(doc, ptype=None, user=None):
	ptype = ptype or "read"
	roles = _user_roles(user)
	if REPORTER_ROLE in roles:
		return ptype in {"read", "select", "print", "report"}
	return _has_inventory_module_permission(doc, ptype, user)


def alert_has_permission(doc, ptype=None, user=None):
	ptype = ptype or "read"
	user = user or frappe.session.user
	roles = _user_roles(user)
	if REPORTER_ROLE in roles and not roles & (FULL_ACCESS_ROLES | set(MODULE_WRITE_ACCESS) | {"Admin General", "Revisor"}):
		if ptype == "create":
			return True
		if ptype in {"read", "write", "select", "print"}:
			return bool(doc and doc.reportado_por == user)
		return False
	return _has_inventory_module_permission(doc, ptype, user)


def user_has_permission(doc, ptype=None, user=None):
	user = user or frappe.session.user
	roles = _user_roles(user)
	if roles & SYSTEM_ACCESS_ROLES:
		return True
	if INVENTORY_SUPERADMIN_ROLE in roles:
		if not doc:
			return True
		target_roles = set(frappe.get_roles(doc.name))
		return bool(target_roles & INVENTORY_USER_ROLES) and not bool(target_roles & SYSTEM_ACCESS_ROLES)
	if roles & LIMITED_USER_ROLES:
		return bool(doc and doc.name == user)
	return True


def _has_inventory_module_permission(doc, ptype=None, user=None):
	if ptype in {"read", "select", "print", "email", "report", "export"}:
		modules = _allowed_modules_for_read(user)
	else:
		modules = _allowed_modules_for_write(user)

	if modules is None:
		return True

	if not doc:
		return bool(modules)

	doc_module = getattr(doc, "modulo", None)
	if not doc_module:
		return bool(modules)

	return doc_module in modules
