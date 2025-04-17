
# Employee Insights

## Overview
Employee Insights is a web application that provides insights into employee data. It includes features for viewing employee details, tasks, performance, projects, and more. It is built using Flask and PostgreSQL, with REST API endpoints that allow for easy interaction with the data. The application also integrates Swagger UI for interactive API documentation.

## Features
- REST API for employee management (including filtering and pagination)
- Authentication using Basic Auth
- Dashboard with employee insights visualization
- Export employee data to CSV/Excel
- Swagger UI for API documentation

## Setup Instructions

### Prerequisites
- Python 3.8+
- PostgreSQL database running locally or remotely

### Installation Steps
1. Clone the repository:
   ```bash
   git clone <your-repository-url>
   cd employee-insights
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables in a `.env` file. The environment configuration should be as follows:
   ```bash
   DATABASE_URI=postgresql://username:password@localhost:5432/employee_db
   FLASK_APP=run.py
   FLASK_ENV=development
   ```

4. Set up the PostgreSQL database (if not already set up):
   - Create a database named `employee_db` and provide the necessary permissions for the `username`.
   - Ensure that the database is running and accessible via the `DATABASE_URI`.

5. Initialize the database and generate fake data:
   ```bash
   python run.py
   ```

### Running the Application
Once the setup is complete, run the Flask application:
```bash
python run.py
```

This will start the Flask application locally, and you can access it at:
- API Documentation: `http://localhost:5000/apidocs/#/`
- Employee API: `http://localhost:5000/employees`

### Authentication
Basic authentication is required for accessing the API endpoints. Use the following credentials:
- Username: `admin`
- Password: `password`

## Swagger UI
- The Swagger UI is available at the `/apidocs/#/` endpoint. This provides an interactive interface to explore the API.

## Dependencies
- Flask
- SQLAlchemy
- PostgreSQL
- Faker (for generating fake data)
- Basic Auth (for authentication)
- flask-swagger-ui (for API documentation)

### .env Configuration
- **DATABASE_URI**: PostgreSQL database URI.
- **FLASK_APP**: The entry point of the Flask application.
- **FLASK_ENV**: The environment mode (development, production).

## Folder Structure
```bash
employee_project/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── schemas.py
│   ├── utils.py
├── migrations/
├── .env
├── run.py
├── requirements.txt
└── README.md
```

## Future Improvements ()

- **Authentication Enhancement**: Switch to JWT or OAuth2 for token-based authentication.
- **Asynchronous Processing**: Use Celery for background task processing, especially for long-running tasks like data generation and report export.
- **Rate Limiting**: Implement rate limiting to prevent abuse and ensure fair usage of the API.
- **Unit and Integration Tests**: Write tests to ensure the API works as expected and is production-ready.

## License
This project is open-source and available under the MIT License.

