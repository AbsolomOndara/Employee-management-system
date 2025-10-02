// Tab switching functionality
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tab system
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabId = btn.getAttribute('data-tab');
            
            // Update active tab button
            tabBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            // Show active tab content
            tabContents.forEach(content => content.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
        });
    });
    
    // Load employees on page load
    loadEmployees();
    
    // Form submissions
    document.getElementById('addEmployeeForm').addEventListener('submit', addEmployee);
    document.getElementById('editEmployeeForm').addEventListener('submit', updateEmployee);
});

// Load all employees
async function loadEmployees() {
    try {
        const response = await fetch('/api/employees');
        const employees = await response.json();
        
        displayEmployees(employees);
        updateEmployeeCount(employees.length);
    } catch (error) {
        showNotification('Error loading employees', 'error');
    }
}

// Display employees in formatted cards
function displayEmployees(employees) {
    const container = document.getElementById('employeesList');
    
    if (employees.length === 0) {
        container.innerHTML = '<div class="no-data">No employees found</div>';
        return;
    }
    
    container.innerHTML = employees.map(employee => `
        <div class="employee-card">
            <div class="employee-header">${employee.name}</div>
            <div class="employee-details">
                <div class="detail-item">
                    <div class="detail-label">SSN</div>
                    <div class="detail-value">${employee.ssn}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Phone</div>
                    <div class="detail-value">${employee.phone}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Email</div>
                    <div class="detail-value">${employee.email}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Salary</div>
                    <div class="detail-value">$${employee.salary}</div>
                </div>
            </div>
        </div>
    `).join('');
}

// Update employee count display
function updateEmployeeCount(count) {
    document.getElementById('employeeCount').textContent = count;
}

// Search employee by SSN
async function searchEmployee() {
    const ssn = document.getElementById('searchSSN').value.trim();
    
    if (!ssn) {
        showNotification('Please enter an SSN', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/employees/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ ssn: ssn })
        });
        
        const result = await response.json();
        const container = document.getElementById('searchResults');
        
        if (result.found) {
            container.innerHTML = `
                <div class="employee-card">
                    <div class="employee-header">${result.employee.name}</div>
                    <div class="employee-details">
                        <div class="detail-item">
                            <div class="detail-label">SSN</div>
                            <div class="detail-value">${result.employee.ssn}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Phone</div>
                            <div class="detail-value">${result.employee.phone}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Email</div>
                            <div class="detail-value">${result.employee.email}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Salary</div>
                            <div class="detail-value">$${result.employee.salary}</div>
                        </div>
                    </div>
                </div>
            `;
            showNotification('Employee found!', 'success');
        } else {
            container.innerHTML = '<div class="no-data">No employee found with that SSN</div>';
            showNotification('Employee not found', 'error');
        }
    } catch (error) {
        showNotification('Error searching for employee', 'error');
    }
}

// Find employee for editing
async function findEmployeeToEdit() {
    const ssn = document.getElementById('editSearchSSN').value.trim();
    
    if (!ssn) {
        showNotification('Please enter an SSN', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/employees/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ ssn: ssn })
        });
        
        const result = await response.json();
        
        if (result.found) {
            document.getElementById('editName').value = result.employee.name;
            document.getElementById('editSSN').value = result.employee.ssn;
            document.getElementById('editPhone').value = result.employee.phone;
            document.getElementById('editEmail').value = result.employee.email;
            document.getElementById('editSalary').value = result.employee.salary;
            
            document.getElementById('editEmployeeForm').style.display = 'block';
            document.getElementById('editEmployeeForm').dataset.oldSsn = result.employee.ssn;
            
            showNotification('Employee found! You can now edit the information.', 'success');
        } else {
            showNotification('Employee not found', 'error');
            document.getElementById('editEmployeeForm').style.display = 'none';
        }
    } catch (error) {
        showNotification('Error finding employee', 'error');
    }
}

// Update employee information
async function updateEmployee(event) {
    event.preventDefault();
    
    const form = event.target;
    const oldSsn = form.dataset.oldSsn;
    
    const employeeData = {
        old_ssn: oldSsn,
        name: document.getElementById('editName').value,
        ssn: document.getElementById('editSSN').value,
        phone: document.getElementById('editPhone').value,
        email: document.getElementById('editEmail').value,
        salary: document.getElementById('editSalary').value
    };
    
    try {
        const response = await fetch('/api/employees/edit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(employeeData)
        });
        
        if (response.ok) {
            showNotification('Employee updated successfully!', 'success');
            form.reset();
            form.style.display = 'none';
            loadEmployees(); // Refresh the employee list
        } else {
            const error = await response.json();
            showNotification(error.error, 'error');
        }
    } catch (error) {
        showNotification('Error updating employee', 'error');
    }
}

// Add new employee
async function addEmployee(event) {
    event.preventDefault();
    
    const form = event.target;
    const employeeData = {
        name: document.getElementById('addName').value,
        ssn: document.getElementById('addSSN').value,
        phone: document.getElementById('addPhone').value,
        email: document.getElementById('addEmail').value,
        salary: document.getElementById('addSalary').value
    };
    
    try {
        const response = await fetch('/api/employees/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(employeeData)
        });
        
        if (response.ok) {
            showNotification('Employee added successfully!', 'success');
            form.reset();
            loadEmployees(); // Refresh the employee list
            
            // Switch to view tab to see the new employee
            document.querySelector('[data-tab="view"]').click();
        } else {
            const error = await response.json();
            showNotification(error.error, 'error');
        }
    } catch (error) {
        showNotification('Error adding employee', 'error');
    }
}

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = `notification ${type} show`;
    
    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}