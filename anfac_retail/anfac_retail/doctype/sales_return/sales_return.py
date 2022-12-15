# Copyright (c) 2022, Anfac Tech and contributors
# For license information, please see license.txt

import frappe
from anfac_retail.api.create_inv import create_inv
from frappe.model.document import Document

class SalesReturn(Document):
	def on_submit(self):
		# frappe.msgprint("ok")
		sales_doc = create_inv(self.name ,dt = 'Sales Return' , is_sales_return = True , is_credit = self.invoice)
		self.sales_invoice = sales_doc.name
		self.save()
	def on_cancel(self):
		if self.sales_invoice:
			sales_doc = frappe.get_doc("Sales Invoice" , self.sales_invoice)
			sales_doc.cancel()
