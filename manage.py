from flask import Flask, render_template, request, jsonify
from flask import json
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from models import db, Contact, Note

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///<databasename>'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://<user>:<passwd>@<ip>:<port>/<databasename>'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://flaskuser:M4st3r123@localhost:3306/test_flask'
db.init_app(app)
Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand) # init migrate upgrade downgrade


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/api/contacts', methods=['GET', 'POST'])
@app.route('/api/contacts/<id>', methods=['GET', 'PUT', 'DELETE'])
def contacts(id=None):
    if request.method == 'GET':
        if id is not None:
            contact = Contact.query.get(id)
            if contact:
                return jsonify(contact.serialize()), 200
            else:
                return jsonify({"msg": "Contact doesn't exist"}), 404
        else:
            contacts = Contact.query.all()
            contacts = list(map(lambda contact: contact.serialize(), contacts))
            return jsonify(contacts), 200

    if request.method == 'POST':
        name = request.json.get('name', None)
        email = request.json.get('email', None)
        phone = request.json.get('phone', "")
        address = request.json.get('address', "")

        if not name:
            return jsonify({"msg": "name is required"}), 400
        if not email:
            return jsonify({"msg": "email is required"}), 400

        contact = Contact()
        contact.name = name
        contact.email = email
        contact.phone = phone
        contact.address = address

        contact.save()

        return jsonify(contact.serialize()), 201

    if request.method == 'PUT':
        name = request.json.get('name', None)
        email = request.json.get('email', None)
        phone = request.json.get('phone', "")
        address = request.json.get('address', "")

        if not name:
            return jsonify({"msg": "name is required"}), 400
        if not email:
            return jsonify({"msg": "email is required"}), 400

        # SELECT * FROM contacts WHERE id = 1
        contact = Contact.query.get(id)

        if not contact:
            return jsonify({"msg": "Contact doesn't exist"}), 404

        contact.name = name
        contact.email = email
        contact.phone = phone
        contact.address = address

        # UPDATE contacts SET name=name, email=email ... WHERE id = 1
        contact.update()

        return jsonify(contact.serialize()), 200

    if request.method == 'DELETE':
        contact = Contact.query.get(id)
        if not contact:
            return jsonify({"msg": "Contact doesn't exist"}), 404
        
        # DELETE FROM contacts WHERE id = 1
        contact.delete()
        return jsonify({"succes", "Contact deleted"}), 200




# iniciar servidor flask
if __name__ == '__main__':
    manager.run()