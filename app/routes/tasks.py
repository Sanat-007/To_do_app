from flask import Blueprint,request,redirect,render_template,flash,session,url_for
from app import db
from app.models import Task

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/')
def view_tasks():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks)

@tasks_bp.route("/add",methods=["POST","GET"])
def add_tasks():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    title = request.form.get('title')
    if title and title.strip():
        new_task = Task(title=title.strip(), status = 'Pending')
        db.session.add(new_task)
        db.session.commit()
        flash('Task added succesfully','success')
        return redirect(url_for('tasks.view_tasks'))
    else:
        flash('Tittle cannot be empty','danger')
    
    title = Task.query.all()
    return render_template('tasks.html',tasks=title)

@tasks_bp.route('/toggle/<int:task_id>', methods=["POST"])
def toggle_status(task_id):
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    task = Task.query.get_or_404(task_id)
    
    # CORRECT LOGIC: Cycle through statuses
    if task.status == 'Pending':
        task.status = 'Working'
    elif task.status == 'Working':
        task.status = 'Done'
    else:  # 'Done' -> 'Pending'
        task.status = 'Pending'
    
    db.session.commit()
    flash(f'Task "{task.title}" status updated to {task.status}', 'success')
    
    return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route('/clear', methods=["POST"])
def clear_tasks():
    Task.query.delete()
    db.session.commit()
    flash('All tasks cleared!','info')
    return redirect(url_for('tasks.view_tasks'))

        