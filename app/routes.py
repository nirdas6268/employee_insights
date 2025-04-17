from flask import Blueprint, jsonify, request, abort
from app.models import Employee, EmployeeTask, EmployeeProject, Performance
from app.schemas import serialize_employee, serialize_employee_detail, get_dashboard_summary
from app import db
from functools import wraps
from flasgger import swag_from  # ✅ Add this

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
@swag_from({
    'responses': {
        200: {
            'description': 'API Welcome Message',
            'examples': {
                'application/json': {
                    'message': 'Welcome to the Employee Insights API!'
                }
            }
        }
    }
})
def index():
    return jsonify(message="Welcome to the Employee Insights API!")

# ✅ GET All Employees with Pagination & Filtering
@employee_bp.route('/employees', methods=['GET'])
@require_auth
@swag_from({
    'parameters': [
        {
            'name': 'page',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'description': 'Page number for pagination'
        },
        {
            'name': 'per_page',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'description': 'Number of items per page'
        },
        {
            'name': 'department',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'Filter by department name'
        }
    ],
    'responses': {
        200: {
            'description': 'List of employees with pagination',
        },
        401: {
            'description': 'Authentication failed'
        }
    }
})
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

# ✅ GET Employee Details
@employee_bp.route('/employees/<int:employee_id>', methods=['GET'])
@require_auth
@swag_from({
    'parameters': [
        {
            'name': 'employee_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'Employee ID'
        }
    ],
    'responses': {
        200: {
            'description': 'Detailed employee info'
        },
        404: {
            'description': 'Employee not found'
        }
    }
})
def get_employee_detail(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    return jsonify(serialize_employee_detail(employee))

# ✅ Dashboard Summary (for visualization)
@employee_bp.route('/dashboard', methods=['GET'])
@require_auth
@swag_from({
    'responses': {
        200: {
            'description': 'Summary data for visualization'
        },
        401: {
            'description': 'Authentication failed'
        }
    }
})
def get_dashboard():
    summary = get_dashboard_summary()
    return jsonify(summary)
