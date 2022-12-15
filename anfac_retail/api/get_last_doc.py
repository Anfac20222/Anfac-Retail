import frappe

@frappe.whitelist()
def get_last_doc(doc):
   
    try:
        # frappe.get_last_doc(doc)
        doc_type = frappe.get_last_doc(doc)
        # frappe.msgprint(doc.reciept_no)
        if doc == "Sales Invoice":
            return doc_type.invocie_no
        elif doc == "Payment Entry":
            return doc_type.reciept_no
        else:
            return doc_type.voucher_no

    except:
        return 1
