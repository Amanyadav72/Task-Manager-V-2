from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
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
        title = request.form['title'].strip()
        if title:
            task = Task(title=title, owner=current_user)
            db.session.add(task)
            db.session.commit()
            flash('Task added successfully!', 'success')
        else:
            flash('Task title cannot be empty!', 'error')
        return redirect(url_for('tasks.dashboard'))
    return render_template('add_task.html')

@tasks_bp.route('/edit/<int:task_id>', methods=['POST'])
@login_required
def edit_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    new_title = request.form.get('title', '').strip()
    
    if new_title:
        task.title = new_title
        db.session.commit()
        flash('Task updated successfully!', 'success')
    else:
        flash('Task title cannot be empty!', 'error')
    
    return redirect(url_for('tasks.dashboard'))

@tasks_bp.route('/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('tasks.dashboard'))

@tasks_bp.route('/toggle/<int:task_id>', methods=['POST'])
@login_required
def toggle_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    task.completed = not task.completed
    db.session.commit()
    
    status = 'completed' if task.completed else 'pending'
    flash(f'Task marked as {status}!', 'success')
    
    return redirect(url_for('tasks.dashboard'))

# API endpoints for AJAX requests
@tasks_bp.route('/api/tasks', methods=['GET'])
@login_required
def api_get_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': task.id,
        'title': task.title,
        'completed': task.completed
    } for task in tasks])

@tasks_bp.route('/api/tasks/<int:task_id>/toggle', methods=['PATCH'])
@login_required
def api_toggle_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    task.completed = not task.completed
    db.session.commit()
    
    return jsonify({
        'success': True,
        'completed': task.completed,
        'message': f'Task marked as {"completed" if task.completed else "pending"}'
    })

@tasks_bp.route('/api/tasks/<int:task_id>', methods=['PUT'])
@login_required
def api_update_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    data = request.get_json()
    
    if 'title' in data and data['title'].strip():
        task.title = data['title'].strip()
        db.session.commit()
        return jsonify({'success': True, 'message': 'Task updated successfully'})
    
    return jsonify({'success': False, 'message': 'Invalid title'}), 400

@tasks_bp.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@login_required
def api_delete_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Task deleted successfully'})

@tasks_bp.route('/bulk-actions', methods=['POST'])
@login_required
def bulk_actions():
    action = request.form.get('action')
    task_ids = request.form.getlist('task_ids')
    
    if not task_ids:
        flash('No tasks selected!', 'error')
        return redirect(url_for('tasks.dashboard'))
    
    tasks = Task.query.filter(Task.id.in_(task_ids), Task.user_id == current_user.id).all()
    
    if action == 'complete_all':
        for task in tasks:
            task.completed = True
        flash(f'{len(tasks)} tasks marked as completed!', 'success')
    elif action == 'delete_all':
        for task in tasks:
            db.session.delete(task)
        flash(f'{len(tasks)} tasks deleted!', 'success')
    elif action == 'uncomplete_all':
        for task in tasks:
            task.completed = False
        flash(f'{len(tasks)} tasks marked as pending!', 'success')
    
    db.session.commit()
    return redirect(url_for('tasks.dashboard'))






"""
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
"""