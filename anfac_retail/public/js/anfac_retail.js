

// $( "#purchase_detal_btn" ).click(function() {
//     alert( "Handler for .click() called." );
//   })

function consoleerp_hi(data , _from , to){
    // alert(data)
    // alert(_from)
    // alert(to)
	frappe.set_route('query-report', 'Purchase Items', { supplier: data , from_date : _from , to_date : to})
}


function statement(party){
    let d = new frappe.ui.Dialog({
        title: 'Enter details',
        fields: [
            {
                label: 'From Date',
                fieldname: 'from_date',
                fieldtype: 'Date',
                reqd : 1
            },
            {
                label: 'To Date',
                fieldname: 'to_date',
                fieldtype: 'Date',
                reqd : 1
            },
            
        ],
        primary_action_label: 'Submit',
        primary_action(values) {
            frappe.call({
                method: "anfac_retail.api.api.get_report_content",
                args: {
                  
                  company: frappe.defaults.get_default('Company'),
                  customer_name: party,
                  from_date: values.from_date,
                  to_date: values.to_date
                },
                callback: function (r) {
                  
                  var x = window.open();
                  x.document.open().write(r.message);
                }
              });
            d.hide();
        }
    });
    
    d.show();
    // alert(party)
    // frappe.new_doc("Customer Statements Sender"  ,{ customer: party } )
    // frappe.set_route('Form', 'Customer Setatements Sender',"Customer Statements Sender" ,{ customer: party })

}
// $( "#purchase_detal_btn").hide()

//   alert($("#purchase_detal_btn").text())


