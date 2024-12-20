from flask import Flask, render_template, request,redirect # Flask modules are used to create the app, render templates, handle HTTP requests, and redirect users
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
Scss(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
# for deployment, add a flag for SQLAlchemy
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    """A database model representing a Todo item in the Todo List.

    Attributes:
        id (int): Unique identifier for each task.
        content (str): Description of the task.
        completed (int): Status of the task, default is 0 (not completed).
        date_created (datetime): Timestamp for when the task was created.
    """
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        """Defines how instances of the Todo class are represented as strings.

        Returns:
            str: String representation of the Todo task, showing its unique ID.
        """
        return f'<Task {self.id}'
    
with app.app_context():
    db.create_all()

@app.route('/', methods=["POST","GET"])
def index():
    """Main page for App

    Returns:
        page: home page
    """
    if request.method == "POST":
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"Error:{e}")
            return f'Error:{e}'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id):
    """delete an item from the todo list

    Args:
        id (int): uuid for each item in the todo list

    Returns:
        redirect: delete and return to home
    """
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()  
        return redirect("/")
    except Exception as e:
        return f"Error:{e}"

@app.route("/update/<int:id>", methods=["GET","POST"])
def update(id):
    """update an item from the todo list

    Args:
        id (int): uuid for each item in the todo list

    Returns:
        redirect: update and return to home
    """
    task = Todo.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR:{e}")
            return "Error"
    else:
        return render_template("update.html", task=task)

# for deploymment, replace in with ==
# if __name__ in "__main__":
if __name__ == "__main__":
    # for deploymment, define this after Todo class
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True) # 'debug=True' enables debug mode for development purposes and should be turned off in production for security and stability
