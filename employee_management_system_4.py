"""
Employee Management System - Functionality 4
Author: [Your Name]
Course: CPT 200 - Fundamentals of Programming Languages
Description: 
- Enhanced employee management system with improved display formatting
- Search employees by SSN functionality
- Edit employee information functionality
- Uses lists and dictionaries for data storage
"""

employees = []

def initialize_sample_data():
    """Initialize the system with sample employee data"""
    global employees
    if not employees:
        sample_employees = [
            {
                "name": "Mike Smith",
                "ssn": "123123123",
                "phone": "111-222-3333",
                "email": "mike@gmail.com",
                "salary": 6000
            },
            {
                "name": "Sara Smith", 
                "ssn": "123123111",
                "phone": "111-222-4444",
                "email": "sara@gmail.com",
                "salary": 6500
            },
            {
                "name": "John Davis",
                "ssn": "123123222",
                "phone": "111-222-5555",
                "email": "john@gmail.com",
                "salary": 7000
            }
        ]
        employees.extend(sample_employees)

def display_employee_formatted(employee):
    """
    Display a single employee in the required formatted style
    """
    # function for creating header with employee name centered
    header = f"---------------------------- {employee['name']} -----------------------------"
    print(header)
    print(f"SSN: {employee['ssn']}")
    print(f"Phone: {employee['phone']}")
    print(f"Email: {employee['email']}")
    print(f"Salary: ${employee['salary']}")
    print("-" * len(header))
    print()

def view_all_employees():
    """
    Display all employees in the new formatted style
    Improved from Week 3 functionality
    """
    if not employees:
        print("No employees found in the system.")
        return
    
    print(f"\nDisplaying all {len(employees)} employees:\n")
    for employee in employees:
        display_employee_formatted(employee)

def search_employee_by_ssn():
    """
    Search for an employee by SSN using looping and string parsing
    Returns the employee dictionary if found, None otherwise
    """
    if not employees:
        print("No employees in the system to search.")
        return None
    
    ssn_to_search = input("Enter SSN to search for: ").strip()
    
    # loop for searching through all employees
    for employee in employees:
        # a string for parsing and comparing SSN values
        if employee['ssn'] == ssn_to_search:
            print("\nEmployee found:")
            display_employee_formatted(employee)
            return employee
    
    print("No employee found with that SSN.")
    return None

def edit_employee_information():
    """
    Edit employee information by first searching with SSN
    Uses the search_employee_by_ssn function to find the employee
    """
    print("\n--- Edit Employee Information ---")
    
    # functon for finding new em,ployee
    employee = search_employee_by_ssn()
    
    if employee is None:
        return  # No employee found to edit
    
    print("\nEditing employee information. Press Enter to keep current value.")
    
    # function for getting new values for each field
    new_name = input(f"Enter new name [{employee['name']}]: ").strip()
    new_ssn = input(f"Enter new SSN [{employee['ssn']}]: ").strip()
    new_phone = input(f"Enter new phone [{employee['phone']}]: ").strip()
    new_email = input(f"Enter new email [{employee['email']}]: ").strip()
    new_salary = input(f"Enter new salary [${employee['salary']}]: ").strip()
    
    # function for updating fields if new values provided
    if new_name:
        employee['name'] = new_name
    if new_ssn:
        employee['ssn'] = new_ssn
    if new_phone:
        employee['phone'] = new_phone
    if new_email:
        employee['email'] = new_email
    if new_salary:
        try:
            employee['salary'] = float(new_salary.replace('$', '').strip())
        except ValueError:
            print("Invalid salary format. Salary not updated.")
    
    print("\nEmployee information updated successfully!")
    print("Updated employee information:")
    display_employee_formatted(employee)

def add_new_employee():
    """
    Add a new employee to the system
    Enhanced from previous functionality
    """
    print("\n--- Add New Employee ---")
    
    name = input("Enter employee name: ").strip()
    ssn = input("Enter employee SSN: ").strip()
    phone = input("Enter employee phone: ").strip()
    email = input("Enter employee email: ").strip()
    
    try:
        salary = float(input("Enter employee salary: ").strip())
    except ValueError:
        print("Invalid salary entered. Please enter a numeric value.")
        return
    
    # fucntion for checking for duplicate SSN
    for employee in employees:
        if employee['ssn'] == ssn:
            print("An employee with this SSN already exists.")
            return
    
    # functon for creating new employee dictionary
    new_employee = {
        "name": name,
        "ssn": ssn,
        "phone": phone,
        "email": email,
        "salary": salary
    }
    
    employees.append(new_employee)
    print(f"\nEmployee '{name}' added successfully!")

def display_menu():
    """
    Display the main menu options
    """
    print("\n" + "="*50)
    print("      EMPLOYEE MANAGEMENT SYSTEM - FUNCTIONALITY 4")
    print("="*50)
    print(f"Current number of employees: {len(employees)}")
    print("\nMain Menu:")
    print("1. View All Employees")
    print("2. Search Employee by SSN")
    print("3. Edit Employee Information")
    print("4. Add New Employee")
    print("5. Exit")
    print("="*50)

def main():
    """
    Main function to run the Employee Management System
    """
    print("Welcome to the Employee Management System")
    print("Initializing with sample data...")
    
    initialize_sample_data()
    
    while True:
        display_menu()
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            view_all_employees()
        elif choice == '2':
            search_employee_by_ssn()
        elif choice == '3':
            edit_employee_information()
        elif choice == '4':
            add_new_employee()
        elif choice == '5':
            print("\nThank you for using the Employee Management System!")
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()