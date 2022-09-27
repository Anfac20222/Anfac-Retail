frappe.ui.form.on('Order', {
	refresh(frm) {
		// your code here
	},
	before_save:function(frm){
		// alert('ok')
		calculate_total(frm)
	}
})

frappe.ui.form.on('Order Items', {
	refresh(frm) {
		// your code here
	},
	item: function(frm , cdt , cdn){
		// alert("ok")
		var row = locals[cdt][cdn]
		row.amount = row.qty * row.rate
		calculate_total(frm)
		frm.refresh_field('order_items')
		
		// alert(row.item)
	},
	qty: function(frm , cdt , cdn){
		// alert("ok")
		var row = locals[cdt][cdn]
		row.amount = row.qty * row.rate
		calculate_total(frm)
		frm.refresh_field('order_items')
		
		// alert(row.item)
	},
	rate: function(frm , cdt , cdn){
		// alert("ok")
		var row = locals[cdt][cdn]
		row.amount = row.qty * row.rate
		calculate_total(frm)
		frm.refresh_field('order_items')
		
		// alert(row.item)
	}
})
function calculate_total(frm){
	let grand_total = 0
	var rows = frm.doc.order_items
	rows.forEach(item => {
		grand_total +=  parseInt(item.amount)
	});
	frm.set_value('grand_total' , grand_total)
}