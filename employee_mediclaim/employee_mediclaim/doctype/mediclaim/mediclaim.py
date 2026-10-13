# Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Mediclaim(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF
		from hrms.hr.doctype.mediclaim_member.mediclaim_member import MediclaimMember

		corporate_name: DF.Data | None
		date_of_joining: DF.Date
		employee: DF.Link
		employee_code: DF.Data | None
		employee_name: DF.Data | None
		members: DF.Table[MediclaimMember]
		policy_effective_date: DF.Date
		policy_no: DF.Data
	# end: auto-generated types

	pass
