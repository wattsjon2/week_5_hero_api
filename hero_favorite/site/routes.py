from flask import Blueprint, render_template, request, jsonify
from flask_login.utils import login_required
from ..api.routes import get_heroes_from_all_users
from hero_favorite.models import db, Hero
from hero_favorite.forms import UserHeroAddForm
from flask_login import login_user, logout_user, current_user, login_required

"""
    Note that in the below code, some arguments are specified when createing blueprint objects
    The first argument, 'site' is the Blueprint's name, which flask uses for routing
    The second arugment, __name__, is the blueprint's import name which flask uses to locate the Blueprint's resources
"""

site = Blueprint('site',__name__,template_folder = 'site_templates')

@site.route('/', methods = ['GET'])
def home():
    heroes = Hero.query
    return render_template('index.html', heroes = heroes)

@site.route('/profile', methods = ['GET','POST'])
@login_required
def profile():
    form = UserHeroAddForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            fav_hero = form.hero.data
            reason = form.reason.data
            user_token = current_user.token
            hero = Hero(fav_hero, reason, user_token)
            db.session.add(hero)
            db.session.commit()
            return render_template('profile.html', form = form)
    except:
         raise Exception('Invalid Form Data: Please Check your form.')

    return render_template('profile.html', form = form)

    
 