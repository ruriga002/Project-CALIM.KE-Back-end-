import os

from flask import Flask, jsonify
from flask_cors import CORS

from config import Config
from database.db import db, migrate, bcrypt, jwt, mail

# Import models (required for Flask-Migrate)
from models.user import User
from models.collection import Collection
from models.product import Product
from models.order import Order
from models.order_item import OrderItem
from models.cart import Cart
from models.contact import Contact

# Import blueprints
from routes.auth_routes import auth_bp
from routes.product_routes import product_bp
from routes.collection_routes import collection_bp
from routes.order_routes import order_bp
from routes.cart_routes import cart_bp
from routes.contact_routes import contact_bp
from routes.admin_routes import admin_bp


def create_app():

    app = Flask(__name__)
    app.url_map.strict_slashes = False

    # -----------------------------
    # Configuration
    # -----------------------------
    app.config.from_object(Config)

    # -----------------------------
    # Enable CORS (Development)
    # -----------------------------
    CORS(
        app,
        resources={r"/api/*": {"origins": "*"}}
    )

    # -----------------------------
    # Initialize Extensions
    # -----------------------------
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    # -----------------------------
    # Seed Initial Data
    # -----------------------------
    with app.app_context():

        db.create_all()

        if not Collection.query.first():

            hoodie_collection = Collection(
                name="Hoodies",
                description="Premium streetwear hoodies.",
                image="https://images.unsplash.com/photo-1512436991641-6745cdb1723f?w=500&auto=format&fit=crop&q=60",
                featured=True
            )

            tshirt_collection = Collection(
                name="T-Shirts",
                description="Classic oversized tees.",
                image="https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500&auto=format&fit=crop&q=60",
                featured=True
            )

            cap_collection = Collection(
                name="Caps",
                description="Stylish snapback caps.",
                image="https://images.unsplash.com/photo-1588850561407-ca4c6f2f3f4a?w=500&auto=format&fit=crop&q=60",
                featured=False
            )

            db.session.add_all([
                hoodie_collection,
                tshirt_collection,
                cap_collection
            ])

            db.session.commit()

        if not Product.query.first():

            hoodie = Collection.query.filter_by(
                name="Hoodies"
            ).first()

            tshirt = Collection.query.filter_by(
                name="T-Shirts"
            ).first()

            cap = Collection.query.filter_by(
                name="Caps"
            ).first()

            products = [

                Product(
                    name="CALIM Beanie",
                    description="Soft custom beanie with a premium finish.",
                    price=3500,
                    stock=25,
                    image="https://images.unsplash.com/photo-1576871337632-b9aef4c17ab9?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8QmVhbmllfGVufDB8fDB8fHww",
                    collection_id=hoodie.id
                ),

                Product(
                    name="CALIM Leather Jacket",
                    description="100% genuine leather jacket.",
                    price=5800,
                    stock=40,
                    image="https://images.unsplash.com/photo-1623854156816-4c4fc355ffc7?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8bGVhdGhlciUyMGphY2tldHxlbnwwfHwwfHx8MA%3D%3D",
                    collection_id=tshirt.id
                ),

                Product(
                    name="CALIM custom jeans",
                    description="custom jeans with CALIM logo.",
                    price=1500,
                    stock=50,
                    image="https://plus.unsplash.com/premium_photo-1674828600712-7d0caab39109?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTN8fGRlbmltfGVufDB8fDB8fHww",
                    collection_id=cap.id
                )

            ]

            db.session.add_all(products)
            db.session.commit()

    # -----------------------------
    # Register Blueprints
    # -----------------------------
    app.register_blueprint(
        auth_bp,
        url_prefix="/api/auth"
    )

    app.register_blueprint(
        product_bp,
        url_prefix="/api/products"
    )

    app.register_blueprint(
        collection_bp,
        url_prefix="/api/collections"
    )

    app.register_blueprint(
        order_bp,
        url_prefix="/api/orders"
    )

    app.register_blueprint(
        cart_bp,
        url_prefix="/api/cart"
    )

    app.register_blueprint(
        contact_bp,
        url_prefix="/api/contact"
    )

    app.register_blueprint(
        admin_bp,
        url_prefix="/api/admin"
    )

    # -----------------------------
    # Home Route
    # -----------------------------
    @app.route("/")
    def home():

        return jsonify({

            "success": True,
            "message": "Welcome to CALIM API",
            "version": "1.0.0",
            "status": "Running"

        })

    # -----------------------------
    # Health Check
    # -----------------------------
    @app.route("/health")
    def health():

        return jsonify({

            "success": True,
            "status": "Healthy"

        })

    return app


app = create_app()


if __name__ == "__main__":

    port = int(os.getenv("PORT", "5001"))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )