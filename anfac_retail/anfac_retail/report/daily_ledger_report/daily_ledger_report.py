# Copyright (c) 2022, Anfac Tech and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import getdate
from frappe.utils import add_to_date
def execute(filters=None):
	
	return get_columns(), get_data(filters)

def get_data(filters):
	# frappe.errprint(filters.account)
	sales = get_sales(filters)
	reciepts = get_recipt(filters)
	journal_recipets =  get_journal(filters)
	journal_payments =  get_journal_payment(filters)
	payments = get_payments(filters)
	purcahse = get_purchase(filters)
	openings = get_account_balance(filters)
	if not filters.account:
		openings =  get_account_balance(filters , "Cash")
	incash = []
	for acco in openings:
		is_group = frappe.db.get_value("Account" , acco.account , "is_group")
		show = frappe.db.get_value("Account" , acco.account , "show")
		if not is_group :
			

			if not filters.account and show: 
				incash.append(
					{
						"type" : "Opening",
						"customer" : acco.account,
						"debit" : acco.balance
					}
			)

			elif acco.account in filters.account:
				incash.append(
					{
						"type" : "Opening",
						"customer" : acco.account,
						"debit" : acco.balance
					}
			)

	total_debit = 0
	total_credit = 0
	for doc in (sales , reciepts , journal_recipets , payments,purcahse, journal_payments  ):
		
		for data in doc:
			incash.append(
				{
					"type" : data.type,
					"date" : data.date,
					"customer" : data.customer,
					"voucher" : data.voucher,
					"debit" : data.debit or '',
					"credit" : data.credit or ''
				}
			)
			total_debit += data.debit
			total_credit += data.credit
	incash.append(
		{}
	)
	incash.append(
		{
			"type" : "<strong>Total</strong>",
			"debit" : total_debit,
			"credit" : total_credit
		}
		
	)
	
	incash.append(
		{
			"type" : "Balance",
			"debit" : total_debit - total_credit
		}
	)
	return incash



# Get Opening Balance
def get_account_balance(filters , account_type = None):
	# pre =adddate(getdate(_from) , datys = -1 ) 
	_from ,to = filters.get('from_date'), filters.get('to')  
	pre = add_to_date(_from, days=-1, as_string=True)
	report_bl = frappe.get_doc("Report", "Account Balance")
	report_filters = {"report_date":pre}
	# if filters.account:
	# 	report_filters['account'] = filters.account
	if account_type:
		report_filters['account_type'] = account_type

	
	columns, data = report_bl.get_data(
		limit=500, user="Administrator", filters=report_filters, as_dict=True
	)

	return data


def get_sales(filters):
	
	

	_from ,to = filters.get('from_date'), filters.get('to')  
	# if center:
	# 	sel_cent += f"and cost_center = '{center}'"
	# if sts == "Unpaid":
	# 	cond += f'and is_pos = 0'
	# elif sts == "Paid":
	# 	cond += f'and is_pos = 1 ' 
	# frappe.msgprint(cond)

	data = frappe.db.sql(f"""
	select 
	"Sales" as type,
	name as name, 
	posting_date as date,
	customer as customer,
	invocie_no as voucher,
	paid_amount as debit,
	0 as credit
	

	from `tabSales Invoice` 
	where  posting_date between "{_from}" and "{to}"
	and is_pos = 1
	;""", as_dict = 1)
	return data


def get_recipt(filters):
	_from ,to = filters.get('from_date'), filters.get('to')  

	
	
	data = frappe.db.sql(f"""
	
	select 
	name  as name, 
	"Reciept" as type,
	posting_date as date, 
	party  as customer,
	reciept_no as voucher,
	paid_amount   as debit,
	0 as credit

	from `tabPayment Entry` 
	where posting_date between "{_from}" and "{to}" and party_type = "Customer" 
	;""" , as_dict = 1)
	return data






def get_journal(filters):
	_from ,to = filters.get('from_date'), filters.get('to')  
	data = frappe.db.sql(f""" 
	select 
	"Reciept" as type,
	p.posting_date as date,
	p.voucher_no as voucher,
	c.account  as customer,


	c.debit as debit,
		c.credit as credit
	
	 from 
	 `tabJournal Entry Account` c 
	 left join `tabJournal Entry` p 
	 on p.name = c.parent
	 where p.posting_date between "{_from}" and "{to}" and p.docstatus !=2  and c.account_type  = "Cash" and c.debit > 0;
	""" ,  as_dict = 1)
	return data



def get_payments(filters):
	_from ,to = filters.get('from_date'), filters.get('to')  

	
	
	data = frappe.db.sql(f"""
	
	select 
	name  as name, 
	"Payment" as type,
	posting_date as date, 
	party  as customer,
	reciept_no as voucher,
	paid_amount   as credit,
	0 as debit

	from `tabPayment Entry` 
	where posting_date between "{_from}" and "{to}" and payment_type = "Pay" 
	;""" , as_dict = 1)
	return data




def get_journal_payment(filters):
	_from ,to = filters.get('from_date'), filters.get('to')  
	data = frappe.db.sql(f""" 
	select 
	"Payment" as type,
	p.posting_date as date,
	p.voucher_no as voucher,
	c.account  as customer,


	c.debit as debit,
		c.credit as credit
	
	 from 
	 `tabJournal Entry Account` c 
	 left join `tabJournal Entry` p 
	 on p.name = c.parent
	 where p.posting_date between "{_from}" and "{to}" and p.docstatus !=2  and c.account_type  = "Cash" and c.credit > 0;
	""" ,  as_dict = 1)
	return data


def get_purchase(filters):
	_from ,to = filters.get('from_date'), filters.get('to')  

	data = frappe.db.sql(f"""
		select 
		"Purchase" as type,
		name as name, 
		posting_date as date,
		supplier as customer,
		voucher_no as voucher,
		paid_amount as credit,
		0 as debit
		

		from `tabPurchase Invoice` 
		where  posting_date between "{_from}" and "{to}"
		and is_paid = 1
		;""", as_dict = 1)
	return data


def get_columns():
	columns = [

{
			"label": _("Date"),
			"fieldtype": "Date",
			"fieldname": "date",
			
			"width": 100,
		},

		{
			"label": _("Type"),
			"fieldtype": "Data",
			"fieldname": "type",
			
			"width": 100,
		},


		{
			"label": _("Voucher"),
			"fieldtype": "Data",
			"fieldname": "voucher",
			
			"width": 100,
		},
	
		
		
		# 	{
		# 	"label": _("Account"),
		# 	"fieldtype": "Data",
		# 	"fieldname": "account",
			
		# 	"width": 200,
		# },
		
			{
			"label": _("Customer"),
			"fieldtype": "Data",
			"fieldname": "customer",
			
			"width": 200,
		},
			
		
		
			{
			"label": _("Debit"),
			"fieldtype": "Currency",
			"fieldname": "debit",
			
			"width": 100,
		},

		{
			"label": _("Credit"),
			"fieldtype": "Currency",
			"fieldname": "credit",
			
			"width": 100,
		},
			
	]

	return columns



