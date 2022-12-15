# Copyright (c) 2022, Anfac Tech and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	
	return get_columns(), get_data(filters)
def get_data(filters):
	
	_from ,to  = filters.get('from_date'), filters.get('to')  
	# if sts == "Unpaid":
	# 	cond += f'and is_pos = 0'
	# elif sts == "Paid":
	# 	cond += f'and is_pos = 1 ' 
	# frappe.msgprint(cond)

	# if center:
	# 	sel_cent += f"and cost_center = '{center}'"
	
	data = frappe.db.sql(f"""
	select 
	name, 
	posting_date,
	party ,
	reciept_no ,
	paid_amount  

from `tabPayment Entry` 
where posting_date between "{_from}" and "{to}" and party_type = "Customer" 
 ;""")
	return data
def get_columns():
	return [
		
		"Voucher:Link/Payment Entry:220",
		"Date: Date:120",
		"Customer Name:Link/Customer:200",
		"Recipt No:Data:120", 
		"Paid Amount:Currency:110",
	
		
	]

