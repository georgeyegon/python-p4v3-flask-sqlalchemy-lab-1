from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///earthquakes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Earthquake(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    magnitude = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(80), nullable=False)
    year = db.Column(db.Integer, nullable=False)


def seed_database():
    """Seed the database with initial data."""
    if not Earthquake.query.first():
        db.session.add(Earthquake(id=1, magnitude=9.0, location="Tokyo", year=2011))
        db.session.add(Earthquake(id=2, magnitude=8.0, location="San Francisco", year=1906))
        db.session.commit()


# Initialize the app and seed the database
with app.app_context():
    db.create_all()
    seed_database()


@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake_by_id(id):
    earthquake = db.session.get(Earthquake, id)
    if earthquake:
        return jsonify({
            "id": earthquake.id,
            "magnitude": earthquake.magnitude,
            "location": earthquake.location,
            "year": earthquake.year
        }), 200
    return jsonify({"error": "Earthquake not found"}), 404


@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter_by(magnitude=magnitude).all()
    if earthquakes:
        return jsonify({
            "count": len(earthquakes),
            "quakes": [{
                "id": eq.id,
                "magnitude": eq.magnitude,
                "location": eq.location,
                "year": eq.year
            } for eq in earthquakes]
        }), 200
    return jsonify({
        "count": 0,
        "quakes": []
    }), 404


if __name__ == '__main__':
    app.run(debug=True)
