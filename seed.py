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

    print("Creating visible products...")

    products = [
        Product(
            name="CALIM Beanie",
            description="Soft custom beanie with a premium finish.",
            price=1500,
            stock=25,
            image="https://images.unsplash.com/photo-1576871337632-b9aef4c17ab9?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8YmVhbmllcyUyMHdpdGglMjByaXZldHN8ZW58MHx8MHx8fDA%3D",
            collection_id=hoodies.id
        ),
        Product(
            name="CALIM Jeans",
            description="Custom made jeans for a perfect fit.",
            price=5000,
            stock=40,
            image="https://images.unsplash.com/photo-1697678207628-6758ecf9a2cc?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fGN1c3RvbSUyMGJhZ2d5JTIwamVhbnN8ZW58MHx8MHx8fDA%3D",
            collection_id=tshirts.id
        ),
        Product(
            name="CALIM Leather Jacket",
            description="A genuine leather jacket for all styling options.",
            price=2000,
            stock=50,
            image="https://plus.unsplash.com/premium_photo-1731950912462-9caa3905627d?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8Y3VzdG9tJTIwbGVhdGhlciUyMGphY2tldHxlbnwwfHwwfHx8MA%3D%3D",
            collection_id=caps.id
        )
    ]

    db.session.add_all(products)

    db.session.commit()

    print("Database seeded successfully!")