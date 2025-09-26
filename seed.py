from app import db, Project
from app import app

with app.app_context():
    p1 = Project(
        title="To-Do List",
        description="This is a To-Do list",
        tech_stack="Flask, SQLite,CRUD Operation",
        github_link="https://github.com/yahiyashaikh04",
        live_link=""
    )
    db.session.add(p1)
    db.session.commit()
    print("Project added!")
