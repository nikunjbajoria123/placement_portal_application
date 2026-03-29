from flask import Flask, render_template, request, redirect
from models import db, Student, Company, PlacementDrive, Application, Admin
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config["SECRET_KEY"] = "secret123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db.init_app(app)


# CREATE DATABASE

with app.app_context():

    db.create_all()

    if not Admin.query.first():

        admin = Admin(
            username="admin",
            password=generate_password_hash("admin123")
        )

        db.session.add(admin)
        db.session.commit()


# LOGIN PAGE

@app.route("/", methods=["GET","POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        # Student login
        student = Student.query.filter_by(email=email).first()

        if student and check_password_hash(student.password,password):
            return redirect("/student/dashboard")

        # Company login
        company = Company.query.filter_by(email=email).first()

        if company and check_password_hash(company.password,password):

            if company.approval_status == "Approved":
                return redirect("/company/dashboard")

            else:
                return "Company not approved by admin yet"

    return render_template("login.html")


# STUDENT REGISTRATION

@app.route("/register/student", methods=["GET","POST"])
def register_student():

    if request.method == "POST":

        student = Student(
            name=request.form["name"],
            email=request.form["email"],
            password=generate_password_hash(request.form["password"]),
            phone=request.form["phone"],
            branch=request.form["branch"],
            cgpa=request.form["cgpa"]
        )

        db.session.add(student)
        db.session.commit()

        return redirect("/")

    return render_template("register_student.html")


# COMPANY REGISTRATION

@app.route("/register/company", methods=["GET","POST"])
def register_company():

    if request.method == "POST":

        company = Company(
            name=request.form["name"],
            email=request.form["email"],
            password=generate_password_hash(request.form["password"]),
            hr_contact=request.form["hr_contact"],
            website=request.form["website"]
        )

        db.session.add(company)
        db.session.commit()

        return redirect("/")

    return render_template("register_company.html")


# ADMIN DASHBOARD

@app.route("/admin/dashboard")
def admin_dashboard():

    students = Student.query.all()
    companies = Company.query.all()
    drives = PlacementDrive.query.all()
    applications = Application.query.all()

    return render_template(
        "admin/dashboard.html",
        students=students,
        companies=companies,
        drives=drives,
        applications=applications
    )


# APPROVE COMPANY

@app.route("/admin/approve_company/<id>")
def approve_company(id):

    company = Company.query.get(id)

    company.approval_status = "Approved"

    db.session.commit()

    return redirect("/admin/dashboard")


# COMPANY DASHBOARD

@app.route("/company/dashboard")
def company_dashboard():

    drives = PlacementDrive.query.all()

    return render_template(
        "company/dashboard.html",
        drives=drives
    )


# CREATE DRIVE

@app.route("/company/create_drive", methods=["GET","POST"])
def create_drive():

    if request.method == "POST":

        drive = PlacementDrive(
            job_title=request.form["job_title"],
            job_description=request.form["job_description"],
            eligibility=request.form["eligibility"],
            deadline=request.form["deadline"],
            status="Pending"
        )

        db.session.add(drive)
        db.session.commit()

        return redirect("/company/dashboard")

    return render_template("company/create_drive.html")


# STUDENT DASHBOARD

@app.route("/student/dashboard")
def student_dashboard():

    drives = PlacementDrive.query.filter_by(status="Approved").all()

    return render_template(
        "student/dashboard.html",
        drives=drives
    )


# APPLY FOR DRIVE

@app.route("/apply/<drive_id>/<student_id>")
def apply(drive_id,student_id):

    existing = Application.query.filter_by(
        student_id=student_id,
        drive_id=drive_id
    ).first()

    if existing:
        return "Already Applied"

    application = Application(
        student_id=student_id,
        drive_id=drive_id,
        status="Applied"
    )

    db.session.add(application)
    db.session.commit()

    return "Application Submitted"


# RUN FLASK APP

if __name__ == "__main__":
    app.run(debug=True)