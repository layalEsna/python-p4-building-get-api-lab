#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate


from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakery_dict = [bakery.to_dict() for bakery in Bakery.query.all()]
    return jsonify(bakery_dict)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id==id).first()
    if bakery:
        bk =bakery.to_dict()
        status = 200
    else:
        bk = 'No bakery found.'
        status = 404
    return make_response(jsonify(bk), status)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    backed_goods = [bk.to_dict() for bk in BakedGood.query.order_by(BakedGood.price.desc())]
    return jsonify(backed_goods)
    

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good(): 
    dict_goods = [bk.to_dict() for bk in BakedGood.query.order_by(BakedGood.price.desc())]
    most_expensive_good = dict_goods[0]
    return jsonify(most_expensive_good)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
