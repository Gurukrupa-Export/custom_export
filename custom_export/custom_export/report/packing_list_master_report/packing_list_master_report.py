# Copyright (c) 2023, gurukrupa_export] and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)
	return columns,data

def get_data(filters=None):
	conditions = get_conditions(filters)
	
	if conditions:		
		data = frappe.db.sql(f"""select tpld.item_code, tpld.item_category, 
						tpld.diamond_pcs, tpld.diamond_quality, tpld.diamond_weight, tpld.diamond_rate, tpld.diamond_amount,
						tpld.gross_weight, tpld.other_weight, tpld.stone_weight , tpld.net_weight , tpld.chain_weight, 
						tpld.gold_amount , tpld.stone_amount , tpld.chain_amount , tpld.metal_touch , tpld.chain_metal_touch,
						tpld.chain_making_charge , tpld.certificate_charge , tpld.jewellery_making_charge , tpld.total_amount, 
						tpl.sales_order,tpl.customer_name, tpl.customer_address, tpl.date
						from `tabPacking List` tpl 
						RIGHT JOIN `tabPacking List Detail` tpld 
						ON tpl.name = tpld.parent  {conditions}""",as_dict=1)
	else:
		data = frappe.db.sql(f"""select tpld.item_code, tpld.item_category, 
						tpld.diamond_pcs, tpld.diamond_quality, tpld.diamond_weight, tpld.diamond_rate, tpld.diamond_amount,
						tpld.gross_weight, tpld.other_weight, tpld.stone_weight , tpld.net_weight , tpld.chain_weight, 
						tpld.gold_amount , tpld.stone_amount , tpld.chain_amount , tpld.metal_touch , tpld.chain_metal_touch,
						tpld.chain_making_charge , tpld.certificate_charge , tpld.jewellery_making_charge , tpld.total_amount, 
						tpl.sales_order,tpl.customer_name, tpl.customer_address, tpl.date
						from `tabPacking List` tpl 
						RIGHT JOIN `tabPacking List Detail` tpld 
						ON tpl.name = tpld.parent""",as_dict=1)
	
	if not data:

		return
	
	# data = process_data(data, filters)
	
	return data

def get_columns(filters=None):
	columns = [
		{
			"label": _("Sales Order"),
			"fieldname": "sales_order",
			"fieldtype": "Data"
		},
		{
			"label": _("Customer Name"),
			"fieldname": "customer_name",
			"fieldtype": "Data"
		},
		{
			"label": _("Customer Address"),
			"fieldname": "customer_address",
			"fieldtype": "Data"
		},
		{
			"label": _("Date"),
			"fieldname": "date",
			"fieldtype": "Date"
		},
		{
			"label": _("Item Code"),
			"fieldname": "item_code",
			"fieldtype": "Data"
		},
		{
			"label": _("Item Category"),
			"fieldname": "item_category",
			"fieldtype": "Data",
		},
		{
			"label": _("Diamond Quality"),
			"fieldname": "diamond_quality",
			"fieldtype": "Data"
		},
		{
			"label": _("Diamond Pcs"),
			"fieldname": "diamond_pcs",
			"fieldtype": "Data"
		},
		{
			"label": _("Diamond Rate"),
			"fieldname": "diamond_rate",
			"fieldtype": "Data"
		},
		{
			"label": _("Diamond Amount"),
			"fieldname": "diamond_amount",
			"fieldtype": "Data"
		},
		{
			"label": _("Gross Weight"),
			"fieldname": "gross_weight",
			"fieldtype": "Data"
		},
		{
			"label": _("Other Weight"),
			"fieldname": "other_weight",
			"fieldtype": "Data"
		},
		{
			"label": _("Stone Weight"),
			"fieldname": "stone_weight",
			"fieldtype": "Data"
		},
		{
			"label": _("Net Weight"),
			"fieldname": "net_weight",
			"fieldtype": "Data"
		},
		{
			"label": _("Chain Weight"),
			"fieldname": "chain_weight",
			"fieldtype": "Data"
		},
		{
			"label": _("Gold Amount"),
			"fieldname": "gold_amount",
			"fieldtype": "Data"
		},
		{
			"label": _("Stone Amount"),
			"fieldname": "stone_amount",
			"fieldtype": "Data"
		},
		{
			"label": _("Chain Amount"),
			"fieldname": "chain_amount",
			"fieldtype": "Data"
		},
		{
			"label": _("Metal Touch"),
			"fieldname": "metal_touch",
			"fieldtype": "Data"
		},
		{
			"label": _("Chain Metal Touch"),
			"fieldname": "chain_metal_touch",
			"fieldtype": "Data"
		},
		{
			"label": _("Chain Making Charge"),
			"fieldname": "chain_making_charge",
			"fieldtype": "Data"
		},
		{
			"label": _("Certificate Charge"),
			"fieldname": "certificate_charge",
			"fieldtype": "Data"
		},
		{
			"label": _("Jewellery Making Charge"),
			"fieldname": "jewellery_making_charge",
			"fieldtype": "Data"
		},
		{
			"label": _("Total Amount"),
			"fieldname": "total_amount",
			"fieldtype": "Data"
		},
	]

	return columns

def get_conditions(filters):
	print(filters)
	filter_list = []


	if filters.get("date"):
		filter_list.append(f'''tpl.date = "{filters.get("date")}"''')

	if filters.get("salesOrder"):
		filter_list.append(f'tpl.sales_order in {tuple(filters.get("salesOrder"))}'.replace(',)',')'))

	if filters.get("customer_name"):
		filter_list.append(f'''tpl.customer_name = "{filters.get("customer_name")}"''')

	if filters.get("item_code"):
		filter_list.append(f'''tpld.item_code = "{filters.get("item_code")}"''')

	conditions = "where " + " and ".join(filter_list)
	if conditions!='where ':
		return conditions