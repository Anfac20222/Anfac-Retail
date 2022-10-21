import frappe

@frappe.whitelist()
def create_inv(doc_name , is_credit = 0 , lab_ref = ''):
    order_doc = frappe.get_doc("Order" , doc_name)
    customer = frappe.db.get_value("Patient" , order_doc.patient , "customer")
    # frappe.msgprint(order_doc.name)
    items = []
    empty_items = ""
    for item in order_doc.order_items:
        item_qty = frappe.db.get_value("Batch" , {"item" :item.item  }, "batch_qty" )
        if float(item_qty) <= 0 :
            empty_items += item.item + ' , '
        #     frappe.throw(
        #     title='Ogerysiis',
            
        #     exc=FileNotFoundError
        # )
        items.append({
            "item_code" : item.item,
            "rate" : item.rate,
            "qty" : item.qty
        })
    payments = []
    # is_pos = 0
    # if not is_credit:
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
        "is_pos" : 1,
       
        "payments": payments,
       
        "items" : items,
        "lab_ref" : lab_ref
    })
    if empty_items:
        frappe.throw(
            title='Ogerysiis',
             msg= f'<b>{empty_items}</b>' + 'Tirada dalabka kuma filna Faldan iska sax',
            
           
        )
        return
    sales_doc.insert()
    sales_doc.submit()
    frappe.msgprint('Billed successfully')