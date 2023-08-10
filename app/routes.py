from app import app
from flask import jsonify
from flask import render_template, request, flash, redirect, url_for
from app.models import *
from app.forms import *
from flask_login import current_user, login_user, login_required, logout_user
from sqlalchemy import func
import json
from flask import render_template, request, flash, redirect, url_for, jsonify


@app.route("/")
def index():
    products = PRODUCT.query.all()
    return render_template("index.html", products=products)


# ------------ addTypeProduct --------------
@app.route('/addProductType_s1')
@login_required
def addProductType_s1():
    if current_user.is_admin == 1:
        return render_template("addProductType_s1.html")
    else:
        flash('Bạn không có quyền truy cập!')
        return render_template("index.html")


@app.route("/addProductType_s2", methods=["POST"])
def addProductType_s2():
    """thêm loại sản phẩm"""
    type_name = request.form.get("type_name")
    type = TYPE(type_name=type_name)
    db.session.add(type)
    db.session.commit()
    message = "Thêm loại sản phảm thành công!"
    return render_template("succes.html", message=message)


# ------------ addNewProduct --------------
@app.route("/addNewProduct_s1")
@login_required
def addNewProduct_s1():
    """chọn loại sản phảm"""
    if current_user.is_admin == 1:
        type_product = TYPE.query.all()
        return render_template("addNewProduct_s1.html", type_product=type_product)
    else:
        flash('Bạn không có quyền truy cập!')
        return render_template("index.html")


@app.route('/addNewProduct_s2', methods=["POST"])
def addNewProduct_s2():
    """Thêm sản phảm """

    product_name = request.form.get("product_name")
    img = request.form.get("img")
    price = request.form.get("price")
    information = request.form.get("information")
    type_id = request.form.get("type_id")
    product = PRODUCT(product_name=product_name, img=img, price=price, information=information, type_id=type_id)
    db.session.add(product)
    db.session.commit()
    message = "Thêm sản phẩm thành công!"
    return render_template("succes.html", message=message)


# ------------ signUpForm --------------
@app.route("/signUp_form", methods=["GET", "POST"])
def signUp_form():
    """form đăng kí"""
    form = signUpForm()
    if form.validate_on_submit():
        user_name = form.user_name.data
        full_name = form.full_name.data
        password = form.password.data
        email = form.email.data
        gender = form.gender.data
        phone = form.phone.data
        address = form.address.data
        NewUser = USER(user_name=user_name, full_name=full_name, password=password, email=email, address=address, gender=gender, phone=phone)
        NewUser.set_password(form.password.data)
        db.session.add(NewUser)
        db.session.commit()
        flash('Đăng kí thành công!')
        return redirect(url_for('index'))
    return render_template("signUp_form.html", form=form)


