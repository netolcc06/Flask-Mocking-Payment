from flask_wtf import FlaskForm
from wtforms import Form, StringField, BooleanField, DecimalField, RadioField, DateField
from wtforms.validators import DataRequired
from wtforms.validators import ValidationError
from wtforms.validators import Email
from wtforms.validators import NumberRange
from pycpfcnpj import cpfcnpj
from decimal import ROUND_HALF_UP

def cpf_check(form, field):
    if not (cpfcnpj.validate(field.data)) or not(str.isdigit(field.data)):
        raise ValidationError('CPf not valid')

def name_check(form, field):
    a = field.data
    if not (all(x.isalpha() or x.isspace() for x in a)):
        raise ValidationError('Name not valid')

def card_name_check(form, field):
    a = field.data
    print (form.data)
    if(len(a)==0) and form.data['payment_type'] == 'Credit':
        raise ValidationError('Insert your name')
    if (not (all(x.isalpha() or x.isspace() for x in a))) and form.data['payment_type'] == 'Credit':
        raise ValidationError('Name not valid')

def card_number_check(form, field):
    a = field.data
    if (not (str.isdigit(a) and len(a)==16)) and form.data['payment_type'] == 'Credit':
        raise ValidationError('Sixteen numbers please')

def card_expiration_date_check(form, field):
    a = field.data
    if (not(len(a) == 7 and a[2] == '/')) and (form.data['payment_type'] == 'Credit'):
        raise ValidationError('Format: mm/yyyy')
    if((not str.isdigit(a[:2])) or (not str.isdigit(a[3:]))) and (form.data['payment_type'] == 'Credit'):
        print(a[:2] + "---------------" + a[3:])
        raise ValidationError('Format: mm/yyyy')

def cvv_check(form, field):
    a = field.data
    if (not(len(a) == 3 and str.isdigit(a))) and (form.data['payment_type'] == 'Credit'):
        raise ValidationError('Format: xyz (numbers)')

def amount_check(form, field):
    a = field.data
    number = float(a)

    if number < 0:
        raise ValidationError('Negative number')
    points = a.count('.')
    if points > 1:
        raise ValidationError('Invalid number')
    if (not (all(x.isdigit() or x=='.' for x in a))) and form.data['payment_type'] == 'Credit':
        raise ValidationError('Numbers only please')
    if points==1:
        point_position = a.find('.')
        if point_position == (len(a)-1 ):
            field.data = a[:len(a)-1]
        if point_position == 0:
            field.data = '0'+ a
        if point_position < (len(a)-3):
            raise ValidationError('Invalid number')
    if len(a) > 20:
        raise ValidationError('Enter a smaller number please')

class PaymentForm(FlaskForm):
    client_id = StringField("id") #does he need to know his/her client_id? lol
    name = StringField("name", validators=[DataRequired(), name_check])
    cpf = StringField("cpf", validators=[DataRequired(), cpf_check]) #can get the client_id by taking a look at the buyer.cpf~client_id
    email = StringField("email", validators=[DataRequired(), Email()])
    #payment_amount = DecimalField("amount", places = 2, rounding=ROUND_HALF_UP, validators=[DataRequired(), NumberRange(min=0)])
    payment_amount = StringField("amount", validators=[DataRequired(), amount_check])
    payment_type = RadioField('payment type', choices=[('Credit','Credit card'),('Boleto','Boleto')], validators=[DataRequired()])
    card_holder_name = StringField("card_holder_name", validators=[card_name_check])
    card_number = StringField("card_number", validators=[card_number_check])
    card_expiration_date = StringField("card_expiration_date", validators=[card_expiration_date_check])
    card_cvv = StringField("card_cvv", validators=[cvv_check])
