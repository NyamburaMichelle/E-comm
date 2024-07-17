from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from flask_cors import CORS
import random 

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "fsbdgfnhgvjnvhmvh" + str(random.randint(1, 1000000000000))
app.config["SECRET_KEY"] = "JKSRVHJVFBSRDFV" + str(random.randint(1, 1000000000000))

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Import models after initializing db
from models import  User, Product, Order, Cart, Review, Category, Admin, Shop
migrate = Migrate(app, db)

@app.route('/')
def home():
    return "Welcome to the Flask app!"



@app.route('/signup/admin', methods=['POST'])
def signup():
    data = request.get_json()
    
    name = data.get('name')
    contacts = data.get('contacts')
    email = data.get('email')
    password = data.get('password')
    address = data.get('address')
    shop_id = data.get('shop_id')

    if not name or not contacts or not email or not password or not address or not shop_id:
        return jsonify({"error": "Missing required fields"}), 400

    existing_admin = Admin.query.filter_by(email=email).first()
    if existing_admin:
        return jsonify({"error": "Email already registered"}), 400

    hashed_password = bcrypt.generate_password_hash(password)

    new_admin = Admin(
        name=name,
        contacts=contacts,
        email=email,
        password=hashed_password,
        address=address,
        shop_id=shop_id
    )

    db.session.add(new_admin)
    db.session.commit()

    return jsonify({"message": "Admin registered successfully"}), 201


#signup user
@app.route('/signup/user', methods=['POST'])
def signup_user():
    data = request.get_json()
    
    name = data.get('name')
    contacts = data.get('contacts')
    email = data.get('email')
    password = data.get('password')
    address = data.get('address')

    if not name or not contacts or not email or not password or not address:
        return jsonify({"error": "Missing required fields"}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Email already registered"}), 400

    hashed_password = bcrypt.generate_password_hash(password)

    new_user = User(
        name=name,
        contacts=contacts,
        email=email,
        password=hashed_password,
        address=address
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

#login
@app.route('/login', methods=['GET'])
def login():
    data = request.get_json()
    
    name= data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    user = User.query.filter_by(name=name, email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity={"id": user.id, "type": "player"})
        return jsonify({"access_token": access_token}), 200

    admin = Admin.query.filter_by(name=name, email=email).first()
    if admin and bcrypt.check_password_hash(admin.password, password):
        access_token = create_access_token(identity={"id": admin.id, "type": "admin"})
        return jsonify({"access_token": access_token}), 200

    return jsonify({"error": "Invalid email or password"}), 401


   






























































if __name__ == "__main__":
    app.run(debug=True)
