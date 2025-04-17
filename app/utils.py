from app import db
from app.models import Employee, Performance, EmployeeTask, EmployeeProject
import random
from faker import Faker

fake = Faker()

def generate_fake_data():
    # Generate 5 fake employees
    for _ in range(5):
        employee = Employee()
        employee.generate_fake_employee()
        db.session.add(employee)
        db.session.commit()  # Commit the employee first so employee.id is available

        # Generate fake tasks for each employee (3 to 5 tasks)
        num_tasks = random.randint(3, 5)
        for _ in range(num_tasks):
            task = EmployeeTask(
                task_name=fake.bs(),  # Random task description
                status=random.choice(['Pending', 'In Progress', 'Completed']),
                due_date=fake.date_this_year(),
                employee_id=employee.id  # Now employee.id will be correctly set
            )
            db.session.add(task)

        # Generate fake projects for each employee (2 to 3 projects)
        num_projects = random.randint(2, 3)
        for _ in range(num_projects):
            project = EmployeeProject(
                project_name=fake.company(),
                role=fake.job(),
                start_date=fake.date_this_decade(),
                end_date=fake.date_this_decade() if random.choice([True, False]) else None,
                employee_id=employee.id  # Now employee.id will be correctly set
            )
            db.session.add(project)

        # Generate fake performance reviews for each employee (2 to 3 reviews)
        num_performance_reviews = random.randint(2, 3)
        for _ in range(num_performance_reviews):
            performance = Performance(
                rating=random.randint(1, 5),
                feedback=fake.text(),
                employee_id=employee.id
            )
            db.session.add(performance)

    db.session.commit()  # Commit all changes at once
    print("Fake employee data generated!")
