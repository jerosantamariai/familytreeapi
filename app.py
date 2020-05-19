from flask import Flask, request, render_template, jsonify
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from models import db
from family import Family

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@ipserver/database'

db.init_app(app)
Migrate(app, db)
CORS(app)

manager = Manager(app)
manager.add_command("db", MigrateCommand) # init, migrate, upgrade
fam = Family('Doe')

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/family', methods=['GET', 'POST'])
@app.route('/family/<int:id>', methods=['GET','PUT', 'DELETE'])
def family(id = None):
    if request.method == 'GET':# busco los elementos de la familia
        if id is not None:
            member = fam.get_member(id)# filtro los members segun id
            if member:
                return jsonify(member), 200
            else:
                return jsonify({"msg": "Not Found"}), 404
        
        else:
            members = fam.get_all_members() # devuelve todos los members
            return jsonify(members), 200


    if request.method == 'POST':
        name = request.json.get("name", None)
        age = request.json.get("age", None)
        lucky_number = request.json.get("lucky_number", None)
        
        if not request.json.get("name", None):
            return jsonify({"name": "Agrega el nombre"}), 400  # 400 o 422
        if not request.json.get("age", None):
            return jsonify({"age": "agrega la edad asopao"}), 400  # 400 o 422
        if not request.json.get("lucky_number", None):
            return jsonify({"lucky number": "Field age is required"}), 400  # 400 o 422
        else:
            pass
        
        member = fam.add_member({
            "name": name, 
            "age": age, 
            "lucky number": lucky_number
        }) # make a new member
        return jsonify(member), 201


    if request.method == 'PUT':
        name = request.json.get("name", None)
        age = request.json.get("age", None)
        lucky_number = request.json.get("lucky_number", None)
        
        if not request.json.get("name", None):
            return jsonify({"name": "Agrega el nombre"}), 400  # 400 o 422
        if not request.json.get("age", None):
            return jsonify({"age": "agrega la edad asopao"}), 400  # 400 o 422
        if not request.json.get("lucky_number", None):
            return jsonify({"lucky number": "Field age is required"}), 400  # 400 o 422
        else:
            pass
        
        datos = fam.add_member({
            "name": name, 
            "age": age, 
            "lucky number": lucky_number
        }) # make a new member
        member=fam.update_member(id, datos)
        return jsonify(member), 200


    if request.method == 'DELETE':
        result = fam.delete_member(id)
        if result:
            return jsonify({"msg": "Member deleted"}), 200
        else:
            return jsonify({"msg": "Error deleting member"}), 400


if __name__ == '__main__':
    manager.run()