import os
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_pymongo import PyMongo

app = Flask(__name__)

# MongoDB Configuration
app.config["MONGO_URI"] = os.environ.get("MONGO_URI", "mongodb://localhost:27017/carDB")
mongo = PyMongo(app)
cars_collection = mongo.db.cars

# Home Page - List All Cars
@app.route('/')
def index():
    cars = list(cars_collection.find())
    return render_template('index.html', cars=cars)

# Add Car Form
@app.route('/add', methods=['GET', 'POST'])
def add_car():
    if request.method == 'POST':
        car = {
            "make": request.form['make'],
            "model": request.form['model'],
            "year": int(request.form['year'])
        }
        cars_collection.insert_one(car)
        return redirect(url_for('index'))
    return render_template('add_car.html')

# Car Details (View, Update, Delete)
@app.route('/car/<car_id>', methods=['GET', 'POST', 'DELETE'])
def car_details(car_id):
    from bson.objectid import ObjectId
    car = cars_collection.find_one({"_id": ObjectId(car_id)})

    if request.method == 'POST':
        cars_collection.update_one(
            {"_id": ObjectId(car_id)},
            {"$set": {
                "make": request.form['make'],
                "model": request.form['model'],
                "year": int(request.form['year'])
            }}
        )
        return redirect(url_for('index'))

    if request.method == 'DELETE':
        cars_collection.delete_one({"_id": ObjectId(car_id)})
        return jsonify({"message": "Car deleted"})

    return render_template('car_details.html', car=car)

if __name__ == '__main__':
    app.run(debug=True)
