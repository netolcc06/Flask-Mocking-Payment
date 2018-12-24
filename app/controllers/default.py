from flask import render_template
from app import app, db
from pycpfcnpj import cpfcnpj
import string
import random

from app.models.forms import PaymentForm
from app.models.tables import Client, Buyer, Card, Payment

def id_generator(size=30, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

incomes = [
    {'description':'salary', 'amount':5000, 'something': 100},
    {'description':'gift', 'amount':5555}
]

@app.route('/incomes')
def get_incomes():
    return jsonify(incomes)

@app.route ('/incomes/amount/<id>', methods = ['GET'])
def get_amount(id):

    string = 'SALARY'

    if incomes[int(id)]['description'] != 'salary':
        string = 'NOT SALARY'

    out = str(incomes[int(id)]['amount']) + ' ' + string

    return jsonify(out)

#or <int:id>
@app.route ('/incomes/something/<id>', methods = ['GET'])
def get_something(id):

    string = 'SOMETHING'

    if not('something' in incomes[int(id)]):
        return 'NOT SOMETHING'

    out = str(incomes[int(id)]['something']) + ' ' + string

    return jsonify(out)

@app.route('/incomes', methods=['POST'])
def add_income():
    incomes.append(request.get_json())
    return '', 204

#unittest https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vii-unit-testing-legacy
@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
def hello_world():
    form = PaymentForm()
    if form.validate_on_submit():
        print("OK")
        if form.data["payment_type"] == "Boleto":
            string_boleto = ' '

            a = form.data["payment_amount"]
            result=''
            for c in a:
                if(c != '.'):
                    result += c

            for i in range(0,6):
                for j in range(0,5):
                    boleto = random.randint(0,9)
                    string_boleto = string_boleto + str(boleto)
                if(i <5):
                    string_boleto = string_boleto + '.'
                else:
                    string_boleto = string_boleto + '.1.48622' + result

            return render_template('boleto.html', string_boleto=string_boleto)
        else:
            client = Client(id_generator())
            buyer = Buyer(id_generator(), form.data["cpf"], form.data["name"], form.data["email"], client.id)
            card = Card(id_generator(),form.data["card_holder_name"], form.data["card_number"],
                form.data["card_expiration_date"], form.data["card_cvv"], buyer.id)
            payment = Payment(id_generator(),form.data["payment_amount"], form.data["payment_type"], card.id)

            unique_client = Client.query.filter_by(id=client.id).first()
            if unique_client == None:
                db.session.add(client)
            else:
                return "This client already exists"

            unique_email = Buyer.query.filter_by(email=buyer.email).first()
            unique_cpf = Buyer.query.filter_by(cpf=buyer.cpf).first()
            if unique_email != None:
                return "Email already found in our database. Please choose another one."
            if unique_cpf != None:
                return "CPF already found in our database. Please choose another one."

            db.session.add(buyer)

            unique_card_number = Card.query.filter_by(card_number=card.card_number).first()
            if unique_card_number == None:
                db.session.add(card)
            else:
                return "This card already exists in our database"

            db.session.add(payment)
            db.session.commit()
            return render_template('checkout.html', form=form)
    else:
        print(form.errors)

    return render_template('index.html', form=form)
