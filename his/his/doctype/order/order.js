frappe.ui.form.on('Order', {
	refresh(frm) {
		frm.add_custom_button('Cash', () => {
			alert("Cash")
			// frappe.set_route('Form', frm.doc.reference_type, frm.doc.reference_name);
		})
		frm.add_custom_button('Credit', () => {
			alert("Credit")
			// frappe.set_route('Form', frm.doc.reference_type, frm.doc.reference_name);
		}),
		// your code here
		calculate_total(frm)
		frm.save()
	},
	// frappe.realtime.on('event_name', (data) => {
	// 	console.log(data)
	// })
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
		grand_total +=  parseInt(item.qty) * parseInt(item.rate) 
	});
	frm.set_value('grand_total' , grand_total)
}