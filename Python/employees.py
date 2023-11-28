import pandas as pd

# Read office addresses
office_addresses = pd.read_csv('datasets/office_addresses.csv')

# Read employee addresses
employee_addresses_cols = ["employee_id", "employee_country", "employee_city", "employee_street", "employee_street_number"]
employee_addresses = pd.read_excel('datasets/employee_information.xlsx', sheet_name=0, usecols=employee_addresses_cols)

# Read employee emergency contacts
emergency_contacts_header = ["employee_id", "last_name", "first_name", "emergency_contact", "emergency_contact_number", "relationship"]
emergency_contacts = pd.read_excel('datasets/employee_information.xlsx', sheet_name="emergency_contacts", header=None, names=emergency_contacts_header)

# Read employee roles
employee_roles = pd.read_json('datasets/employee_roles.json', orient="index")

# Merge employee addresses with office addresses
employees = employee_addresses.merge(office_addresses, left_on='employee_country', right_on='office_country', how='left')

# Merge employee data with roles
employees = employees.merge(employee_roles, left_on='employee_id', right_index=True)

# Merge employee data with emergency contacts
employees = employees.merge(emergency_contacts, on='employee_id')

# Fill missing values with 'Remote'
employees.fillna('Remote', inplace=True)

# Define the desired column order
final_columns = ['employee_id', 'first_name', 'last_name', 'employee_country', 'employee_city', 'employee_street', 'employee_street_number', 'emergency_contact', 'emergency_contact_number', 'relationship', 'monthly_salary', 'team', 'title', 'office', 'office_country', 'office_city', 'office_street', 'office_street_number']

# Create the final dataframe with the desired column order
employees_final = employees[final_columns]

# Set employee_id as the index
employees_final.set_index('employee_id', inplace=True)