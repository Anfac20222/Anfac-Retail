// Copyright (c) 2022, Anfac Tech and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Sales Report"] = {
	"filters": [
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default:frappe.datetime.now_date(),
			reqd: 1
		},
		{
			fieldname: "to",
			label: __("To Date"),
			fieldtype: "Date",
			default:frappe.datetime.now_date(),
			reqd: 1
		},
		{
			"fieldname":"account",
			"label": __("Account"),
			"fieldtype": "MultiSelectList",
			"options": "Account",
			"default" : ["1110 - Cash - AT"],
			get_data: function(txt) {
				return frappe.db.get_link_options('Account', txt, {
					company: frappe.defaults.get_global_default("company"),
					is_group : 0,
					

				});
			}
		},
		

	]
};

