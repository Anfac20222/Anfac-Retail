// Copyright (c) 2022, Anfac Tech and contributors
// For license information, please see license.txt

frappe.ui.form.on('Credit Sales', {
	refresh: function(frm) {
		if(frm.is_new()){
			// alert('ok')
			frm.set_value("sales_invoice" , '')
		}
	},
	customer: function(frm){
		frappe.call({
			method: "erpnext.accounts.doctype.payment_entry.payment_entry.get_party_details",
			args: {
				company: "Life Care Pharma",
				party_type: "Customer",
				party: frm.doc.customer,
				date: frm.doc.date,
				cost_center: "Main - LCP"
			},
			callback: function(r, rt) {
				if(r.message) {
				frm.set_value("customer_balance", r.message.party_balance)
				}
			}
		});
	},

	details: function(frm){
	   frappe.call({
			method: "anfac_retail.api.api.get_report_content",
			args: {
			  
			  company: frappe.defaults.get_default('Company'),
			  customer_name: frm.doc.customer,
			  from_date: "01-01-2020",
			  to_date: frappe.datetime.nowdate()
			},
			callback: function (r) {
			  
			  var x = window.open();
			  x.document.open().write(r.message);
			}
		  });
	},
	
	amount: function(frm , cdt , cdn){
	let row = locals[cdt][cdn]
	row.rate = row.amount/row.qty
	if(row.qty){
	frm.refresh_field('items')
	}
   // console.log(row)
   // alert("ok")
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
		// if(r.message.actual_qty <= 0  || row.qty > r.message.actual_qty){
		// 	frappe.msgprint({
		// 		title: __('Notification'),
		// 		indicator: 'red',
		// 		message: __(`Tirada Kaaga Tataalo <b>${row.item}</b>  Waa <b>${r.message.actual_qty }</b> `)
		// 	});			
		// }

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
	// 	frappe.db.get_value("Bin" , {'warehouse' : frm.doc.warehouse , 'item_code' : row.item} , 'actual_qty')
	//    .then(r => {
	// 	if(row.qty >= r.message.actual_qty){
	// 		frappe.msgprint({
	// 			title: __('Notification'),
	// 			indicator: 'red',
	// 			message: __(`Tirada Kaaga Tataalo <b>${row.item}</b>  Waa <b>${r.message.actual_qty }</b> `)
	// 		});			
	// 	}

	
	//    })
		row.amount = row.qty * row.rate
		calculate_total(frm)
		frm.refresh_field('items')
		
		// alert(row.item)
	},
	rate: function(frm , cdt , cdn){
		// alert("ok")
		var row = locals[cdt][cdn]
		frappe.db.get_value("Item Price" , {"item_code" : row.item , "buying" : 1 } , 'price_list_rate')
	   .then(r => {
		if( row.rate < r.message.price_list_rate ){
			frappe.msgprint({
				title: __('Notification'),
				indicator: 'red',
				message: __(`Qimaha aad ku ibinayso  <b>${row.item}</b>  waxa uu kayartahay Qimaha aad Ku sogaday  <b>${r.message.price_list_rate }</b> `)
			});			
		}
	   })
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
		grand_total +=  parseFloat(item.qty) * parseFloat(item.rate) 
	});
	if(frm.doc.discount){
	grand_total = grand_total - parseFloat(frm.doc.discount) 
	}
	// alert( grand_total)
	frm.set_value('grand_total' , grand_total)
}



frappe.ui.form.on('Order Items', {
	refresh(frm) {
		// your code here
	},
		amount: function(frm , cdt , cdn){
	    let row = locals[cdt][cdn]
	    row.rate = row.amount/row.qty
	    if(row.qty){
	    frm.refresh_field('items')
	    }
	   // console.log(row)
	   // alert("ok")
	}

})
