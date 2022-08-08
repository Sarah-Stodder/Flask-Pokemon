from flask import redirect, render_template, request, url_for, flash, make_response, g, abort
import requests
from .forms import  Find_pokemon
from app.models import  Pokemon,  User
from flask_login import login_required, current_user
from . import bp as main
from random import randint

@main.route('/', methods=['GET'])
def home():
    return render_template('home.html.j2')


@main.route('/pokemon', methods=['GET', 'POST'])
@login_required
def pokemon():
    form = Find_pokemon()
    if request.method =='POST':
        pokemon_name = form.pokemon_name.data.lower()
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}/'
        response = requests.get(url)
        if not response.ok:
                error_string = "That pokemon isnt in our database yet! Try again, or check your spelling!"
                return render_template('catch.html.j2', error=error_string,form=form)
        data = response.json()
        for pokemon in data:
            poke_dict={}
            poke_dict={
                "poke_id": data['id'],
                "name": data['name'].title(),
                "ability":data['abilities'][0]["ability"]["name"],
                "base experience":data['base_experience'],
                "photo":data['sprites']['other']['home']["front_default"],
                "attack base stat": data['stats'][1]['base_stat'],
                "hp base stat":data['stats'][0]['base_stat'],
                "defense stat":data['stats'][2]["base_stat"],
                
            }
            if not Pokemon.poke_known(poke_dict["name"]):
                pokemon=Pokemon()
                pokemon.from_dict(poke_dict) 
                pokemon.save()
            
            return render_template('catch.html.j2', pokemon=poke_dict, form=form)
    
    return render_template('catch.html.j2', form=form)
    
@main.route('/catch/<int:id>')
@login_required
def catch_poke(id):
    pokemon = Pokemon.query.filter_by(poke_id=id).first()
    if pokemon in current_user.pokemon:
        flash(f'You already have that pokemon on your team!', 'danger')
        return redirect(url_for('main.pokemon'))
    elif current_user.pokemon.count() == 5:
        flash('Your Pokemon Team is full. Please remove Pokemon before adding.', 'danger')
        return redirect(url_for('main.pokemon'))
    else:
        flash(f'Added to your Pokemon team', 'success')
        current_user.catch_u_poke(pokemon)
    return redirect(url_for('main.pokemon'))



@main.route('/my_team')
@login_required
def my_team():
    return render_template('my_team.html.j2',  team=current_user.pokemon.all(), user=current_user)




@main.route('/pokemon/<string:name>')
@login_required
def release(name):
    poke_to_remove = Pokemon.query.filter_by(poke_name=name).first()
    current_user.remove_poke(poke_to_remove)
    flash(f"Released!", 'warning')
    return redirect(url_for('main.my_team'))

@main.route("/show_users")
@login_required
def show_users():
    users = User.query.filter(User.id != current_user.id, User.pokemon).all()
    return render_template("show_users.html.j2", users=users )


@main.route('/view_user_team/<int:id>')
@login_required
def view_user_team(id):
    user = User.query.get(id)
    if user.pokemon:
        return render_template("my_team.html.j2", team=user.pokemon, user=user)
    flash("This user has not caught any Pokmon yet!")
    return redirect(url_for("main.show_users"))


@main.route('/battle/<int:id>')
@login_required
def battle(id):  
    ran = randint(100,600)
    user =User.query.get(id) 
    op_team = user.pokemon
    cur_team = current_user.pokemon
    op_total = 0
    cur_total = 0
    for op in op_team:
        op_total += op.hp_base
        op_total += op.attack_base
        op_total += op.defense_stat
        op_team += ran
    for cur in cur_team:
        cur_total += cur.hp_base
        cur_total += cur.attack_base
        cur_total += cur.defense_stat
        cur_total += ran
    if op_total < cur_total:
       winner = current_user
       print(op_total)
       print(cur_total)
       current_user.add_win()
       user.add_loss()
       current_user.add_battle()
       user.add_battle()
    elif op_total > cur_total:
       winner = user
       current_user.add_loss()
       user.add_win()
       current_user.add_battle()
       user.add_battle()
    return render_template("battle.html.j2", op_team=user.pokemon, user=user, cur_team=current_user.pokemon, winner=winner)