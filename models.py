from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_names = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    county_of_residence = db.Column(db.String(100), nullable=False)
    town = db.Column(db.String(100), nullable=False)
    email_address = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    whatsapp_number = db.Column(db.String(20), nullable=False)
    bio = db.Column(db.Text, nullable=False)

    educational_background = db.relationship('EducationalBackground', backref='application', lazy=True)
    work_experience = db.relationship('WorkExperience', backref='application', lazy=True)
    computer_literacy = db.relationship('ComputerLiteracy', backref='application', lazy=True)


class EducationalBackground(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'), nullable=False)
    level_of_academic = db.Column(db.String(50), nullable=False)
    major = db.Column(db.String(100), nullable=False)
    institution_attended = db.Column(db.String(100), nullable=False)
    duration_from = db.Column(db.Date, nullable=False)
    duration_to = db.Column(db.Date, nullable=False)


class WorkExperience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'), nullable=False)
    nature_of_work = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(100), nullable=False)
    employer_entity = db.Column(db.String(100), nullable=False)
    duration_from = db.Column(db.Date, nullable=False)
    duration_to = db.Column(db.Date, nullable=False)


class ComputerLiteracy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'), nullable=False)
    level_of_computer_literacy = db.Column(db.String(50), nullable=False)
    course_name = db.Column(db.String(100), nullable=False)
    institution_attended = db.Column(db.String(100), nullable=False)
    duration_from = db.Column(db.Date, nullable=False)
    duration_to = db.Column(db.Date, nullable=False)