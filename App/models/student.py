from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from sqlalchemy import ForeignKey
from App.models.user import User
from App.models.todo import Todo

class Student(User):
    __tablename__ = "student"
    studentid = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    todos = db.relationship('Todo', backref='student', lazy=True)

    __mapper_args__ = {
        'inherit_condition': (studentid == User.id)
    }

    def __init__(self, username, password, email):
        super().__init__(username, password)
        self.email = email

    def add_todo(self, text):
        new_todo = Todo(text=text, user_id=self.studentid)
        self.todos.append(new_todo)
        db.session.add(self)
        db.session.commit()
        return new_todo
    
    def get_json(self):
        return {
      "studentid": self.studentid,
      "username": self.username,
      "email": self.email,
      "role": 'student',
      "todos": ', '.join([todo.text for todo in self.todos])
      }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    