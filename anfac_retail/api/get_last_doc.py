import frappe

@frappe.whitelist()
def get_last_doc(doc = "Sales Invoice"):
    try:
        # frappe.get_last_doc("Task")
        doc = frappe.get_last_doc(doc)
        return doc.invoice_no
    except:
        return 1
