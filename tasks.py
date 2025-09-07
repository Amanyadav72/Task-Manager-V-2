from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from models import Task
from extensions import db


tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/dashboard')
@login_required
def dashboard():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', tasks=tasks)

@tasks_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_task():
    if request.method == 'POST':
        task = Task(title=request.form['title'], owner=current_user)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('tasks.dashboard'))
    return render_template('add_task.html')
