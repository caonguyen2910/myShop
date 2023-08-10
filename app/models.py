
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from geoalchemy2 import Geometry


class USER(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, nullable=False, unique=True)
    full_name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    gender = db.Column(db.String, nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Integer, default=0)

    def set_password(self, password_input):
        self.password = generate_password_hash(password_input)

    def check_password(self, password_input):
        return check_password_hash(self.password, password_input)


@login.user_loader
def load_user(id):
    return USER.query.get(int(id))


class PRODUCT(db.Model):
    __tablename__ = "product"
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String, nullable=False)
    img = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    information = db.Column(db.String, nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey("type.id"), nullable=False)


class TYPE(db.Model):
    __tablename__ = "type"
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String, nullable=False)


class BILL(db.Model):
    __tablename__ = "bill"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.product_id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)


class SHOPPOINT(db.Model):
    __tablename__ = "shoppoint"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    level = db.Column(db.Integer, nullable=False)
    img = db.Column(db.String, nullable=False)
    geom = db.Column(Geometry('POINT'))


class SHOP_building(db.Model):
    __tablename__ = "SHOP_building"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    number_floor = db.Column(db.Integer, nullable=False, default=1)
    area = db.Column(db.Float, nullable=False, default=1)
    geom = db.Column(Geometry('POLYGON'))
