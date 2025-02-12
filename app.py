import os
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_pymongo import PyMongo

app = Flask(__name__)

# MongoDB Config
app.config["MONGO_URI"] = os.environ.get("MONGO_URI", "mongodb://localhost:27017/carDB")
mongo = PyMongo(app)
cars_collection = mongo.db.cars

# Liveness Probe
@app.route('/health', methods=['GET'])
def healthz():
    return jsonify({"status": "healthy"}), 200

# Readiness Probe
@app.route('/ready', methods=['GET'])
def readyz():
    
    try:
        mongo.db.command("ping")  
        return jsonify({"status": "ready"}), 200
    except Exception as e:
        return jsonify({"status": "not ready", "error": str(e)}), 500


# Home Page
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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

