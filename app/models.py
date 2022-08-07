
from app import db, login
from sqlalchemy import ForeignKey
from sqlalchemy.orm import backref,  foreign, remote
from flask_login import UserMixin # THIS IS ONLY FOR THE USER MODEL!!!!!!!!!!!!
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash


user_poke = db.Table("user_poke",
    db.Column("poke_id", db.Integer, db.ForeignKey("pokemon.poke_id")),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"))
)

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True, index=True)
    password = db.Column(db.String)
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    icon = db.Column(db.Integer)
    win = db.Column(db.Integer, default=0)
    lose = db.Column(db.Integer, default=0)
    battle = db.Column(db.Integer, default=0)
    pokemon = db.relationship(
        "Pokemon",
        secondary=user_poke,
        backref="user_poke",
        lazy="dynamic",
        )
  
    def __repr__(self):
        return f'<User: {self.email} | {self.id}>'
    
    # Human readable repr
    def __str__(self):
        return f'<User: {self.email} | {self.first_name} {self.last_name}>'

    # salts and hashes our password to make it hard to steal
    def hash_password(self, original_password):
        return generate_password_hash(original_password)

    # compares the user password to the password provided in the login form
    def check_hashed_password(self, login_password):
        return check_password_hash(self.password, login_password)

    #save user to db
    def save(self):
        db.session.add(self) # add the userr to the session
        db.session.commit() # space the stuff in the session to the database
    
    def from_dict(self, data):
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.email=data['email']
        self.password=self.hash_password(data['password'])
        self.icon=data['icon']
        #self.pokemen = data['pokemen']
    
    def get_icon_url(self):
        return f"http://avatars.dicebear.com/api/adventurer/{self.icon}.svg"

    def check_poke(self, poke_check):
         return poke_check in self.pokemon

    def catch_u_poke(self, poke_catch):
        self.pokemon.append(poke_catch)
        db.session.commit()
    
    def remove_poke(self, poke):
        self.pokemon.remove(poke)
        db.session.commit()

    def add_win(self):
        self.win += 1
        db.session.commit()

    def add_loss(self):
        self.lose += 1
        db.session.commit()
   
    def add_battle(self):
        self.battle += 1
        db.session.commit()

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    # SELECT * FROM user WHERE id = ???




class Pokemon(db.Model):
    __tablename__ = 'pokemon'
    poke_id = db.Column(db.Integer, primary_key=True)
    poke_name = db.Column(db.String, unique=True)
    ability = db.Column(db.String)
    base_experience = db.Column(db.Integer)
    photo = db.Column(db.String)
    attack_base=  db.Column(db.Integer)
    hp_base = db.Column(db.Integer)
    defense_stat = db.Column(db.Integer)

    
  
        
   
    

    
    def __repr__(self):
        return f"<Pokemon: {self.id} | {self.name}>"

    def edit(self, new_pokemon):
        self.poke_name = new_pokemon

    def save(self):
        db.session.add(self) #adds the post to the db session
        db.session.commit() #save everything in the session to the db
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

   
    def poke_known(poke_name):
        return Pokemon.query.filter_by(poke_name=poke_name).first()

        
    def from_dict(self, poke_dict):
        self.poke_id=poke_dict['poke_id']
        self.poke_name=poke_dict['name']
        self.ability = poke_dict['ability']
        self.base_experience =poke_dict['base experience']
        self.photo=poke_dict['photo']
        self.attack_base=poke_dict['attack base stat']
        self.hp_base=poke_dict['hp base stat']
        self.defense_stat=poke_dict['defense stat']
     
      
      
  