def serialize_employee(emp):
    return {
        'id': emp.id,
        'name': f'{emp.first_name} {emp.last_name}',
        'email': emp.email,
        'department': emp.department,
        'job_title': emp.job_title
    }

def serialize_employee_detail(emp):
    return {
        'id': emp.id,
        'name': f'{emp.first_name} {emp.last_name}',
        'email': emp.email,
        'department': emp.department,
        'job_title': emp.job_title,
        'phone': emp.phone_number,
        'hire_date': str(emp.hire_date),
        'tasks': [
            {
                'task_name': t.task_name,
                'status': t.status,
                'due_date': str(t.due_date)
            } for t in emp.tasks
        ],
        'projects': [
            {
                'project_name': p.project_name,
                'role': p.role,
                'start_date': str(p.start_date),
                'end_date': str(p.end_date) if p.end_date else None
            } for p in emp.projects
        ],
        'performance_reviews': [
            {
                'rating': perf.rating,
                'feedback': perf.feedback,
                'review_date': str(perf.review_date)
            } for perf in emp.performances
        ]
    }

from app.models import Employee, Performance, EmployeeTask
from sqlalchemy import func
from app import db

def get_dashboard_summary():
    total_employees = Employee.query.count()

    dept_counts = db.session.query(Employee.department, func.count()).group_by(Employee.department).all()
    avg_rating = db.session.query(func.avg(Performance.rating)).scalar()

    task_status_counts = db.session.query(EmployeeTask.status, func.count()).group_by(EmployeeTask.status).all()

    return {
        'total_employees': total_employees,
        'employees_per_department': {dept: count for dept, count in dept_counts},
        'average_performance_rating': round(avg_rating, 2) if avg_rating else None,
        'tasks_by_status': {status: count for status, count in task_status_counts}
    }
