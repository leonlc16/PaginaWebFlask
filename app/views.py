from flask import Blueprint
from flask import render_template, request, flash, redirect, url_for, abort
from .forms import LoginForm, RegisterForm, TaskForm
from . models import User, Task
from flask_login import login_user, logout_user, login_required, current_user
from flask_login import LoginManager
from .consts import *


loginManager = LoginManager()
page = Blueprint('page',__name__)

@loginManager.user_loader
def loader_user(id):
    return User.get_by_id(id)

@page.app_errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404


@page.route('/')
def index():
    return render_template('index.html', title="index")



@page.route('/logout')
def logout():
    logout_user()
    flash(LOGOUT)
    return redirect(url_for('.login'))



@page.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('.tasks'))

    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.get_by_username(form.username.data)
        
        if user and user.verify_password(form.password.data) :
            login_user(user)
            flash(LOGIN)
            return redirect(url_for('.tasks'))
        else:
            flash(ERROR_USER_PASSWORD, 'error')
    return render_template('auth/login.html', title='Login', form=form)



@page.route('/registrar',  methods=['GET','POST'])
def registrar():
    if current_user.is_authenticated:
        return redirect(url_for('.tasks'))

    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate():
            user = User.create_element(form.username.data, form.password.data, form.email.data)
            flash(USER_CREATED)
            login_user(user)
            return redirect(url_for('.tasks'))
    return render_template('auth/registrar.html', title="Regstrar Usuario", form=form)




@page.route('/tasks')
@login_required
def tasks():
    task = current_user.tasks
    return render_template('tasks/list.html', title="Tareas", task=task)

@page.route('/tasks/new', methods=['GET','POST'] )
@login_required
def new_task():
    form = TaskForm(request.form)

    if request.method == 'POST':
        if form.validate():
            task =  Task.create_element(form.title.data, form.description.data, current_user.id)
            if task:
                flash(TASK_CREATED)
                return redirect(url_for('.tasks'))

    return render_template('tasks/new.html', title='Registra tarea', form=form)

@page.route('/tasks/edit/<int:task_id>', methods=['GET','POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        abort(404)
    form = TaskForm(request.form, obj=task)
    if request.method == 'POST' and form.validate():
        task = Task.update_elements(task.id, form.title.data, form.description.data)
        if task:
            flash(TASK_UPDATE)
            return redirect(url_for('.tasks')) 
    return render_template('tasks/edit.html', title='Editar tarea', form=form)


@page.route('/tasks/delete/<int:task_id>', methods=['GET','POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        abort(404)
    
    if Task.delete_element(task.id):
        flash(DELETE_TASK)

    return redirect(url_for('.tasks'))