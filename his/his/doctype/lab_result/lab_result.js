// Copyright (c) 2022, Anfac and contributors
// For license information, please see license.txt

frappe.ui.form.on('Lab Result', {
	refresh: function(frm) {
		frm.add_custom_button('Print', () => {
			if(frm.doc.lab_test_name){
			window.open(`
			http://104.251.214.176/printview?doctype=Lab%20Result&name=${frm.doc.name}&trigger_print=1&format=Urine&no_letterhead=0&letterhead=Logo&settings=%7B%7D&_lang=en-US
	`);
			}
			else{
				if(frm.doc.type == "Hormones"){

					window.open(`


					http://104.251.214.176/printview?doctype=Lab%20Result&name=${frm.doc.name}&trigger_print=1&format=hormone&no_letterhead=0&letterhead=Logo&settings=%7B%7D&_lang=en-US

			
			
					`);
					
									}
				else{
				window.open(`
				http://104.251.214.176/printview?doctype=Lab%20Result&name=${frm.doc.name}&trigger_print=1&format=Test%20Report&no_letterhead=0&letterhead=Logo&settings=%7B%7D&_lang=en-US		`);
			}
		}
		})
	}
});
