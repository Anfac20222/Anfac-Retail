import frappe

@frappe.whitelist()
def create_journal(doc , method = None):
    for exp in doc.taxes:
        if exp.against_account:
            # frappe.msgprint("this is " ,doc.voucher_no)
            journal_doc = frappe.get_doc(
                {
                    'doctype': 'Journal Entry',
                    'voucher_type' : 'Journal Entry',
                    'posting_date' : doc.posting_date,
                    'voucher_no' : doc.voucher_no,
                    'accounts' : [{
                        'account' : exp.expense_account,
                        'debit_in_account_currency' : exp.amount,
                    
                        
                    },
                    {
                        'account' : exp.against_account,
                        'credit_in_account_currency' : exp.amount,
                        'party_type' : exp.party,
                        'party' : exp.supplier

                        
                    }
                    
                    ]
                

                }
            )
            # print("\n\n\n\n\n",journal_doc , "\n\n\n\n\n\n")
            # frappe.msgprint(exp.amount)
            journal_doc.insert()
            journal_doc.submit()
            frappe.db.set_value('Landed Cost Taxes and Charges', exp.name, 'journal_entry', journal_doc.name)


def cancel_journal(doc , method = None):
    for exp in doc.taxes:
        journal_doc = frappe.get_doc("Journal Entry" , exp.journal_entry)
        journal_doc.cancel()

@frappe.whitelist()        
def create_journal_se(doc , method = None):
    for exp in doc.additional_costs:
        journal_doc = frappe.get_doc(
            {
                'doctype': 'Journal Entry',
                'voucher_type' : 'Journal Entry',
                'posting_date' : doc.posting_date,
                'voucher_no' : doc.voucher_no,
                'accounts' : [{
                    'account' : exp.expense_account,
                    'debit_in_account_currency' : exp.amount,
                   
                    
                },
                {
                    'account' : "1110 - Cash - ATC",
                    'credit_in_account_currency' : exp.amount,

                    
                }
                
                ]
            

            }
        )
        # print("\n\n\n\n\n",journal_doc , "\n\n\n\n\n\n")
        # frappe.msgprint(exp.amount)
        journal_doc.insert()
        journal_doc.submit()
        frappe.db.set_value('Landed Cost Taxes and Charges', exp.name, 'journal_entry', journal_doc.name)


def cancel_journal_se(doc , method = None):
    for exp in doc.additional_costs:
        journal_doc = frappe.get_doc("Journal Entry" , exp.journal_entry)
        journal_doc.cancel()        
 
