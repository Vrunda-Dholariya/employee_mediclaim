# Employee Mediclaim

A Frappe app that adds Mediclaim details to the Employee record in ERPNext/HRMS.

## What it includes
- A **Mediclaim** tab on the Employee DocType (custom fields, exported as fixtures)
- **Mediclaim** and **Mediclaim Member** DocTypes (Mediclaim Member is a child table)
- **Employee Mediclaim Report** and **Employee Mediclaim Report 2**, script reports with multiple filters

## Requirements
- Frappe / ERPNext v16
- HRMS

## Installation
    bench get-app <repo-url>
    bench --site <site-name> install-app employee_mediclaim
    bench --site <site-name> migrate

For Docker setups, add this repo to `apps.json` and build a custom image.

## License
MIT
