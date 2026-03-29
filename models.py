from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Admin(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(200))


class Student(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(200))

    phone = db.Column(db.String(20))
    branch = db.Column(db.String(50))
    cgpa = db.Column(db.Float)


class Company(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(200))

    hr_contact = db.Column(db.String(100))
    website = db.Column(db.String(200))

    approval_status = db.Column(db.String(20), default="Pending")


class PlacementDrive(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    job_title = db.Column(db.String(100))
    job_description = db.Column(db.Text)

    eligibility = db.Column(db.String(200))
    deadline = db.Column(db.String(50))

    status = db.Column(db.String(20), default="Pending")


class Application(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer)
    drive_id = db.Column(db.Integer)

    status = db.Column(db.String(20), default="Applied")