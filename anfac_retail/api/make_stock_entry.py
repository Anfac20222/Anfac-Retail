import frappe

@frappe.whitelist()
def make_stock_entry(work_order_id, purpose, qty=None):
	work_order = frappe.get_doc("Work Order", work_order_id)
	if not frappe.db.get_value("Warehouse", work_order.wip_warehouse, "is_group"):
		wip_warehouse = work_order.wip_warehouse
	else:
		wip_warehouse = None
	
	stock_entry = frappe.new_doc("Stock Entry")
	stock_entry.purpose = purpose
	stock_entry.work_order = work_order_id
	stock_entry.company = work_order.company
	stock_entry.from_bom = 1
	stock_entry.bom_no = work_order.bom_no
	stock_entry.use_multi_level_bom = work_order.use_multi_level_bom
	
	# accept 0 qty as well
	if  qty:
		qty= int(qty)

	stock_entry.fg_completed_qty = (
		qty if qty is not None else (flt(work_order.qty) - flt(work_order.produced_qty))
	)

	if work_order.bom_no:
		stock_entry.inspection_required = frappe.db.get_value(
			"BOM", work_order.bom_no, "inspection_required"
		)

	if purpose == "Material Transfer for Manufacture":
		stock_entry.voucher_no = work_order.voucher_no
		stock_entry.to_warehouse = wip_warehouse
		stock_entry.project = work_order.project
	else:
		stock_entry.voucher_no = "tran"+work_order.voucher_no
		stock_entry.from_warehouse = wip_warehouse
		stock_entry.to_warehouse = work_order.fg_warehouse
		stock_entry.project = work_order.project		
		

	stock_entry.posting_date = work_order.posting_date
	stock_entry.set_stock_entry_type()
	stock_entry.get_items()
	stock_entry.set_serial_no_batch_for_finished_good()
	if purpose == "Material Transfer for Manufacture":
		if work_order.additional_costs:
			for i in work_order.additional_costs:
				stock_entry.append("additional_costs",{"expense_account": i.expense_account, "description":i.description, "amount": i.amount }) 
				
	stock_entry.save()
	stock_entry.submit()
	return stock_entry.as_dict()

