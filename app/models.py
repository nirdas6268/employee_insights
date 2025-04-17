from datetime import datetime
from app import db
from faker import Faker

fake = Faker()

# Employee Model
class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    job_title = db.Column(db.String(100))
    phone_number = db.Column(db.String(50))
    hire_date = db.Column(db.Date)
    department = db.Column(db.String(50))

    # Relationship with EmployeeTask
    tasks = db.relationship('EmployeeTask', backref='employee', lazy=True)
    
    # Relationship with EmployeeProject
    projects = db.relationship('EmployeeProject', backref='employee', lazy=True)
    
    # Relationship with Performance
    performances = db.relationship('Performance', backref='employee', lazy=True)

    def __repr__(self):
        return f'<Employee {self.first_name} {self.last_name}>'

    def generate_fake_employee(self):
        self.first_name = fake.first_name()
        self.last_name = fake.last_name()
        self.email = fake.email()
        self.job_title = fake.job()
        self.phone_number = fake.phone_number()
        self.hire_date = fake.date_this_decade()
        self.department = fake.company()

# EmployeeTask Model
class EmployeeTask(db.Model):
    __tablename__ = 'employee_tasks'

    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(100))
    status = db.Column(db.String(50))  # e.g., 'Pending', 'In Progress', 'Completed'
    due_date = db.Column(db.Date)

    # Foreign Key linking to Employee
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)

    def __repr__(self):
        return f'<EmployeeTask {self.task_name} for Employee {self.employee_id}>'

# EmployeeProject Model
class EmployeeProject(db.Model):
    __tablename__ = 'employee_projects'

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100))
    role = db.Column(db.String(100))  # e.g., 'Developer', 'Manager'
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date, nullable=True)

    # Foreign Key linking to Employee
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)

    def __repr__(self):
        return f'<EmployeeProject {self.project_name} with Role {self.role}>'

# Performance Model
class Performance(db.Model):
    __tablename__ = 'performances'

    id = db.Column(db.Integer, primary_key=True)
    review_date = db.Column(db.Date, default=datetime.utcnow)
    rating = db.Column(db.Integer)  # 1-5 scale
    feedback = db.Column(db.String(500))

    # Foreign Key linking to Employee
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)

    def __repr__(self):
        return f'<Performance {self.rating} on {self.review_date}>'

# Data generation for Tasks, Projects, and Performance
def generate_fake_data():
    # Get all employees
    employees = Employee.query.all()
    
    # For each employee, generate task and project records
    for employee in employees:
        # Generate tasks
        num_tasks = fake.random_int(min=3, max=5)
        for _ in range(num_tasks):
            task = EmployeeTask(
                employee_id=employee.id,
                task_name=fake.bs(),  # Generate a task name 
                status=fake.random_element(elements=('Pending', 'In Progress', 'Completed')),
                due_date=fake.date_this_year()  # Assign a random due date
            )
            db.session.add(task)
        
        # Generate projects (e.g., 2 to 3 projects)
        num_projects = fake.random_int(min=2, max=3)
        for _ in range(num_projects):
            project = EmployeeProject(
                employee_id=employee.id,
                project_name=fake.company(),  # Generate a project name (random company name)
                role=fake.job(),
                start_date=fake.date_this_decade(),
                end_date=fake.date_this_decade() if fake.boolean() else None  # End date is optional
            )
            db.session.add(project)

        # Generate performance reviews (e.g., 1 to 2 reviews per employee)
        num_reviews = fake.random_int(min=1, max=2)
        for _ in range(num_reviews):
            performance = Performance(
                employee_id=employee.id,
                rating=fake.random_int(min=1, max=5),
                feedback=fake.sentence(),
                review_date=fake.date_this_decade()
            )
            db.session.add(performance)

    # Commit once after all employees' data is inserted
    db.session.commit()
