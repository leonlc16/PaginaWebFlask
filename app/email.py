from flask_mail import Message
from flask import current_app, render_template
from flask_mail import Mail

mail = Mail()
def welcome_mail(user):
    message = Message('Bienvenido a el proyecto de Flask n.n',
        sender=current_app.config['MAIL_USERNAME'], recipients=[user.email])
    message.html = render_template('email/welcome.html', user=user)
    mail.send(message)

