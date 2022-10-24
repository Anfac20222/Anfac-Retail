import frappe

@frappe.whitelist()
def create_inv(doc_name ,dt , is_sales_return = False , is_credit = False):
    cash_sales = frappe.get_doc(dt , doc_name)
    customer = cash_sales.customer
    # frappe.msgprint(order_doc.name)
    items = []
    empty_items = ""
    for item in cash_sales.items:
        # item_qty = frappe.db.get_value("Batch" , {"item" :item.item  }, "batch_qty" )
        # if float(item_qty) <= 0 :
        #     empty_items += item.item + ' , '
        # #     frappe.throw(
        # #     title='Ogerysiis',
            
        # #     exc=FileNotFoundError
        # # )
        qty = item.qty
        if is_sales_return:
            qty = float(item.qty) * (-1)
        items.append({
            "item_code" : item.item,
            "rate" : item.rate,
            "qty" : qty
        })
    payments = []
    # is_pos = 0
    # if not is_credit:
    # b =frappe.defaults.get_user_permissions(frappe.session.user)
    # pos =b['POS Profile'][0].doc
    # pos = frappe.get_doc("POS Profile" , pos)
    # payment = pos.payments
    
    paid_amount = cash_sales.grand_total
    if is_sales_return:
        paid_amount = cash_sales.grand_total * (-1)
    is_pos = 0
    if not is_credit:
        is_pos = 1
        payments.append(
                {
                    "mode_of_payment" : "Cash",
                    "amount" : cash_sales.grand_total
                    
                }
            )
    is_return = 0
    if is_sales_return :
         is_return = 1 

    sales_doc = frappe.get_doc({
        "doctype" : "Sales Invoice",
        "is_return" : is_return,
        "customer": customer,
        "is_pos" : is_pos,
        "discount_amount" : cash_sales.discount,
        "payments": payments,
       
        "items" : items,
       
    })
   
    sales_doc.insert()
    sales_doc.submit()
    frappe.msgprint('Billed successfully')
    return sales_doc
    # cash_sales.sales_invoice = sales_doc.name
    # cash_sales.save()
    
    