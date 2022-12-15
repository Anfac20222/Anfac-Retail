# Copyright (c) 2022, Anfac Tech and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	
	return get_columns(), get_data(filters)
def get_data(filters):
	cond = ""
	sel_cent = ""
	

	_from ,to, sts, center = filters.get('from_date'), filters.get('to')  ,filters.get('status') , filters.get('center') 
	if center:
		sel_cent += f"and cost_center = '{center}'"
	if sts == "Unpaid":
		cond += f'and is_paid = 0'
	elif sts == "Paid":
		cond += f'and is_paid = 1 ' 
	# frappe.msgprint(cond)
	amount = "net_total"
	if sts == "Paid":
		amount = 'paid_amount'
	report_type = 'query-report'
	report = 'Accounts Receivable'
	data = frappe.db.sql(f"""
	select 
	customer ,
	'',
	sum(net_total) ,
	CONCAT('<button type=''button'' class = "btn btn-primary" data=''', customer ,''' onClick=''sales_items(this.getAttribute("data") , "{_from}" , "{to}")''>Details</button>') as "Button:Data:100" 

from `tabSales Invoice` 
where  posting_date between "{_from}" and "{to}" and docstatus = 1 group by customer
 ;""")
	return data
	
def get_columns():
	return [
		
		"Customer Name:Link/Customer:200",
		"Number: Data:120",
		"Amount:Currency:110",
		"Detail:Data:110"
	
		
	]


