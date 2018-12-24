from app import db

class Client(db.Model):
    __tablename__= "clients"

    id = db.Column(db.String, primary_key=True)

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return '<User with id = %r>' % self.id


class Buyer(db.Model):
    __tablename__= "buyers"

    id = db.Column(db.String, primary_key=True)

    #name, email, cpf
    cpf = db.Column(db.String(11), nullable=False, unique=True,primary_key = True)#number without dots
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique = True, nullable=False)

    client_id = db.Column(db.String, db.ForeignKey('clients.id'))
    client = db.relationship('Client', foreign_keys = client_id)


    def __init__(self, id, cpf, name, email, client_id):
        self.id = id
        self.cpf = cpf
        self.name = name
        self.email = email
        self.client_id = client_id

    #def __repr__(self):
    #    return '<User with id = %r>' % self.id

class Card(db.Model):
    __tablename__= "cards"

    id = db.Column(db.String, primary_key=True)

    buyer_id = db.Column(db.String, db.ForeignKey('buyers.id')) #can I do that? or clients.id?
    buyer = db.relationship('Buyer', foreign_keys = buyer_id)

    holder_name = db.Column(db.String(80), nullable=False)
    card_number = db.Column(db.String(16), unique = True, nullable=False) #can 2 different people use the same card?
    expiration_date = db.Column(db.String(7), nullable=False) #specify format MM/YYYY
    cvv = db.Column(db.String(3), nullable=False) #specify format xyz

    def __init__(self, id, holder_name, card_number, expiration_date, cvv, buyer_id):
        self.id = id
        self.holder_name = holder_name
        self.card_number = card_number
        self.expiration_date = expiration_date
        self.cvv = cvv
        self.buyer_id = buyer_id

    #def __repr__(self):
    #    return '<User with id = %r>' % self.id

class Payment(db.Model):
    __tablename__= "payments"

    #amount, type, card, buyer
    amount = db.Column(db.String(20), nullable=False)
    id = db.Column(db.String, primary_key=True)
    type = db.Column(db.String(5), nullable=False) #True if Card

    card_id = db.Column(db.String, db.ForeignKey('cards.id')) #create a null card
    card = db.relationship('Card', foreign_keys = card_id)


    def __init__(self, id, amount, type, card_id):
        self.id = id
        self.amount = amount
        self.type = type
        self.card_id = card_id


    #def __repr__(self):
    #    return '<User with id = %r>' % self.id