# ---------- Login ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Đăng nhập"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = loginForm()
    if form.validate_on_submit():
        user = USER.query.filter_by(user_name=form.user_name.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Tên đăng nhập hoặc mật khẩu không đúng!')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


# ---------- logout ----------------
@app.route('/logout')
def logout():
    """Đăng xuất"""
    logout_user()
    return redirect(url_for('index'))


# ------------ setAdmin --------------
@app.route('/setAdmin')
@login_required
def setAdmin():
    """Xét admin"""
    if current_user.is_admin == 1:
        users = USER.query.all()
        return render_template('setAdmin.html', users=users)
    else:
        flash('Bạn không có quyền truy cập!')
        return render_template("index.html")


@app.route('/setAdmin_s2/<int:id>')
def setAdmin_s2(id):
    user = USER.query.get(id)
    return render_template('setAdmin_s2.html', user=user)


@app.route('/setAdmin_s3', methods=['GET', 'POST'])
def setAdmin_s3():
    id = request.form.get('id')
    is_admin = request.form.get('is_admin')
    user = USER.query.get(id)
    user.is_admin = is_admin
    db.session.commit()
    message = "Xét Admin thành công!"
    return render_template('succes.html', message=message)


# ------------ updateProduct --------------
@app.route('/updateProduct_s1')
def updateProduct_s1():
    """Chọn loại sản phẩm"""
    if current_user.is_admin == 1:
        types = TYPE.query.all()
        return render_template('updateProduct_s1.html', types=types)
    else:
        flash('Bạn không có quyền truy cập!')
        return render_template('index.html')


@app.route('/updateProduct_s2/<int:type_id>')
def updateProduct_s2(type_id):
    """chọn sản phẩm"""
    products = PRODUCT.query.filter_by(type_id=type_id).all()
    return render_template('updateProduct_s2.html', products=products)


@app.route('/updateProduct_s3/<int:product_id>')
def updateProduct_s3(product_id):
    """form sản phẩm"""
    product = PRODUCT.query.filter_by(product_id=product_id).first()
    return render_template('updateProduct_s3.html', product=product)


@app.route('/updateProduct_s4', methods=['POST'])
def updateProduct_s4():
    product_id = request.form.get('product_id')
    product_name = request.form.get('product_name')
    img = request.form.get('img')
    price = request.form.get('price')
    information = request.form.get('information')
    type_id = request.form.get('type_id')
    product = PRODUCT.query.get(product_id)
    product.product_name = product_name
    product.img = img
    product.price = price
    product.information = information
    product.type_id = type_id
    db.session.commit()
    message = "Update sản phẩm thành công!"
    return render_template('succes.html', message=message)


# ------------deleteProduct --------------
@app.route('/deleteProduct_s1')
def deleteProduct_s1():
    """Chọn loại sản phẩm"""
    if current_user.is_admin == 1:
        types = TYPE.query.all()
        return render_template('deleteProduct_s1.html', types=types)
    else:
        flash('Bạn không có quyền truy cập!')
        return render_template('index.html')


@app.route('/deleteProduct_s2/<int:type_id>')
def deleteProduct_s2(type_id):
    """chọn sản phẩm"""
    products = PRODUCT.query.filter_by(type_id=type_id).all()
    return render_template('deleteProduct_s2.html', products=products)


@app.route('/deleteProduct_s3', methods=['POST'])
def deleteProduct_s3():
    """Xóa sản phẩm"""
    checkbox = request.form.getlist('checkbox')
    for id in checkbox:
        product = PRODUCT.query.get(id)
        db.session.delete(product)
        db.session.commit()
    message = "Xóa sản phẩm thành công!"
    return render_template('succes.html', message=message)


# ------------buyProduct --------------
@app.route('/buyProduct_s1', methods=['POST'])
@login_required
def buyProduct_s1():
    user_id = current_user.id
    product_id = request.form.get('product_id')
    price = request.form.get('price')
    quantity = request.form.get('quantity')
    total = int(price) * int(quantity)
    bill = BILL(user_id=user_id, product_id=product_id, quantity=quantity, total=total)
    db.session.add(bill)
    db.session.commit()
    flash('Mua hàng thành công!')
    return redirect(url_for('index'))


# ------------viewBill --------------S
@app.route('/viewBill_s1')
def viewBill_s1():
    user_id = current_user.id
    bills = BILL.query.filter_by(user_id=user_id).all()
    return render_template('viewBill_s1.html', bills=bills)


@app.route('/viewBill_s2', methods=['POST'])
def viewBill_s2():
    product_id = request.form.get('product_id')
    product = PRODUCT.query.filter_by(product_id=product_id).first()
    id = request.form.get('id')
    bill = BILL.query.filter_by(id=id).first()
    return render_template('viewBill_s2.html', bill=bill, product=product)


# ------------information --------------
@app.route('/information')
def information():
    id = current_user.id
    user = USER.query.get(id)
    return render_template('information.html', user=user)


@app.route('/updateInformation', methods=['POST'])
def updateInformation():
    id = request.form.get('id')
    user_name = request.form.get('user_name')
    full_name = request.form.get('full_name')
    phone = request.form.get('phone')
    gender = request.form.get('gender')
    address = request.form.get('address')
    email = request.form.get('email')
    user = USER.query.get(id)
    user.user_name = user_name
    user.full_name = full_name
    user.email = email
    user.gender = gender
    user.address = address
    user.phone = phone
    db.session.commit()
    message = "Cập nhật thành công!"
    return render_template('succes.html', message=message)


# ------------------veiwDetail-----------------
@app.route('/veiwDetail/<int:product_id>')
def veiwDetail(product_id):
    product = PRODUCT.query.get(product_id)
    return render_template("veiwDetail.html", product=product)


# ------------------------search------------------
@app.route('/search', methods=['POST'])
def search():
    search = request.form.get('search')
    products = PRODUCT.query.filter(PRODUCT.product_name.like(f"%{search}%")).all()
    return render_template('search.html', products=products)


# -------------------addSHOP-----------------
@app.route("/insertSHOP_s1", methods=["GET"])
def insertSHOP_s1():
    """choose place to add ATM"""
    form = addSHOPForm()
    return render_template("insertSHOP_s1.html", form=form)


@app.route("/insertSHOP_result", methods=["POST"])
def insertSHOP_result():
    """add new SHOP"""
    # Get form information.
    name = request.form.get("name")
    img = request.form.get("img")
    level = request.form.get("level")
    address = request.form.get("address")
    geomInput = 'Point(' + request.form.get("lng") + " " + request.form.get("lat") + ")"
    newSHOP = SHOPPOINT(name=name, address=address, img=img, level=level, geom=func.ST_GeomFromText(geomInput, 4326))
    db.session.add(newSHOP)
    db.session.commit()
    message = "Thêm địa điểm thành công!"
    return render_template("succes.html", message=message)


# --------------------apiSHOP------------------
@app.route("/api/v1/SHOPPOINTs")
def SHOPPOINTs_get_API():
    """Return feature in point table"""
    shops = db.session.query(SHOPPOINT.id, SHOPPOINT.name, SHOPPOINT.address, SHOPPOINT.level, SHOPPOINT.img, \
    func.ST_AsGeoJSON(SHOPPOINT.geom).label('geometry')).all()
    # Get all daily flights.
    shopFeatures = []  # store all shop
    for shop in shops:  # generate geojson for each shop
        shop_temp = {}
        shop_temp["type"] = "Feature"
        shop_temp["properties"] = {
            "id": shop.id,
            "name": shop.name,
            "level": shop.level,
            "img": shop.img,
            "address": shop.address,
        }
        shop_temp["geometry"] = json.loads(shop.geometry)
        shopFeatures.append(shop_temp)  # add shop geojson to list

    return jsonify({  # convert to geojson format
            "features": shopFeatures
        })


# --------------------veiwSHOP------------------------
@app.route("/SHOPPOINTs", methods=["GET"])
def SHOPPOINTs():
    return render_template("SHOPPOINTs.html")


# ---------------------updateAndeleteSHOP------------------
@app.route("/updateAndDeleteSHOP")
def updateAndDeleteSHOP():
    return render_template("updateAndDeleteSHOP.html")


@app.route("/deleteSHOP", methods=['POST'])
def deleteSHOP():
    id = request.form.get('id')
    shop = SHOPPOINT.query.get(id)
    db.session.delete(shop)
    db.session.commit()
    message = "Xóa thành công!"
    return render_template("succes.html", message=message)


@app.route("/api/v1/SHOP/<int:id>")
def updateSHOP_s1(id):
    shop = db.session.query(SHOPPOINT.id, SHOPPOINT.name, SHOPPOINT.address, SHOPPOINT.level, SHOPPOINT.img, \
    func.ST_AsGeoJSON(SHOPPOINT.geom).label('geometry')).filter_by(id=id).first()
    shopFeatures = []
    shop_temp = {}
    shop_temp["type"] = "Feature"
    shop_temp["properties"] = {
        "id": shop.id,
        "name": shop.name,
        "level": shop.level,
        "img": shop.img,
        "address": shop.address,
    }
    shop_temp["geometry"] = json.loads(shop.geometry)
    shopFeatures.append(shop_temp)  # add shop geojson to list

    return jsonify({  # convert to geojson format
            "features": shopFeatures
        })


@app.route("/updateSHOP_s2", methods=['POST'])
def updateSHOP_s2():
    id = request.form.get('id')
    return render_template("updateSHOP_s1.html", id=id)


@app.route("/updateSHOP_s3", methods=['POST'])
def updateSHOP_s3():
    id = request.form.get('id')
    address = request.form.get('address')
    name = request.form.get('name')
    level = request.form.get('level')
    img = request.form.get('img')
    lat = request.form.get('lat')
    lng = request.form.get('lng')
    geomInput = 'Point(' + request.form.get("lng") + " " + request.form.get("lat") + ")"
    shop = SHOPPOINT.query.get(id)
    shop.address = address
    shop.name = name
    shop.level = level
    shop.img = img
    shop.geom = func.ST_GeomFromText(geomInput, 4326)
    db.session.commit()
    message = "Cập nhật thành công!"
    return render_template("succes.html", message=message)
