from app import create_app, db
from app.utils import generate_fake_data

app = create_app()

def setup_database():
    with app.app_context():  # Push the application context
        db.create_all()  # Create tables
        generate_fake_data()  # Generate fake data

if __name__ == '__main__':
    setup_database()  # Call the setup function to initialize DB and data
    app.run(debug=True)  # Start the Flask app
