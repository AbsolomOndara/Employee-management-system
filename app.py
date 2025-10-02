from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Initialize employee data
employees = [
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/employees', methods=['GET'])
def get_employees():
    return jsonify(employees)

@app.route('/api/employees/add', methods=['POST'])
def add_employee():
    data = request.json
    new_employee = {
        "name": data['name'],
        "ssn": data['ssn'],
        "phone": data['phone'],
        "email": data['email'],
        "salary": float(data['salary'])
    }
    
    # Check for duplicate SSN
    for employee in employees:
        if employee['ssn'] == new_employee['ssn']:
            return jsonify({"error": "Employee with this SSN already exists"}), 400
    
    employees.append(new_employee)
    return jsonify({"message": "Employee added successfully", "employee": new_employee})

@app.route('/api/employees/search', methods=['POST'])
def search_employee():
    data = request.json
    ssn = data['ssn']
    
    for employee in employees:
        if employee['ssn'] == ssn:
            return jsonify({"found": True, "employee": employee})
    
    return jsonify({"found": False, "message": "No employee found with that SSN"})

@app.route('/api/employees/edit', methods=['POST'])
def edit_employee():
    data = request.json
    old_ssn = data['old_ssn']
    
    # Find employee
    for i, employee in enumerate(employees):
        if employee['ssn'] == old_ssn:
            # Update employee data
            employees[i] = {
                "name": data['name'],
                "ssn": data['ssn'],
                "phone": data['phone'],
                "email": data['email'],
                "salary": float(data['salary'])
            }
            return jsonify({"message": "Employee updated successfully", "employee": employees[i]})
    
    return jsonify({"error": "Employee not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)