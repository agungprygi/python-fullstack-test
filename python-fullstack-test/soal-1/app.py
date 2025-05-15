from flask import Flask, request, jsonify
from model import db, MyClient
from config import DATABASE_URL, REDIS_URL
import redis
import json
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db.init_app(app)

r = redis.StrictRedis.from_url(REDIS_URL, decode_responses=True)

def save_to_redis(slug, data):
    r.set(slug, json.dumps(data))

@app.before_request
def create_tables():
    db.create_all()

@app.route('/clients', methods=['POST'])
def create_client():
    data = request.json
    client = MyClient(**data, created_at=datetime.now())
    db.session.add(client)
    db.session.commit()
    save_to_redis(client.slug, client.to_dict())
    return jsonify(client.to_dict()), 201

@app.route('/clients/<slug>', methods=['GET'])
def get_client(slug):
    json_data = r.get(slug)
    if json_data:
        return jsonify(json.loads(json_data))
    client = MyClient.query.filter_by(slug=slug).first_or_404()
    save_to_redis(slug, client.to_dict())
    return jsonify(client.to_dict())

@app.route('/clients/<slug>', methods=['PUT'])
def update_client(slug):
    client = MyClient.query.filter_by(slug=slug).first_or_404()
    data = request.json
    for key, value in data.items():
        setattr(client, key, value)
    client.updated_at = datetime.now()
    db.session.commit()
    save_to_redis(slug, client.to_dict())
    return jsonify(client.to_dict())

@app.route('/clients/<slug>', methods=['DELETE'])
def delete_client(slug):
    client = MyClient.query.filter_by(slug=slug).first_or_404()
    db.session.delete(client)
    db.session.commit()
    r.delete(slug)
    return jsonify({'message': f'Client {slug} deleted'}), 200


if __name__ == '__main__':
    app.run(debug=True)