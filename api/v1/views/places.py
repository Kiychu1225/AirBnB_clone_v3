#!/usr/bin/python3
"""Implements routes for managing Place objects"""
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.user import User
from models.state import State
from models.amenity import Amenity
from flasgger.utils import swag_from


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
@swag_from('documentation/place/get_places.yml', methods=['GET'])
def get_places_by_city(city_id):
    """Retrieves place objects by city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route("/places/<place_id>", methods=["GET"],
                 strict_slashes=False)
@swag_from('documentation/place/get_place.yml', methods=['GET'])
def get_place(place_id):
    """Retrieves a Place object by its ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
@swag_from('documentation/place/delete_place.yml', methods=['DELETE'])
def delete_place(place_id):
    """Deletes a Place object by its ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({})


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
@swag_from('documentation/place/post_place.yml', methods=['POST'])
def create_place(city_id):
    """Creates a new Place object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    req = request.get_json()
    if type(req) != dict:
        abort(400, description="Not a JSON")
    if not req.get("user_id"):
        abort(400, description="Missing user_id")
    user = storage.get(User, req.get("user_id"))
    if user is None:
        abort(404)
    if not req.get("name"):
        abort(400, description="Missing name")
    new_place = Place(**req)
    new_place.city_id = city_id
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places_search", methods=["POST"],
                 strict_slashes=False)
@swag_from('documentation/place/put_place.yml', methods=['PUT'])
def search_places():
    """Retrieves Place objects based on the request body"""
    req = request.get_json()
    if type(req) != dict:
        abort(400, description="Not a JSON")
    state_ids = req.get("states", [])
    city_ids = req.get("cities", [])
    amenity_ids = req.get("amenities", [])
    places = []
    if state_ids == city_ids == []:
        places = storage.all(Place).values()
    else:
        states = [
            storage.get(State, _id) for _id in state_ids
            if storage.get(State, _id)
        ]
        cities = [city for state in states for city in state.cities]
        cities += [
            storage.get(City, _id) for _id in city_ids
            if storage.get(City, _id)
        ]
        cities = list(set(cities))
        places = [place for city in cities for place in city.places]

    amenities = [
        storage.get(Amenity, _id) for _id in amenity_ids
        if storage.get(Amenity, _id)
    ]

    res = []
    for place in places:
        res.append(place.to_dict())
        for amenity in amenities:
            if amenity not in place.amenities:
                res.pop()
                break

    return jsonify(res)


@app_views.route("/places/<place_id>", methods=["PUT"],
                 strict_slashes=False)
@swag_from('documentation/place/post_search.yml', methods=['POST'])
def update_place(place_id):
    """Updates a Place object by its ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    req = request.get_json()
    if type(req) != dict:
        abort(400, description="Not a JSON")
    for key, value in req.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200

