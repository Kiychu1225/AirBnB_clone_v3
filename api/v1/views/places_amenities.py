#!/usr/bin/python3
"""Implements routes for managing the link between Place and Amenity objects"""
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views
from models import storage
from os import getenv
from flask import jsonify, abort
from flasgger.utils import swag_from

mode = getenv("HBNB_TYPE_STORAGE")


@app_views.route("/places/<place_id>/amenities", methods=["GET"],
                 strict_slashes=False)
@swag_from('documentation/place_amenity/get_places_amenities.yml',
           methods=['GET'])
def get_amenities_by_place(place_id):
    """Retrieves all amenities associated with a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if mode == "db":
        return jsonify([amenity.to_dict() for amenity in place.amenities])
    else:
        return jsonify([
            storage.get(Amenity, _id).to_dict() for _id in place.amenity_ids
        ])


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
@swag_from('documentation/place_amenity/delete_place_amenities.yml',
           methods=['DELETE'])
def delete_amenity_from_place(place_id, amenity_id):
    """Deletes an Amenity object associated with a Place object"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if mode == "db":
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity.id not in place.amenity_id:
            abort(404)
        place.amenity_id.remove(amenity.id)
    amenity.delete()
    storage.save()

    return jsonify({})


@app_views.route("places/<place_id>/amenities/<amenity_id>", methods=["POST"],
                 strict_slashes=False)
@swag_from('documentation/place_amenity/post_place_amenities.yml',
           methods=['POST'])
def insert_amenity_in_place(place_id, amenity_id):
    """Inserts a new Amenity object into a Place object"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if mode == "db":
        if amenity in place.amenities:
            return jsonify(amenity.to_dict())
        else:
            place.amenities.append(amenity)
    else:
        if amenity.id in place.amenity_id:
            return jsonify(amenity.to_dict())
        else:
            place.amenity_id.append(amenity.id)
    storage.save()
    return jsonify(amenity.to_dict()), 201

