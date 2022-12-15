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
                    "amount" : paid_amount
                    
                }
            )
    is_return = 0
    if is_sales_return :
         is_return = 1 
    sales_doc = frappe.get_doc({
        "doctype" : "Sales Invoice",
        "is_return" : is_return,
        "posting_date" : cash_sales.date,
        "customer": customer,
        "is_pos" : is_pos,
        "discount_amount" : cash_sales.discount,
        "payments": payments,
        "voucher_no" : doc_name,
        "items" : items,
       
    })
   
    sales_doc.insert()
    sales_doc.submit()
    frappe.msgprint('Billed successfully')
    return sales_doc
    # cash_sales.sales_invoice = sales_doc.name
    # cash_sales.save()
    
    




def purchase(doc_name ,dt , is_purchase_return = False , is_credit = False):
    cash_sales = frappe.get_doc(dt , doc_name)
    supplier = cash_sales.supplier
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
        if is_purchase_return:
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
    if is_purchase_return:
        paid_amount = cash_sales.grand_total * (-1)
    is_paid = 0
    account = ''
    if not is_credit:
        is_paid = 1
        account = cash_sales.account
        
                    
        
                    
          
    is_return = 0
    if is_purchase_return :
         is_return = 1 
    frappe.msgprint(str(cash_sales.date))
    pur_doc = frappe.get_doc({
        "doctype" : "Purchase Invoice",
        "posting_date" : cash_sales.date,
        "is_return" : is_return,
        "supplier": supplier,
        "discount_amount" : cash_sales.discount,
        "is_paid" : is_paid,
        "discount_amount" : cash_sales.discount,
        "cash_bank_account" : account,
        "paid_amount" : paid_amount,
        "bill_no" : cash_sales.supplier_invoice,
        # "payments": payments,
        "voucher_no" : doc_name,
       
        "items" : items,
       
    })
   
    pur_doc.save()
    pur_doc.submit()
    frappe.msgprint('Billed successfully')
    return pur_doc
    # cash_sales.sales_invoice = sales_doc.name
    # cash_sales.save()
    
    
