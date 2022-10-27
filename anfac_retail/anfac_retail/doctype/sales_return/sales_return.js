// Copyright (c) 2022, Anfac Tech and contributors
// For license information, please see license.txt
var d = {}
frappe.ui.form.on('Sales Return', {
	
	refresh: function(frm) {
		if(frm.is_new()){
			frm.disable_save();
		
		
		frm.add_custom_button('Save', () => {
			
			d = new frappe.ui.Dialog({
				title: 'Return Type',
				fields: [
					{
						label: 'Refund',
						fieldname: 'refund',
						fieldtype: 'Check',
						read_only : 1,
						default : 1
						// onchange: function(e) {
						// 	// alert("Selected : ", this.value)
						// 	// console.log('this is ' , this.value)
						// 	// check_uncheck(e)
						// 	d.set_value('invoice' , !this.value)

							
						// }
					},
					{
						label: 'Invoice',
						fieldname: 'invoice',
						fieldtype: 'Check',
						onchange: function(e) {
							// alert("Selected : ", this.value)
							// console.log('this is ' , this.value)
							// check_uncheck(e)
							
							d.set_value('refund' , !this.value)

							
						}
					}
				],
				primary_action_label: 'Submit',
				primary_action(values) {
					// console.log(values);
					frm.set_value('invoice' , values.invoice)
					frm.set_value('refund' , values.refund)
					frm.save()
					frm.save("Submit")
					d.hide();
				}
			});
			
			d.show();
			
			// frappe.set_route('Form', frm.doc.reference_type, frm.doc.reference_name);
		})
	}
		
	},
		
		// save:function(frm){
			
		// },
		before_save:function(frm){
			// alert('ok')
			calculate_total(frm)
		},
		discount :function(frm){
			calculate_total(frm)
		}
	})
	
	frappe.ui.form.on('Order Items', {
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
		refresh(frm) {
			// your code here
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
	

	function check_uncheck(e){
			alert(d)
			d.set_value("inovice" , 1)
			console.log(d)
	}