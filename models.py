from extensions import db, login_manager
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    tasks = db.relationship('Task', backref='owner', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    priority = db.Column(db.String(10), default='medium')
    due_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Fixed: datetime.utcnow instead of datetime.utcnow
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f'<Task {self.title}>'
    
    @property
    def formatted_created_at(self):
        """Returns formatted creation date"""
        if self.created_at:
            return self.created_at.strftime('%B %d, %Y at %I:%M %p')
        return 'Unknown'
    
    @property
    def formatted_due_date(self):
        """Returns formatted due date"""
        if self.due_date:
            return self.due_date.strftime('%B %d, %Y')
        return None
    
    @property
    def is_overdue(self):
        """Check if task is overdue"""
        if self.due_date and not self.completed:
            return datetime.now().date() > self.due_date
        return False