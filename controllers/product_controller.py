from flask import request, jsonify

from database.db import db

from models.product import Product
from models.collection import Collection


# GET /api/products
def get_products():

    products = Product.query.all()

    return jsonify({
        "products": [product.to_dict() for product in products]
    })


# GET /api/products/<id>
def get_product(product_id):

    product = Product.query.get(product_id)

    if not product:
        return jsonify({
            "message": "Product not found"
        }), 404

    return jsonify(product.to_dict())


# POST /api/products
def create_product():

    data = request.get_json()

    required = [
        "name",
        "description",
        "price",
        "stock",
        "image",
        "collection_id"
    ]

    for field in required:
        if field not in data:
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


# PUT /api/products/<id>
def update_product(product_id):

    product = Product.query.get(product_id)

    if not product:
        return jsonify({
            "message": "Product not found."
        }), 404

    data = request.get_json()

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
    })


# DELETE /api/products/<id>
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
    })