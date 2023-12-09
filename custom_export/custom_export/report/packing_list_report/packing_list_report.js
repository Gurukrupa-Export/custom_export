// Copyright (c) 2023, gurukrupa_export] and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Packing List Report"] = {
	"filters": [		
		{
			"label": __("Sales Order ID"),
			"fieldname": "salesOrder",
			"fieldtype": "MultiSelectList",
			get_data: function(txt) {
				var filters = get_filter_dict(frappe.query_report)
				if (!filters) filters = {}
				return frappe.db.get_link_options('Sales Order', txt, filters);
			},
			"on_change": function(query_report){
				var emp_list = query_report.get_filter_value('salesOrder')
				query_report.current_emp = 0
				query_report.emp_count = emp_list.length
				set_employee(query_report, query_report.current_emp)
			},
		},
		{
			"label": __("Selected Sales Order"),
			"fieldtype": "Link",
			"fieldname": "cur_sales_order",
			"options": "Sales Order",
			// "reqd": 1,
			"hidden": 1,
			"get_query": function() {
				var salesOrder_list = frappe.query_report.get_filter_value('salesOrder')
				console.log(salesOrder_list);
				return {
					"doctype": "Sales Order",
					"filters": {"name":["in",salesOrder_list]}
				}
			},
			"on_change": function(query_report){
				let emp =  frappe.query_report.get_filter_value('cur_sales_order');
				let employees = query_report.get_filter_value('salesOrder')
				var idx = employees.indexOf(emp)
				if (idx>0) {
					query_report.current_emp = idx
				}
				// set_employee_details(query_report)
			},

		},
		{
			"label": __("Sales Order"),
			"fieldtype": "Link",
			"fieldname": "sales_order",
			"options": "Sales Order",
			"hidden": 1,
			"get_query": function() {
				var filters = get_filter_dict(frappe.query_report)
				if (!filters) return
				return {
					"doctype": "Sales Order",
					"filters": filters
				}
			}
		},
		{
			"label": __("Customer Name"),
			"fieldtype": "Link",
			"fieldname": "customer_name",
			"options":"Customer"
		},
		{
			"label": __("Customer"),
			"fieldtype": "Link",
			"fieldname": "customer",
			"options":"Customer",
			"hidden": 1,
		},
		{
			"label": __("Date"),
			"fieldtype": "Date",
			"fieldname": "date",
			// "default": frappe.datetime.get_today(),
		},
		{
			"label": __("Item Code"),
			"fieldtype": "Link",
			"fieldname": "item_code",
			"options": "Item",
		},
	],
	onload: (report) => {
		// fetch_month_list()
		report.page.add_button("Clear Filters", function() {
			window.open("/app/query-report/Packing%20List%20Report", "_self")
		}).addClass("btn-info")
		report.page.add_button("Generate", function() {
			var emp = frappe.query_report.get_filter_value('cur_sales_order');
			var date = frappe.query_report.get_filter_value('date');
			var customer_name = frappe.query_report.get_filter_value('customer_name');
			frappe.query_report.set_filter_value({
				"sales_order": emp,
				"date":date,
				"customer_name":customer_name
			});
			// else {
			// }
		}).addClass("btn-primary")
		fetch_salesOrder(report)
	}
};

function set_employee(query_report, index, preset = false) {
	var salesOrder = query_report.get_filter_value('salesOrder')
	query_report.set_filter_value({
		"cur_sales_order": salesOrder[index] || null,
		"sales_order": preset ? salesOrder[index] : null
	});
}

function set_employee_details(query_report) {
	var employee = query_report.get_filter_value('cur_sales_order');
	frappe.db.get_value("Sales Order", employee, ["customer_name", "customer_address", ], (r)=> {
		query_report.set_filter_value({
			"customer_name": r.customer_name,
			// "customer_address": r.customer_address,
			// "emp_department": r.department,
			// "punch_id": r.attendance_device_id
		});
		// frappe.db.get_value("Shift Type", r.default_shift, "shift_hours", (shift)=>{
		// 	query_report.set_filter_value({
		// 		"shift_hrs": shift.shift_hours
		// 	});
		// })
	})
}

function fetch_salesOrder(query_report){
	var filters = get_filter_dict(query_report)
	console.log(filters);
	if (filters){
		frappe.db.get_list("Sales Order",{"filters" : filters, "pluck":"name", "order_by":"name"}).then((r)=>{
			query_report.set_filter_value("salesOrder",r)
			if (r.length != 0) {
				query_report.current_emp = 0
				query_report.emp_count = r.length
				set_employee(query_report, query_report.current_emp)
			}
			else {
				query_report.set_filter_value({
					"sales_order": null
				});		
			}
		})
	}
}

function get_filter_dict(query_report) {
	var customerName = query_report.get_filter_value('customer');
	console.log(customerName);
	// var department = query_report.get_filter_value('department');
	var filters = {}
	// if (customerName && department.length > 0) {
	if (customerName) {
		filters['customer'] = customerName
		// filters['department'] = ['in',department]
	}
	else if (customerName) {
		filters['customer'] = customerName
	}
	// else if (department.length > 0) {
	// 	filters['department'] = ['in',department]
	// }
	else {
		return null
	}
	return filters
}