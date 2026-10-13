frappe.query_reports["Employee Mediclaim Report"] = {
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
		{
			fieldname: "employee_filter",
			label: __("Employee"),
			fieldtype: "Link",
			options: "Employee",
		},
		{
			fieldname: "employee_addition",
			label: __("Employee Addition"),
			fieldtype: "Check",
			default: 1,
		},
		{
			fieldname: "dependent_addition",
			label: __("Dependent Addition"),
			fieldtype: "Check",
			default: 0,
		},
		{
			fieldname: "member_deletion",
			label: __("Member Deletion"),
			fieldtype: "Check",
			default: 0,
		},
	],
	onload: function(report) {
		const checkbox_fields = ["employee_addition", "dependent_addition", "member_deletion"];

		function enforce_single(active_field) {
			checkbox_fields.forEach(function(fname) {
				if (fname !== active_field) {
					report.page.fields_dict[fname].set_value(0);
				}
			});
		}

		checkbox_fields.forEach(function(fname) {
			report.page.fields_dict[fname].df.onchange = function() {
				const value = report.page.fields_dict[fname].get_value();
				if (value) {
					enforce_single(fname);
				}
				report.refresh();
			};
		});

		// Force date range back to current month on every load
		report.page.fields_dict["from_date"].set_value(frappe.datetime.month_start());
		report.page.fields_dict["to_date"].set_value(frappe.datetime.month_end());
		report.page.fields_dict["employee_filter"].set_value("");

		// Fix checkbox state on page load, in case saved filters have more than one ticked
		const ticked = checkbox_fields.filter(function(fname) {
			return report.page.fields_dict[fname].get_value();
		});
		if (ticked.length > 1) {
			enforce_single(ticked[0]);
		} else if (ticked.length === 0) {
			report.page.fields_dict["employee_addition"].set_value(1);
		}

		report.refresh();

		// NEW: Export All Views button
		report.page.add_inner_button(__("Export All Views"), function() {
			const current_filters = report.get_values();
			const params = new URLSearchParams({
				filters: JSON.stringify(current_filters),
			});
			window.open(`/api/method/hrms.hr.report.employee_mediclaim_report.employee_mediclaim_report.export_all_views?${params.toString()}`);
		});
	},
};