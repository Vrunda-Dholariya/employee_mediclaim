frappe.query_reports["Employee Mediclaim Report 2"] = {
	filters: [
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.datetime.month_start(),
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: frappe.datetime.month_end(),
		},
	],
	onload: function(report) {
		// Force date range back to current month on every load,
		// since saved filter values in local storage override "default"
		report.page.fields_dict["from_date"].set_value(frappe.datetime.month_start());
		report.page.fields_dict["to_date"].set_value(frappe.datetime.month_end());
		report.refresh();
	},
};