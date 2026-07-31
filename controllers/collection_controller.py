from flask import request, jsonify

from database.db import db
from models.collection import Collection


# GET /api/collections
def get_collections():

    collections = Collection.query.all()

    return jsonify({
        "collections": [collection.to_dict() for collection in collections]
    })


# GET /api/collections/<id>
def get_collection(collection_id):

    collection = Collection.query.get(collection_id)

    if not collection:
        return jsonify({
            "message": "Collection not found"
        }), 404

    return jsonify(collection.to_dict())


# POST /api/collections
def create_collection():

    data = request.get_json()

    if not data:
        data = {}

    name = data.get("name")
    description = data.get("description")
    image = data.get("image")
    featured = data.get("featured", False)

    if not name:
        return jsonify({
            "message": "Name is required."
        }), 400

    collection = Collection(
        name=name,
        description=description,
        image=image,
        featured=featured
    )

    db.session.add(collection)
    db.session.commit()

    return jsonify({
        "message": "Collection created successfully.",
        "collection": collection.to_dict()
    }), 201


# PUT /api/collections/<id>
def update_collection(collection_id):

    collection = Collection.query.get(collection_id)

    if not collection:
        return jsonify({
            "message": "Collection not found."
        }), 404

    data = request.get_json() or {}

    collection.name = data.get("name", collection.name)
    collection.description = data.get("description", collection.description)
    collection.image = data.get("image", collection.image)
    collection.featured = data.get("featured", collection.featured)

    db.session.commit()

    return jsonify({
        "message": "Collection updated successfully.",
        "collection": collection.to_dict()
    })


# DELETE /api/collections/<id>
def delete_collection(collection_id):

    collection = Collection.query.get(collection_id)

    if not collection:
        return jsonify({
            "message": "Collection not found."
        }), 404

    db.session.delete(collection)
    db.session.commit()

    return jsonify({
        "message": "Collection deleted successfully."
    })
