from app import app
from database.db import db, bcrypt

from models.user import User
from models.collection import Collection
from models.product import Product


with app.app_context():

    print("Clearing existing seed data...")

    db.session.query(Product).delete()
    db.session.query(Collection).delete()
    db.session.query(User).delete()

    db.session.commit()

    print("Creating admin user...")

    admin = User(
        full_name="Admin User",
        email="admin@calim.com",
        password=bcrypt.generate_password_hash("Admin123").decode("utf-8"),
        phone="0712345678",
        role="admin"
    )

    customer = User(
        full_name="John Doe",
        email="john@example.com",
        password=bcrypt.generate_password_hash("password123").decode("utf-8"),
        phone="0799999999",
        role="customer"
    )

    db.session.add_all([admin, customer])
    db.session.commit()

    print("Creating collections...")

    hoodies = Collection(
        name="Hoodies",
        description="Premium streetwear hoodies.",
        image="https://images.unsplash.com/photo-1512436991641-6745cdb1723f?w=800&auto=format&fit=crop&q=60",
        featured=True
    )

    tshirts = Collection(
        name="T-Shirts",
        description="Classic oversized tees.",
        image="https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=800&auto=format&fit=crop&q=60",
        featured=True
    )

    caps = Collection(
        name="Caps",
        description="Stylish snapback caps.",
        image="https://images.unsplash.com/photo-1512436991641-6745cdb1723f?w=800&auto=format&fit=crop&q=60",
        featured=False
    )

    db.session.add_all([hoodies, tshirts, caps])
    db.session.commit()

    print("Creating products...")

    products = [

        Product(
            name="CALIM Beanie",
            description="Soft custom beanie with a premium finish.",
            price=3500,
            stock=25,
            image="https://images.unsplash.com/photo-1576871337632-b9aef4c17ab9?w=500&auto=format&fit=crop&q=60",
            collection_id=hoodies.id
        ),

        Product(
            name="CALIM Leather Jacket",
            description="100% genuine leather jacket.",
            price=5800,
            stock=40,
            image="https://images.unsplash.com/photo-1623854156816-4c4fc355ffc7?w=500&auto=format&fit=crop&q=60",
            collection_id=tshirts.id
        ),

        Product(
            name="CALIM Custom Jeans",
            description="Custom jeans with CALIM logo.",
            price=1500,
            stock=50,
            image="https://plus.unsplash.com/premium_photo-1674828600712-7d0caab39109?w=500&auto=format&fit=crop&q=60",
            collection_id=caps.id
        ),

    ]

    db.session.add_all(products)
    db.session.commit()

    print("Products created successfully!")
    print("Database seeded successfully!")