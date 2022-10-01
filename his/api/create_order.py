import frappe
@frappe.whitelist()
def create_order(doc , method = None):
    order = frappe.db.exists("Order", doc.service, cache=True)
    if not order:
        # frappe.msgprint(doc.service)
        orders =  ['drug_prescription' , 'lab_test_prescription' ,'procedure_prescription']
        for order in orders:
            if order == 'drug_prescription' :
                if doc.drug_prescription
                    create_drug(doc)
            if order == 'lab_test_prescription':
                if doc.lab_test_prescription:
                    create_service(doc , order)
    else:
        update_order(doc , order)

def update_order(doc , method = None):
    items = []
    if doc.lab_test_prescription:
        order_doc = frappe.get_doc("Order" , doc.service)
        for item in doc.lab_test_prescription:
            template = frappe.get_doc('Lab Test Template' , item.lab_test_code)
            items.append(
                    {
                        'item' : template.name,
                        'qty' : 1,
                        'rate' : template.lab_test_rate,
                        
                    }
                    )
        frappe.set_value("Order" , order_doc.name ,"order_items" , items )
    # order_doc.order_items = items
        order_doc.reload()
    drug_items = []
    if doc.drug_prescription:
        order_doc = frappe.get_doc("Order" , doc.medical)
        for item in doc.drug_prescription:
            
            item_price = frappe.db.get_value("Item Price" , {"item_code" : item.drug_code , "selling" : 1} , "price_list_rate")
            items.append(
                {
                    'item' : item.drug_code,
                    'qty' : item.qty,
                    'rate' : item_price,
                    'amount' : int(item.qty) * int(item_price)
                }
                )
       
        frappe.set_value("Order" , order_doc.name ,"order_items" , items )
    # frappe.publish_realtime("doc_update", {"modified": doc.modified, "doctype": doc.doctype, "name": doc.name},
	# 		doctype=doc.doctype, docname=doc.name, after_commit=True)
def create_service(doc , services):
    items = []
    total = 0
    for service in doc.lab_test_prescription:
        template = frappe.get_doc('Lab Test Template' , service.lab_test_code)
        items.append(
            {
                'item' : template.name,
                'qty' : 1,
                'rate' : template.lab_test_rate,
                'amount' : template.lab_test_rate
            }
            )
        total += template.lab_test_rate
        
    new_doc = frappe.get_doc({
            'doctype' : 'Order',
            'patient' : doc.patient,
            'doctor' : doc.practitioner,
            'order_items' : items,
            'grand_total': total,
            'order_type' : 'Service'
            
        })
    new_doc.insert(
        ignore_permissions=True, # ignore write permissions during insert
        ignore_links=True, # ignore Link validation in the document
        ignore_if_duplicate=True, # dont insert if DuplicateEntryError is thrown
        ignore_mandatory=True # insert even if mandatory fields are not set
    )
    frappe.set_value("Patient Encounter" , doc.name,"service" , new_doc.name)
    frappe.db.commit()


def create_drug(doc):
    items = []
    total = 0
    for drug in doc.drug_prescription:
       
        item_price = frappe.db.get_value("Item Price" , {"item_code" : drug.drug_code , "selling" : 1} , "price_list_rate")
        items.append(
            {
                'item' : drug.drug_code,
                'qty' : drug.qty,
                'rate' : item_price,
                'amount' : int(drug.qty) * int(item_price)
            }
            )
        total += int(drug.qty) * int(item_price)
        
    new_doc = frappe.get_doc({
            'doctype' : 'Order',
            'patient' : doc.patient,
            'doctor' : doc.practitioner,
            'order_items' : items,
            'grand_total': total,
            'order_type' : 'Pharmacy'
            
        })
    new_doc.insert()
    frappe.set_value("Patient Encounter" , doc.name,"medical" , new_doc.name)
    frappe.db.commit()



