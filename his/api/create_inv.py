import frappe

@frappe.whitelist()
def create_inv(doc_name , is_credit = 0):
    order_doc = frappe.get_doc("Order" , doc_name)
    customer = frappe.db.get_value("Patient" , order_doc.patient , "customer")
    # frappe.msgprint(order_doc.name)
    items = []
    for item in order_doc.order_items:
        items.append({
            "item_code" : item.item,
            "rate" : item.rate,
            "qty" : item.qty
        })
    payments = []
    is_pos = 0
    if not is_credit:
        b =frappe.defaults.get_user_permissions(frappe.session.user)
        pos =b['POS Profile'][0].doc
        pos = frappe.get_doc("POS Profile" , pos)
        # payment = pos.payments
        
        for mode in pos.payments:
            payments.append(
                    {
                        "mode_of_payment" : mode.mode_of_payment,
                        "amount" : order_doc.grand_total
                    }
                )
   
    sales_doc = frappe.get_doc({
        "doctype" : "Sales Invoice",
        "patient" : order_doc.patient,
        "customer": customer,
        "is_pos" : is_pos,
       
        "payments": payments,
       
        "items" : items
    })
    sales_doc.insert()
    sales_doc.submit()
    frappe.msgprint('Billed successfully')