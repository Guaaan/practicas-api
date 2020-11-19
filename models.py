from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from sqlalchemy.sql.schema import ForeignKey
db = SQLAlchemy()

class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(150), nullable=True, default="")
    address = db.Column(db.String(150), nullable=True, default="sin direccion")
    notes = db.relationship('Note', backref='contact', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address
        }

    def serialize_with_notes(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "notes": self.getNotes()
        } 
    
    def getNotes(self):
        return list(map(lambda note: note.serialize(), self.notes))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    contact_id = db.Column(db.Integer, ForeignKey('contacts.id'))
    #contact = db.relationship('Contact')

    def serialize(self):
        return {
            "id": self.id,
            "text": self.text,
            #"contact_id": self.contact_id,
            "contact": {
                "name": self.contact.name,
                "email": self.contact.email,
                "phone": self.contact.phone
            }
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()