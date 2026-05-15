
import frappe
from frappe import _


def set_internal_code(doc, method=None):
    """RF-GE-02: Automatically assign a unique internal code for General furniture."""
    if doc.modulo == "General" and not doc.codigo_interno:
        # Generate a simple unique code based on year and count
        year = frappe.utils.nowdate()[:4]
        prefix = f"INV-GEN-{year}-"
        
        # Get count of general articles this year
        count = frappe.db.count("Articulo de Inventario", {
            "modulo": "General",
            "codigo_interno": ["like", f"{prefix}%"]
        })
        
        doc.codigo_interno = f"{prefix}{str(count + 1).zfill(4)}"

def update_stock_on_movement(doc, method=None):
    """Update stock_actual in Articulo de Inventario when a movement is submitted."""
    if not doc.articulo:
        return

    articulo = frappe.get_doc("Articulo de Inventario", doc.articulo)
    
    # Calculate adjustment
    adjustment = doc.cantidad
    if doc.tipo_movimiento == "Salida":
        adjustment = -adjustment
        
    # Check if we have enough stock for "Salida" (optional but recommended)
    if doc.tipo_movimiento == "Salida" and (articulo.stock_actual or 0) < doc.cantidad:
        # We allow it but maybe send a message? PRD doesn't forbid negative stock but it's good to know.
        pass

    new_stock = (articulo.stock_actual or 0) + adjustment
    
    # Update the article
    articulo.db_set("stock_actual", new_stock)
    
    # Log the change in the article's comments/timeline
    articulo.add_comment("Comment", _("Stock actualizado a {0} ({1} por {2})").format(
        new_stock, doc.tipo_movimiento, doc.name
    ))

def reverse_stock_on_cancel(doc, method=None):
    """Reverse the stock update if a movement is cancelled."""
    if not doc.articulo:
        return

    articulo = frappe.get_doc("Articulo de Inventario", doc.articulo)
    
    # Calculate reverse adjustment
    adjustment = doc.cantidad
    if doc.tipo_movimiento == "Entrada":
        adjustment = -adjustment
        
    new_stock = (articulo.stock_actual or 0) + adjustment
    articulo.db_set("stock_actual", new_stock)
    
    articulo.add_comment("Comment", _("Movimiento {0} cancelado. Stock revertido a {1}").format(
        doc.name, new_stock
    ))
