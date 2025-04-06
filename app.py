from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager
from flask_mail import Mail, Message
from flask_cors import CORS
from datetime import datetime

from models import Application, EducationalBackground, WorkExperience, ComputerLiteracy, db
from flask_migrate import Migrate
import logging

# Initialize extensions
jwt = JWTManager()
mail = Mail()

def create_app():
    app = Flask(__name__)

    # App configuration
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///applications.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret'

    # Mail configuration
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'youmingtechnologies@gmail.com'  # Change to your email
    app.config['MAIL_PASSWORD'] = 'dqolkusklogpmhmo'  # Use an App Password
    app.config['MAIL_DEFAULT_SENDER'] = 'youmingtechnologies@gmail.com'  # Change to your email

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    CORS(app)
    migrate = Migrate(app, db)

    # Create tables
    with app.app_context():
        db.create_all()

    # Configure logging
    logging.basicConfig(level=logging.ERROR)

    # Helper function to send email to the company
    def send_email(data):
        receiver_email = "youmingtechnologies@gmail.com"  # Replace with company email

        # Create email content
        message = Message(
            "New Pre-Admission Questionnaire Submission",
            recipients=[receiver_email]
        )
        message.html = f"""
        <html>
            <body>
                <h2>New Application Received</h2>
                <p><strong>Full Name:</strong> {data['full_names']}</p>
                <p><strong>Date of Birth:</strong> {data['date_of_birth']}</p>
                <p><strong>County of Residence:</strong> {data['county_of_residence']}</p>
                <p><strong>Town:</strong> {data['town']}</p>
                <p><strong>Email Address:</strong> {data['email_address']}</p>
                <p><strong>Phone Number:</strong> {data['phone_number']}</p>
                <p><strong>WhatsApp Number:</strong> {data['whatsapp_number']}</p>
                <p><strong>Bio:</strong> {data['bio']}</p>
                <h3>Educational Background</h3>
                {format_list(data['educational_background'])}
                <h3>Work Experience</h3>
                {format_list(data['work_experience'])}
                <h3>Computer Literacy</h3>
                {format_list(data['computer_literacy'])}
            </body>
        </html>
        """

        try:
            mail.send(message)
            return True
        except Exception as e:
            logging.error(f"Failed to send email: {str(e)}")
            return False

    # Helper function to send confirmation email to the sender
    def send_confirmation_email(sender_email):
        # Create email content for the sender
        message = Message(
            "Application Submission Confirmation",
            recipients=[sender_email]
        )
        message.html = """
        <html>
            <body>
                <h2>Thank You for Your Submission!</h2>
                <p>We have successfully received your application.</p>
                <p>You will receive a response from us within 3 business days.</p>
                <p>If you have any questions, feel free to contact us.</p>
            </body>
        </html>
        """

        try:
            mail.send(message)
            return True
        except Exception as e:
            logging.error(f"Failed to send confirmation email: {str(e)}")
            return False

    # Helper function to format lists into HTML
    def format_list(items):
        if not items:
            return "<p>No data provided.</p>"
        html = "<ul>"
        for item in items:
            html += f"<li>{item}</li>"
        html += "</ul>"
        return html

    # API endpoint to submit the questionnaire
    @app.route('/submit', methods=['POST'])
    def submit():
        try:
            # Extract JSON data from the request
            data = request.get_json()

            # Validate required fields
            required_fields = [
                'full_names', 'date_of_birth', 'county_of_residence', 'town',
                'email_address', 'phone_number', 'whatsapp_number', 'bio',
                'educational_background', 'work_experience', 'computer_literacy'
            ]
            for field in required_fields:
                if field not in data:
                    return jsonify({"error": f"Missing field: {field}"}), 400

            # Parse dates
            try:
                date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d')
            except ValueError:
                return jsonify({"error": "Invalid date format for date_of_birth. Use YYYY-MM-DD."}), 400

            # Create new application
            new_application = Application(
                full_names=data['full_names'],
                date_of_birth=date_of_birth,
                county_of_residence=data['county_of_residence'],
                town=data['town'],
                email_address=data['email_address'],
                phone_number=data['phone_number'],
                whatsapp_number=data['whatsapp_number'],
                bio=data['bio']
            )
            db.session.add(new_application)
            db.session.flush()  # Flush to get the application ID

            # Add educational background entries
            for entry in data['educational_background']:
                try:
                    duration_from = datetime.strptime(entry['duration_from'], '%Y-%m-%d')
                    duration_to = datetime.strptime(entry['duration_to'], '%Y-%m-%d')
                except ValueError:
                    return jsonify({"error": "Invalid date format in educational_background. Use YYYY-MM-DD."}), 400

                new_educational_entry = EducationalBackground(
                    application_id=new_application.id,
                    level_of_academic=entry['level_of_academic'],
                    major=entry['major'],
                    institution_attended=entry['institution_attended'],
                    duration_from=duration_from,
                    duration_to=duration_to
                )
                db.session.add(new_educational_entry)

            # Add work experience entries
            for entry in data['work_experience']:
                try:
                    duration_from = datetime.strptime(entry['duration_from'], '%Y-%m-%d')
                    duration_to = datetime.strptime(entry['duration_to'], '%Y-%m-%d')
                except ValueError:
                    return jsonify({"error": "Invalid date format in work_experience. Use YYYY-MM-DD."}), 400

                new_work_experience_entry = WorkExperience(
                    application_id=new_application.id,
                    nature_of_work=entry['nature_of_work'],
                    designation=entry['designation'],
                    employer_entity=entry['employer_entity'],
                    duration_from=duration_from,
                    duration_to=duration_to
                )
                db.session.add(new_work_experience_entry)

            # Add computer literacy entries
            for entry in data['computer_literacy']:
                try:
                    duration_from = datetime.strptime(entry['duration_from'], '%Y-%m-%d')
                    duration_to = datetime.strptime(entry['duration_to'], '%Y-%m-%d')
                except ValueError:
                    return jsonify({"error": "Invalid date format in computer_literacy. Use YYYY-MM-DD."}), 400

                new_computer_literacy_entry = ComputerLiteracy(
                    application_id=new_application.id,
                    level_of_computer_literacy=entry['level_of_computer_literacy'],
                    course_name=entry['course_name'],
                    institution_attended=entry['institution_attended'],
                    duration_from=duration_from,
                    duration_to=duration_to
                )
                db.session.add(new_computer_literacy_entry)

            # Commit everything to the database
            db.session.commit()

            # Send email notification to the company
            if not send_email(data):
                return jsonify({"error": "Failed to send email notification to the company."}), 500

            # Send confirmation email to the sender
            if not send_confirmation_email(data['email_address']):
                return jsonify({"error": "Failed to send confirmation email to the sender."}), 500

            return jsonify({"message": "Application submitted successfully!"}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    return app

# Run the app
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)