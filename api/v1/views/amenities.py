#!/usr/bin/python3
"""Defines routes for Amenity objects"""
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort, request
from flasgger.utils import swag_from


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/amenity/all_amenities.yml')
def get_all_amenities():
    """Retrieve all Amenities"""
    res = [amenity.to_dict() for amenity in storage.all(Amenity).values()]
    return jsonify(res)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/amenity/get_amenity.yml', methods=['GET'])
def get_amenity_by_id(amenity_id):
    """Retrieve an Amenity by its ID"""
    res = storage.get(Amenity, amenity_id)
    if res is None:
        abort(404)
    return jsonify(res.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/amenity/delete_amenity.yml', methods=['DELETE'])
def delete_amenity_by_id(amenity_id):
    """Delete an Amenity by its ID"""
    amenity = storage.get(Amenity, amenity

