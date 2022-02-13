from flask import Blueprint, jsonify, request
from heroes.helpers import token_required
from heroes.models import db, User, Hero ,hero_schema, heroes_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('getdata')
@token_required
def getdata():
    return {'some': 'value'}


@api.route('/heroes', methods=['POST'])
@token_required
def create_hero(current_user_token):
    id = request.json['id']
    name = request.json['name']
    description = request.json['description']
    comics_appeared_in = request.json['comics_appeared_in']
    super_powers = request.json['super_powers']
    date_created = request.json['date_created']
    user_token = current_user_token.token

    hero = Hero(id, name, description, comics_appeared_in, super_powers, date_created, user_token)
    db.session.add(hero)
    db.session.commit()

    response = hero_schema.dump(hero)
    return jsonify(response)

# retrieve all heroes
@api.route('/heroes', methods=['GET'])
@token_required
def get_heroes(current_user_token):
    owner= current_user_token.token
    heroes = Hero.query.filter_by(user_token = owner).all()
    response = heroes_schema.dump(heroes)
    return jsonify(response)

# retrieve a single hero
@api.route('/heroes/<id>', methods=['GET'])
@token_required
def get_hero(current_user_token, id):
    owner= current_user_token.token
    hero = Hero.query.get(id)
    response = hero_schema.dump(hero)
    return jsonify(response)

# update hero
@api.route('/hero/<id>', methods=['POST', 'PUT'])
@token_required
def update_hero(current_user_token, id):
    hero = Hero.query.get(id)

    id = request.json['id']
    name = request.json['name']
    description = request.json['description']
    comics_appeared_in = request.json['comics_appeared_in']
    super_powers = request.json['super_powers']
    date_created = request.json['date_created']
    user_token = current_user_token.token

    db.session.commit()
    response = hero_schema.dump(hero)
    return jsonify(response)

# DELETE a hero
@api.route('/hero/<id>', methods = ['DELETE'])
@token_required
def delete_hero(current_user_token, id):
    hero = Hero.query.get(id)
    db.sessoin.delete(hero)
    db.session.commit()

    response = hero_schema.dump(hero)
    return jsonify(response)