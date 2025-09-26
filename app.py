from flask import Flask,render_template,redirect,flash,request,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage

load_dotenv()

FLASK_SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
SMTP_HOST = os.environ.get("SMTP_HOST")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASS = os.environ.get("SMTP_PASS")
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL")

app= Flask(__name__)
app.secret_key= FLASK_SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///portfilo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False

db=SQLAlchemy(app)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    tech_stack = db.Column(db.String(200), nullable=False)
    github_link = db.Column(db.String(200))
    live_link = db.Column(db.String(200))

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def send_email(to_email, subject, body):
    msg = EmailMessage()
    msg["From"] = SMTP_USER
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        print(" Email sent")
    except Exception as e:
        print("Error:", e)

@app.route('/')
def home():
    projects = Project.query.all()
    return render_template("index.html", projects=projects)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        msg = request.form['message']
        new_msg = Message(name=name, email=email, message=msg)
        db.session.add(new_msg)
        db.session.commit()
        body = f"""
     New message received:

    Name: {name}
    Email: {email}
    Message: {msg}
    """
        send_email(ADMIN_EMAIL, "New Contact Form Message", body)

        flash("Message sent successfully!")
        return redirect(url_for("contact"))

    return render_template("contact.html")

@app.route('/project')
def project():
    projects = Project.query.all()
    return render_template("project.html", projects=projects)


@app.route('/about')
def about():

    return render_template('about.html')

@app.route('/skill')
def skill():

    return render_template('skill.html')

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)