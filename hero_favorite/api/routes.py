from flask import Blueprint,request,jsonify
from hero_favorite.helpers import token_required
from hero_favorite.models import db, User, Hero, hero_schema, heroes_schema


api = Blueprint('api',__name__, url_prefix ='/api')

@api.route('/getdata')
@token_required
def getdata(current_user_token):
    return { 'some':'value'}

# CREATE Hero ROUTE
@api.route('/heroes', methods = ['POST'])
@token_required
def create_hero(current_user_token):
    fav_hero = request.json['fav_hero']
    reason = request.json['reason']
    user_token = current_user_token.token

    hero = Hero(fav_hero, reason, user_token)
    db.session.add(hero)
    db.session.commit()
    response = hero_schema.dump(hero)
    return jsonify(response)

# retrive all heroes endpoint
@api.route('/heroes', methods = ['GET'])
@token_required
def get_heroes(current_user_token):
    owner = current_user_token.token
    heroes = Hero.query.filter_by(user_token = owner).all()
    response = heroes_schema.dump(heroes)
    return jsonify(response)

# retrieve single hero endpoint
@api.route('/heroes/<id>', methods = ['GET'])
@token_required
def get_hero(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        hero = Hero.query.get(id)
        response = hero_schema.dump(hero)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid Token Required'}),401

# update hero endpoint
@api.route('/heroes/<id>', methods = ['POST','PUT'])
@token_required
def update_hero(current_user_token, id):
    hero = Hero.query.get(id) #Get the drone instance

    hero.fav_hero = request.json['fav_hero']
    hero.reason = request.json['reason']
    hero.user_token = current_user_token.token

    db.session.commit()
    response = hero_schema.dump(hero)
    return jsonify(response)

# delete hero Endpoint
@api.route('heroes/<id>', methods = ['DELETE'])
@token_required
def delete_hero(current_user_token, id):
    hero = Hero.query.get(id)
    db.session.delete(hero)
    db.session.commit()

    response = hero_schema.dump(hero)
    return jsonify(response)


# retrive all heroes endpoint
@api.route('/heroes/all', methods = ['GET'])
@token_required
def get_heroes_from_all_users(current_user_token):
    heroes = Hero.query.all()
    response = heroes_schema.dump(heroes)
    return jsonify(response)