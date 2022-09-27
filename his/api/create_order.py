import frappe
@frappe.whitelist()
def create_order(doc , method = None):
    order = frappe.db.exists("Order", doc.service, cache=True)
    if not order:
        frappe.msgprint(doc.service)
        orders =  ['drug_prescription' , 'lab_test_prescription' ,'procedure_prescription']
        for order in orders:
            if order == 'drug_prescription' :
                pass
            if order == 'lab_test_prescription':
                create_service(doc , order)
    else:
        update_order(doc , order)

def update_order(doc , service):
    items = []
    order_doc = frappe.get_doc("Order" , doc.service)
    for item in doc.lab_test_prescription:
        template = frappe.get_doc('Lab Test Template' , item.lab_test_code)
        items.append(
                {
                    'item' : item.name,
                    'qty' : 1,
                    'rate' : template.lab_test_rate,
                    'amount' : template.lab_test_rate
                }
                )
    order_doc.order_items = items
    order_doc.db_update()

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
    new_doc.insert()
    frappe.db.set_value("Patient Encounter" , doc.name,"service" , new_doc.name)
    frappe.db.commit()

def create_medical(medical):
    name = 1+2
    frappe.errprint(medical)