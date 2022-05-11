from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField
from wtforms import validators
from wtforms.validators import InputRequired
 
class ContactForm(FlaskForm):
  name = StringField("Name",  validators=[InputRequired("Please enter your name.")])
  email = EmailField("Email",  validators=[InputRequired("Please enter your email address."), validators.Email("Please enter your email address.")])
  subject = StringField("Subject",  validators=[InputRequired("Please enter a subject.")])
  message = StringField("Message",  validators=[InputRequired("Please enter a message.")])
  submit = SubmitField("Send")