from wtforms import Form
from wtforms import validators
from wtforms import StringField, PasswordField, BooleanField, TextAreaField
from wtforms.fields.html5 import EmailField

from .models import User
class LoginForm(Form):
    username = StringField('Username', [
        validators.length(min=4, max=50, message='El username se encuentra fuera de rango')
    ])
    password = PasswordField('Password', [
        validators.DataRequired(message="La clave es requerida")
    ])

class RegisterForm(Form):
    username = StringField('Username', [
        validators.length(min=4, max=50)
    ])
    email = EmailField('Correo electronico', [
        validators.length(min=6, max=100),
        validators.DataRequired(message="El email es requerido"),
        validators.Email(message="Ingrese un email valido")
    ])
    password = PasswordField('Clave', [
        validators.DataRequired(message="La clave es requerida"),
        validators.EqualTo('confirm_password', message='La contrasenia no coincide')
    ])

    confirm_password = PasswordField('Confirmar clave')
    accept = BooleanField('', {
        validators.DataRequired()
    })


    def validate_username(self, username):
        if User.get_by_username(username.data):
            raise validators.ValidationError("Este username se encuentra en uso")
    
    def validate_email(self, email):
        if User.get_by_email(email.data):
            raise validators.ValidationError("Este correo ya se encuentra en uso")

    
class TaskForm(Form):
    title = StringField('Titulo',[
        validators.length(min=4, max=50, message='Titulo fuera de rango'),
        validators.DataRequired(message='El titulo es requerido')
    ])
    description = TextAreaField('Descripcion',[
        validators.DataRequired(message='La descripcion es requerida')
    ], render_kw={'rows':5})