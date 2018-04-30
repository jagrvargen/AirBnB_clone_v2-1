#!/usr/bin/python3
'''
   This module handles all default RestFul API actions for Review objects.
'''
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models import Review


@app_views.route('/places/<uuid:place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def all_reviews_by_place(place_id):
    '''
       Retrieves all Review objects from storage that for specified Review
    '''
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    reviews_list = []
    reviews = storage.all("Review")
    for k, v in reviews.items():
        if v.place_id == str(place_id):
            reviews_list.append(v.to_dict())

    return jsonify(reviews_list)


@app_views.route('/reviews/<uuid:review_id>', methods=['GET'],
                 strict_slashes=False)
def review_by_id(review_id):
    '''
       Retrieves a specified Review object from storage
    '''
    try:
        review = storage.get("Review", review_id)
        format_review = review.to_dict()
        return jsonify(format_review)
    except Exception:
        abort(404)


@app_views.route('/reviews/<uuid:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    '''
       Deletes a specified Review object from storage
    '''
    try:
        review = storage.get("Review", review_id)
        storage.delete(review)
        return jsonify({}), 200
    except Exception:
        abort(404)


@app_views.route('/places/<uuid:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    '''
       Creates a new Review object and saves it to storage
    '''
    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    if not request.json:
        abort(400)
        return jsonify({"error": "Not a JSON"})

    review_dict = request.get_json()
    if "user_id" not in review_dict:
        abort(400)
        return jsonify({"error": "Missing user_id"})
    elif "text" not in review_dict:
        abort(400)
        return jsonify({"error": "Missing text"})

    # Check that user_id is linked to actual User object
    user_check = storage.get("User", review_dict["user_id"])
    if not user_check:
        abort(404)

    review_text = review_dict["text"]
    user_id = review_dict["user_id"]
    review = Review(text=review_text, user_id=user_id, place_id=place_id)
    for k, v in review_dict.items():
        setattr(review, k, v)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<uuid:review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    '''
       Updates an existing Review object and saves it to storage
    '''
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    if not request.json:
        abort(400)
        return jsonify({"error": "Not a JSON"})

    req = request.get_json()
    for k, v in req.items():
        if k != "id" and k != "created_at" and k != "updated_at" and \
                k != "user_id" and k != "place_id":
            setattr(review, k, v)
    review.save()

    return jsonify(review.to_dict()), 200
