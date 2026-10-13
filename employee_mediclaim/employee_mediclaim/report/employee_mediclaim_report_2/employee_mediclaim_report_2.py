import frappe
from frappe import _
from frappe.utils import date_diff, nowdate, getdate


def execute(filters=None):
    filters = frappe._dict(filters or {})
    data = get_data(filters)
    for row in data:
        dob = row.get("date_of_birth")
        row["age"] = date_diff(getdate(nowdate()), getdate(dob)) // 365 if dob else None
        row["member_type"] = "Employee" if (row.get("relation") or "").strip().lower() == "self" else "Dependent"

    total_employees = len([r for r in data if (r.get("relation") or "").strip().lower() == "self"])
    total_dependents = len(data) - total_employees
    total_members = len(data)

    data.append({"employee_name": _("Total Employees"), "count": total_employees})
    data.append({"employee_name": _("Total Dependents"), "count": total_dependents})
    data.append({"employee_name": _("Total Members"), "count": total_members})

    report_summary = [
        {"label": _("Total Employees"), "value": total_employees, "indicator": "Blue"},
        {"label": _("Total Dependents"), "value": total_dependents, "indicator": "Orange"},
        {"label": _("Total Members"), "value": total_members, "indicator": "Green"},
    ]

    return get_columns(), data, None, None, report_summary


def get_columns():
    return [
        {"label": _("Employee Code"), "fieldname": "employee_code", "fieldtype": "Data", "width": 210},
        {"label": _("Employee Name"), "fieldname": "employee_name", "fieldtype": "Data", "width": 260},
        {"label": _("Corporate Name"), "fieldname": "corporate_name", "fieldtype": "Data", "width": 250},
        {"label": _("Policy No"), "fieldname": "policy_no", "fieldtype": "Data", "width": 250},
        {"label": _("Policy Effective Date"), "fieldname": "policy_effective_date", "fieldtype": "Date", "width": 230},
        {"label": _("Company Date of Joining"), "fieldname": "company_doj", "fieldtype": "Date", "width": 230},
        {"label": _("Date of Internship"), "fieldname": "date_of_internship", "fieldtype": "Date", "width": 210},
        {"label": _("Dependant Name"), "fieldname": "dependant_name", "fieldtype": "Data", "width": 260},
        {"label": _("Relation"), "fieldname": "relation", "fieldtype": "Data", "width": 190},
        {"label": _("Gender"), "fieldname": "gender", "fieldtype": "Link", "options": "Gender", "width": 190},
        {"label": _("Date of Birth"), "fieldname": "date_of_birth", "fieldtype": "Date", "width": 200},
        {"label": _("Age (Years)"), "fieldname": "age", "fieldtype": "Int", "width": 150},
        {"label": _("Sum Insured"), "fieldname": "sum_insured", "fieldtype": "Data", "width": 200},
        {"label": _("Mobile No."), "fieldname": "mobile_no", "fieldtype": "Data", "width": 210},
        {"label": _("Employee's E-mail Id"), "fieldname": "email", "fieldtype": "Data", "width": 260},
        {"label": _("Location"), "fieldname": "location", "fieldtype": "Data", "width": 200},
        {"label": _("Member Type"), "fieldname": "member_type", "fieldtype": "Data", "width": 170},
        {"label": _("Grade"), "fieldname": "grade", "fieldtype": "Link", "options": "Employee Grade", "width": 150},
        {"label": _("Designation"), "fieldname": "designation", "fieldtype": "Link", "options": "Designation", "width": 220},
        {"label": _("Salary Account No"), "fieldname": "salary_account_no", "fieldtype": "Data", "width": 220},
        {"label": _("MICR"), "fieldname": "micr_code", "fieldtype": "Data", "width": 190},
        {"label": _("IFSC"), "fieldname": "ifsc_code", "fieldtype": "Data", "width": 190},
        {"label": _("Bank Name"), "fieldname": "bank_name", "fieldtype": "Data", "width": 200},
        {"label": _("Account Type"), "fieldname": "account_type", "fieldtype": "Data", "width": 190},
        {"label": _("Bank Address"), "fieldname": "bank_address", "fieldtype": "Data", "width": 200},
        {"label": _("Bank Contact No"), "fieldname": "bank_contact_no", "fieldtype": "Data", "width": 190},
        {"label": _("Name as Per Bank Account"), "fieldname": "name_as_per_bank", "fieldtype": "Data", "width": 220},
        {"label": _("Member Effective Date"), "fieldname": "member_effective_date", "fieldtype": "Date", "width": 210},
        {"label": _("Deletion Date"), "fieldname": "deletion_date", "fieldtype": "Date", "width": 190},
        {"label": _("Count"), "fieldname": "count", "fieldtype": "Int", "width": 150},
    ]


def get_data(filters):
    conditions, values = [], {}

    if filters.get("from_date"):
        conditions.append("e.date_of_joining >= %(from_date)s")
        values["from_date"] = filters["from_date"]
    if filters.get("to_date"):
        conditions.append("e.date_of_joining <= %(to_date)s")
        values["to_date"] = filters["to_date"]

    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""

    return frappe.db.sql(f"""
        SELECT COALESCE(NULLIF(TRIM(e.employee_number), ''), e.name) AS employee_code,
               e.employee_name, e.company AS corporate_name, e.custom_policy_no AS policy_no,
               e.custom_policy_effective_date AS policy_effective_date,
               e.date_of_joining AS company_doj,
               e.custom_date_of_internship AS date_of_internship,
               mm.member_name AS dependant_name, mm.relation, mm.gender, mm.date_of_birth,
               mm.effective_date AS member_effective_date,
               e.relieving_date AS deletion_date,
               e.cell_number AS mobile_no, e.company_email AS email,
               e.grade, e.designation, e.bank_ac_no AS salary_account_no,
               e.micr_code, e.ifsc_code, e.bank_name
        FROM `tabEmployee` e
        JOIN `tabMediclaim Member` mm ON mm.parent = e.name AND mm.parenttype = 'Employee'
        {where}
        ORDER BY e.employee_name, mm.relation
    """, values, as_dict=True)