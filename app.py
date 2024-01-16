from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure secret key

db = SQLAlchemy(app)

class Office(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    office_no = db.Column(db.Integer)
    title = db.Column(db.String(50))
    address = db.Column(db.String(255))
    city = db.Column(db.String(50))
    town = db.Column(db.String(50))
    telephone = db.Column(db.String(50))
    worktime = db.Column(db.String(50))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    email = db.Column(db.String(100))
    password = db.Column(db.String(50))
    country = db.Column(db.String(50))
    city = db.Column(db.String(50))


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    car_no = db.Column(db.Integer)
    name = db.Column(db.String(100))
    office_no = db.Column(db.Integer)
    location = db.Column(db.String(100))
    date = db.Column(db.String(50))
    time = db.Column(db.String(50))
    type = db.Column(db.String(50))
    transmission = db.Column(db.String(50))
    deposit = db.Column(db.Integer)
    mileage= db.Column(db.Integer)
    age = db.Column(db.Integer)
    cost = db.Column(db.Integer)
    discounted_cost = db.Column(db.Integer)
    image = db.Column(db.String(50))


with app.app_context():
    db.create_all()

users_data = [
    {"name": "İhsan Efe","surname": "Uzun","email": "ihsanefe@gmail.com","password": "İzmir","country": "Konak","city": ""},
    
]


offices_data = [
    {"office_no": 1,"title": "İZMİR ALSANCAK TOWN","address": "İsmet Kaptan Mh, Gaziosmanpaşa Bulvarı N:7 Hilton İzmir 2.blok Z03 , 35210","city": "İzmir","town": "Konak","telephone": "0232 441 44 17 - 0232 441 44 18","worktime": "Monday - Sunday 09:00 - 19:00"},
    {"office_no": 2,"title": "IZMIR BORNOVA TOWN","address": "Ankara Asfaltı No:30 Birmot İzmir temsilciliği , 35530","city": "İzmir","town": "Bayraklı","telephone": "0232 241 22 73","worktime": "Monday - Saturday 08:30 - 18:00"},
    {"office_no": 3,"title": "MANISA","address": "Laleli Mahallesi, Ali Rıza Efendi Caddesi, No:2/A","city": "Manisa","town": "Yunusemre","telephone": "0236 228 22 79","worktime": "Monday - Sunday 09:00 - 19:00"},
    {"office_no": 4,"title": "AYDIN TOWN","address": "Güzelhisar Mah. Adnan Menderes Bulvarı Vali Yazıcıoğlu Kültür Merkezi Karşısı No:91/A","city": "Aydın","town": "Merkez","telephone": "0256 221 18 57","worktime": "Monday - Saturday 10:00 - 18:00"},

]

# Sample data for cars
cars_data = [
    {"car_no": 1, "name": "Renault Clio", "office_no": 1, "location": "İZMİR ALSANCAK TOWN", "date": "2024-01-01", "time": "12:00", "type": "ECONOMIC", "transmission": "Manual", "deposit": 2500, "mileage": 1000, "age": 21, "cost": 957, "discounted_cost": 800, "image":"https://www.avis.com.tr/Avis/media/Avis/Cars/b-renault-clio.png"},
    {"car_no": 2, "name": "Fiat Egea", "office_no": 1, "location": "İZMİR ALSANCAK TOWN", "date": "2024-02-01", "time": "02:00", "type": "ECONOMIC", "transmission": "Manual", "deposit": 2500, "mileage": 1000, "age": 25, "cost": 1035, "discounted_cost": 879, "image":"https://www.avis.com.tr/Avis/media/Avis/Cars/n-fiat-egea.png"},
    {"car_no": 3, "name": "Renault Clio AT", "office_no": 1, "location": "İZMİR ALSANCAK TOWN", "date": "2024-01-01", "time": "04:00", "type": "ECONOMIC", "transmission": "Automatic", "deposit": 2500, "mileage": 1000, "age": 21, "cost": 1089, "discounted_cost": 926, "image":"https://www.avis.com.tr/Avis/media/Avis/Cars/f-renault-clio-at.png"},
    {"car_no": 4, "name": "Ford Focus", "office_no": 1, "location": "İZMİR ALSANCAK TOWN", "date": "2024-01-01", "time": "04:00", "type": "COMFORT", "transmission": "Automatic", "deposit": 3000, "mileage": 1000, "age": 23, "cost": 1464, "discounted_cost": 1244, "image":"https://www.avis.com.tr/Avis/media/Avis/Cars/o-ford-focus.png"},
    {"car_no": 5, "name": "Peugeot 2008", "office_no": 1, "location": "İZMİR ALSANCAK TOWN", "date": "2024-03-01", "time": "04:00", "type": "COMFORT", "transmission": "Automatic", "deposit": 3000, "mileage": 1000, "age": 23, "cost": 1524, "discounted_cost": 1295, "image":"https://www.avis.com.tr/Avis/media/Avis/Cars/o-ford-focus.png"},
    {"car_no": 6, "name": "Audi A3", "office_no": 1, "location": "İZMİR ALSANCAK TOWN", "date": "2024-01-01", "time": "04:00", "type": "PRESTIGE", "transmission": "Automatic", "deposit": 3500, "mileage": 1000, "age": 25, "cost": 2171, "discounted_cost": 1844, "image":"https://www.avis.com.tr/Avis/media/Avis/Cars/h-audi-a3.png"},
    {"car_no": 7, "name": "Volvo XC40", "office_no": 1, "location": "İZMİR ALSANCAK TOWN", "date": "2024-01-01", "time": "04:00", "type": "PREMIUM", "transmission": "Automatic", "deposit": 5000, "mileage": 1000, "age": 27, "cost": 2888, "discounted_cost": 2454, "image":"https://www.avis.com.tr/Avis/media/Avis/Cars/m-volvo-xc40.png"},

    {"car_no": 8, "name": "Fiat Egea", "office_no": 3, "location": "MANISA", "date": "2024-01-01", "time": "02:00", "type": "ECONOMIC", "transmission": "Manual", "deposit": 2500, "mileage": 1000, "age": 25, "cost": 1035, "discounted_cost": 879, "image":"https://www.avis.com.tr/Avis/media/Avis/Cars/n-fiat-egea.png"},
    {"car_no": 9, "name": "Renault Clio AT", "office_no": 3, "location": "MANISA", "date": "2024-01-01", "time": "04:00", "type": "ECONOMIC", "transmission": "Automatic", "deposit": 2500, "mileage": 1000, "age": 21, "cost": 1089, "discounted_cost": 926, "image":"https://www.avis.com.tr/Avis/media/Avis/Cars/f-renault-clio-at.png"},
    {"car_no": 10, "name": "Peugeot 2008", "office_no": 3, "location": "MANISA", "date": "2022-03-01", "time": "04:00", "type": "COMFORT", "transmission": "Automatic", "deposit": 3000, "mileage": 1000, "age": 23, "cost": 1524, "discounted_cost": 1295, "image":"https://www.avis.com.tr/Avis/media/Avis/Cars/o-ford-focus.png"},
    {"car_no": 11, "name": "Audi A3", "office_no": 3, "location": "MANISA", "date": "2024-01-01", "time": "04:00", "type": "PRESTIGE", "transmission": "Automatic", "deposit": 3500, "mileage": 1000, "age": 25, "cost": 2171, "discounted_cost": 1844, "image":"https://www.avis.com.tr/Avis/media/Avis/Cars/h-audi-a3.png"},
    {"car_no": 12, "name": "Volvo XC40", "office_no": 3, "location": "MANISA", "date": "2022-03-01", "time": "04:00", "type": "PREMIUM", "transmission": "Automatic", "deposit": 5000, "mileage": 1000, "age": 27, "cost": 2888, "discounted_cost": 2454, "image":"https://www.avis.com.tr/Avis/media/Avis/Cars/m-volvo-xc40.png"},

    {"car_no": 13, "name": "Fiat Egea", "office_no": 4, "location": "AYDIN TOWN", "date": "2024-01-01", "time": "02:00", "type": "ECONOMIC", "transmission": "Manual", "deposit": 2500, "mileage": 1000, "age": 25, "cost": 1035, "discounted_cost": 879, "image":"https://www.avis.com.tr/Avis/media/Avis/Cars/n-fiat-egea.png"},
    {"car_no": 14, "name": "Audi A3", "office_no": 4, "location": "AYDIN TOWN", "date": "2024-01-01", "time": "04:00", "type": "PRESTIGE", "transmission": "Automatic", "deposit": 3500, "mileage": 1000, "age": 25, "cost": 2171, "discounted_cost": 1844, "image":"https://www.avis.com.tr/Avis/media/Avis/Cars/h-audi-a3.png"},
    {"car_no": 15, "name": "Volvo XC40", "office_no": 4, "location": "AYDIN TOWN", "date": "2022-03-01", "time": "04:00", "type": "PREMIUM", "transmission": "Automatic", "deposit": 5000, "mileage": 1000, "age": 27, "cost": 2888, "discounted_cost": 2454, "image":"https://www.avis.com.tr/Avis/media/Avis/Cars/m-volvo-xc40.png"},

    {"car_no": 16, "name": "Fiat Egea", "office_no": 2, "location": "IZMIR BORNOVA TOWN", "date": "2024-01-01", "time": "02:00", "type": "ECONOMIC", "transmission": "Manual", "deposit": 2500, "mileage": 1000, "age": 25, "cost": 1035, "discounted_cost": 879, "image":"https://www.avis.com.tr/Avis/media/Avis/Cars/n-fiat-egea.png"},
    {"car_no": 17, "name": "Audi A3", "office_no": 2, "location": "IZMIR BORNOVA TOWN", "date": "2024-01-01", "time": "04:00", "type": "PRESTIGE", "transmission": "Automatic", "deposit": 3500, "mileage": 1000, "age": 25, "cost": 2171, "discounted_cost": 1844, "image":"https://www.avis.com.tr/Avis/media/Avis/Cars/h-audi-a3.png"},
    {"car_no": 18, "name": "Volvo XC40", "office_no": 2, "location": "IZMIR BORNOVA TOWN", "date": "2022-03-01", "time": "04:00", "type": "PREMIUM", "transmission": "Automatic", "deposit": 5000, "mileage": 1000, "age": 27, "cost": 2888, "discounted_cost": 2454, "image":"https://www.avis.com.tr/Avis/media/Avis/Cars/m-volvo-xc40.png"},
]
    
with app.app_context():
    for office_data in offices_data:
        office = Office.query.filter_by(office_no=office_data['office_no']).first()
        if office is None:
            office = Office(**office_data)
            db.session.add(office)

    for car_data in cars_data:
        car = Car.query.filter_by(car_no=car_data['car_no']).first()
        if car is None:
            car = Car(**car_data)
            db.session.add(car)
    db.session.commit()


@app.route("/", methods=['GET', 'POST'])
def home():
    # Check if the user is logged in
    user_id = session.get('user_id')
    
    # Fetch user information
    user = User.query.get(user_id)

    # If the user is logged in, filter offices based on the user's city
    if user:
        offices = Office.query.filter_by(city=user.city).all()
        selected_city = user.city
    else:
        offices = Office.query.all()
        selected_city = None

    return render_template('home.html', user=user, offices=offices, selected_city=selected_city)
    


@app.route('/search_cars', methods=['GET'])
def search_cars():
    # Get filter parameters from the request
    office_no = request.args.get('office_no')
    date = request.args.get('date')
    time = request.args.get('time')
    car_type = request.args.get('type')
    order_by = request.args.get('order_by')  # 'asc' or 'desc'
    transmission = request.args.get('transmission')

    # Query cars based on the provided parameters
    query = db.session.query(Car)

    if office_no:
        query = query.filter_by(office_no=office_no)

    if date:
        query = query.filter_by(date=date)

    if time:
        query = query.filter_by(time=time)

    if car_type:
        query = query.filter_by(type=car_type)

    if transmission:
        query = query.filter_by(transmission=transmission)

    # Apply order by price
    if order_by == 'asc':
        query = query.order_by(Car.cost.asc())
    elif order_by == 'desc':
        query = query.order_by(Car.cost.desc())

    cars = query.all()

    user = None
    if 'user_id' in session:
        # Assuming user information is stored in the session, adjust this based on your authentication mechanism
        user = User.query.get(session['user_id'])

    return render_template('search.html', cars=cars, user=user)

# Route for handling Google login
@app.route('/google-login', methods=['POST'])
def google_login():
    # Extract user information from the Google authentication response
    google_user_info = {
        'name': request.form.get('name'),
        'email': request.form.get('email'),
        # Add other relevant information
    }

    # Check if the user already exists in the database
    user = User.query.filter_by(email=google_user_info['email']).first()

    if not user:
        # If the user doesn't exist, create a new User record
        new_user = User(
            name=google_user_info['name'],
            surname = "",
            email = google_user_info['email'],
            password = "password",
            country = "Turkey",
            city = "İzmir"
            # Set other attributes
        )
        db.session.add(new_user)
        db.session.commit()

        # Log in the new user
        user = new_user

    # Store user information in the session
    session['user_id'] = user.id

    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email, password=password).first()

        if user:
            # Store user information in session
            session['user_id'] = user.id
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid email or password')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        country = request.form['country']
        city = request.form['city']

        # Check if the password matches the confirmation
        if password != confirm_password:
            return render_template('register.html', error='Password and Confirm Password do not match')

        # Check if the user already exists in the database
        if User.query.filter_by(email=email).first():
            return render_template('register.html', error='Email already registered')

        # Add the new user to the database
        new_user = User(name=name, surname=surname, email=email, password=password, country=country, city=city)
        db.session.add(new_user)
        db.session.commit()

        # Redirect to the login page after successful registration
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout', methods=['GET'])
def logout():
    # Clear the user session
    session.pop('user_id', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)