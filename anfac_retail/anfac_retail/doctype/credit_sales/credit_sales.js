// Copyright (c) 2022, Anfac Tech and contributors
// For license information, please see license.txt

frappe.ui.form.on('Credit Sales', {
	refresh: function(frm) {
		if(frm.is_new()){
			// alert('ok')
			frm.set_value("sales_invoice" , '')
		}
	},
	before_save:function(frm){
		// alert('ok')
		calculate_total(frm)
	},
	discount :function(frm){
		calculate_total(frm)
	}
})

frappe.ui.form.on('Order Items', {
	refresh(frm) {
		// your code here
	},
	item:function(frm , cdt ,cdn){
	    var row = locals[cdt][cdn]
	   frappe.db.get_value("Item Price" , {"item_code" : row.item , "selling" : 1 } , 'price_list_rate')
	   .then(r => {
	       if (r.message.price_list_rate){
	           row.rate = r.message.price_list_rate
	           row.amount = row.qty * row.rate
	           frm.refresh_field("items")
	       }
	   })
	   frappe.db.get_value("Bin" , {'warehouse' : frm.doc.warehouse , 'item_code' : row.item} , 'actual_qty')
	   .then(r => {
	    
	       if(r.message.actual_qty){
	           row.available_qty = r.message.actual_qty
	            frm.refresh_field("items")
	       }
	       else{
	           //   alert("ok")
	             row.available_qty = 0
	            frm.refresh_field("items")
	       }
	   })
	    
	},
	// item: function(frm , cdt , cdn){
	// 	// alert("ok")
	// 	var row = locals[cdt][cdn]
	// 	row.amount = row.qty * row.rate
	// 	calculate_total(frm)
	// 	frm.refresh_field('items')
		
	// 	// alert(row.item)
	// },
	qty: function(frm , cdt , cdn){
		// alert("ok")
		var row = locals[cdt][cdn]
		row.amount = row.qty * row.rate
		calculate_total(frm)
		frm.refresh_field('items')
		
		// alert(row.item)
	},
	rate: function(frm , cdt , cdn){
		// alert("ok")
		var row = locals[cdt][cdn]
		row.amount = row.qty * row.rate
		calculate_total(frm)
		frm.refresh_field('items')
		
		// alert(row.item)
	}
})
function calculate_total(frm){
	// alert("pk")
	let grand_total = 0
	var rows = frm.doc.items
	rows.forEach(item => {
		grand_total +=  parseInt(item.qty) * parseFloat(item.rate) 
	});
	if(frm.doc.discount){
	grand_total = grand_total - parseFloat(frm.doc.discount) 
	}
	// alert( grand_total)
	frm.set_value('grand_total' , grand_total)
}
