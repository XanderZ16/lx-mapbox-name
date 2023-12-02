from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
)
from pymongo import MongoClient

app = Flask(__name__)

password = 'Aa13245768'
db_cdn = f'mongodb+srv://xander:{
    password}@cluster0.hgsq4xy.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(db_cdn)
db = client.dbxander


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = list(db.restaurants.find({}, {'_id': False}))
    return jsonify({
        "result": "success",
        "restaurants": restaurants
    })


@app.route('/restaurant/create', methods=['POST'])
def create_restaurants():
    name = request.form.get('name')
    category = request.form.get('category')
    location = request.form.get('location')
    longitude = request.form.get('longitude')
    latitude = request.form.get('latitude')

    doc = {
        'name': name,
        'category': category,
        'location': location,
        'center': [longitude, latitude]
    }
    db.restaurants.insert_one(doc)
    return jsonify({
        'result': 'success',
        'msg': 'successfully created a restaurant'
    })

@app.route('/restaurant/delete', methods=['POST'])
def delete_restaurants():
    name = request.form.get('name')
    db.restaurants.delete_one({'name': name})
    return jsonify({
        'result': 'success',
        'msg': 'successfully deleted a restaurant'
    })

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
