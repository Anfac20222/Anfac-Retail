frappe.ui.form.on('Sales Invoice', {
	refresh(frm) {
		// alert("ok ok")
		// your code here
		if (frm.is_new()) {
		frappe.call({
        method: "anfac_retail.api.get_last_doc.get_last_doc", //dotted path to server method
        callback: function(r) {
            // code snippet
            var m = r.message
            // console.log(m.toString())
            //   // var str = "Rs. 6,67,000";
            var inv_n = m.toString();
            var inv_name = inv_n.replace(/\d/g, "");
            var res = parseInt(inv_n.replace(/\D/g, ""));
            // alert(res)
            if (res !== 1){
                frm.set_value("invoice_no" , `${inv_name}${res+1}` )
            }
            
            // alert(res);
        }
    });
	}
	}
})

frappe.ui.form.on('Sales Invoice Item', {
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