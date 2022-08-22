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
		cond += f'and is_pos = 0'
	elif sts == "Paid":
		cond += f'and is_pos = 1 ' 
	# frappe.msgprint(cond)
	amount = "net_total"
	if sts == "Paid":
		amount = 'paid_amount'
	data = frappe.db.sql(f"""
	select 
	name, 
	posting_date,
	customer ,
	invoice_no ,
	{amount}  

from `tabSales Invoice` 
where  posting_date between "{_from}" and "{to}" {cond} 
 ;""")
	return data
def get_columns():
	return [
		
		"Voucher:Link/Sales Invoice:220",
		"Date: Date:120",
		"Customer Name:Link/Customer:200",
		"Invoice No:Data:120", 
		"Paid Amount:Currency:110",
	
		
	]

