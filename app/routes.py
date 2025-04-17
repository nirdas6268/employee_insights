from flask import Blueprint, jsonify, request, abort
from app.models import Employee, EmployeeTask, EmployeeProject, Performance
from app.schemas import serialize_employee, serialize_employee_detail, get_dashboard_summary
from app import db
from functools import wraps
from flask import request
import base64

employee_bp = Blueprint('employee_bp', __name__)

# Basic Auth decorator
def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not (auth.username == 'admin' and auth.password == 'password'):
            return abort(401, description="Authentication Required")
        return f(*args, **kwargs)
    return decorated

@employee_bp.route('/')
def index():
    return jsonify(message="Welcome to the Employee Insights API!")

# ✅ GET All Employees with Pagination & Filtering
@employee_bp.route('/employees', methods=['GET'])
@require_auth
def get_employees():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    department = request.args.get('department')

    query = Employee.query
    if department:
        query = query.filter(Employee.department.ilike(f'%{department}%'))

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    employees = [serialize_employee(emp) for emp in pagination.items]

    return jsonify({
        'employees': employees,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page
    })

# ✅ GET Employee Details with Related Info
@employee_bp.route('/employees/<int:employee_id>', methods=['GET'])
@require_auth
def get_employee_detail(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    return jsonify(serialize_employee_detail(employee))

# ✅ Visualization Endpoint (Dashboard Summary)
@employee_bp.route('/dashboard', methods=['GET'])
@require_auth
def get_dashboard():
    summary = get_dashboard_summary()
    return jsonify(summary)
