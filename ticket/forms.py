from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextField, RadioField, TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length


### change the following tuples accordingly to your application ticket needs
ticket_app = ([
    ( '1', 'Server' ),
    ( '2', 'Local' )
    ])

ticket_arg = ([
    ( '1', 'Development (code)' ),
    ( '2', 'Deploy (code)' ),
    ( '3', 'Bugs (code)' ),
    ( '4', 'Bugs (front-end)' ),
    ( '5', 'Improvement Suggestion' ),
    ( '6', 'Other' )
    ])

urgency_choices = ([
    ( '1', 'Low' ),
    ( '2', 'Medium' ),
    ( '3', 'High' )
    ])


### these are the Forms actually imported
class TicketForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=250)])
    body = TextAreaField('Body', validators=[DataRequired(), Length(min=1, max=4000)])
    urgency = RadioField('Urgency', choices=urgency_choices, validators=[DataRequired()] )
    application = RadioField('Application', choices=ticket_app, validators=[DataRequired()])
    argument = SelectField('Argument', choices=ticket_arg, validators=[DataRequired()])
    submit = SubmitField('Submit')

class TicketReplyForm(FlaskForm):
    body = TextAreaField('Update')
    follow = BooleanField('Follow Ticket Updates (e-mail)')
    submit = SubmitField('Update')
