from markets import db,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id=db.Column(db.Integer(),primary_key=True)
    username=db.Column(db.String(length=50),nullable=False,unique=True)
    email=db.Column(db.String(length=50),nullable=False,unique=True)
    password_hash=db.Column(db.String(length=50),nullable=False)
    budget=db.Column(db.Integer(),default=1000)
    items=db.relationship('Item',backref='owned_user',lazy=True)

class Item(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    name=db.Column(db.String(length=30),nullable=False,unique=True)
    price=db.Column(db.Integer(),nullable=False)
    barcode=db.Column(db.String(length=12),nullable=False,unique=True)
    description=db.Column(db.String(length=1000),nullable=False,unique=True)
    owner=db.Column(db.Integer(),db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Item {self.name}'