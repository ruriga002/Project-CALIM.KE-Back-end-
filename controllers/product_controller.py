from flask import request, jsonify
from flask_jwt_extended import jwt_required

from database.db import db

from models.product import Product
from models.collection import Collection

from middleware.admin_required import admin_required


# ==========================
# GET ALL PRODUCTS
# Public
# ==========================
def get_products():

    products = Product.query.all()

    return jsonify({
        "products": [product.to_dict() for product in products]
    }), 200


# ==========================
# GET SINGLE PRODUCT
# Public
# ==========================
def get_product(product_id):

    product = Product.query.get(product_id)

    if not product:
        return jsonify({
            "message": "Product not found."
        }), 404

    return jsonify(product.to_dict()), 200


# ==========================
# CREATE PRODUCT
# Admin Only
# ==========================
@jwt_required()
@admin_required
def create_product():

    data = request.get_json() or {}

    required = [
        "name",
        "description",
        "price",
        "stock",
        "image",
        "collection_id"
    ]

    for field in required:

        if not data.get(field):

            return jsonify({
                "message": f"{field} is required."
            }), 400

    collection = Collection.query.get(data["collection_id"])

    if not collection:

        return jsonify({
            "message": "Collection not found."
        }), 404

    product = Product(

        name=data["name"],
        description=data["description"],
        price=data["price"],
        stock=data["stock"],
        image=data["image"],
        collection_id=data["collection_id"]

    )

    db.session.add(product)
    db.session.commit()

    return jsonify({
        "message": "Product created successfully.",
        "product": product.to_dict()
    }), 201


# ==========================
# UPDATE PRODUCT
# Admin Only
# ==========================
@jwt_required()
@admin_required
def update_product(product_id):

    product = Product.query.get(product_id)

    if not product:

        return jsonify({
            "message": "Product not found."
        }), 404

    data = request.get_json() or {}

    if "collection_id" in data:

        collection = Collection.query.get(data["collection_id"])

        if not collection:

            return jsonify({
                "message": "Collection not found."
            }), 404

    product.name = data.get("name", product.name)
    product.description = data.get("description", product.description)
    product.price = data.get("price", product.price)
    product.stock = data.get("stock", product.stock)
    product.image = data.get("image", product.image)
    product.collection_id = data.get(
        "collection_id",
        product.collection_id
    )

    db.session.commit()

    return jsonify({
        "message": "Product updated successfully.",
        "product": product.to_dict()
    }), 200


# ==========================
# DELETE PRODUCT
# Admin Only
# ==========================
@jwt_required()
@admin_required
def delete_product(product_id):

    product = Product.query.get(product_id)

    if not product:

        return jsonify({
            "message": "Product not found."
        }), 404

    db.session.delete(product)
    db.session.commit()

    return jsonify({
        "message": "Product deleted successfully."
    }), 200