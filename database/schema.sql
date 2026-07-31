CREATE TABLE IF NOT EXISTS products (
  id SERIAL PRIMARY KEY,
  name VARCHAR(150) NOT NULL,
  slug VARCHAR(150) NOT NULL UNIQUE,
  price INTEGER NOT NULL DEFAULT 0,
  category VARCHAR(100) NOT NULL,
  description TEXT,
  image_url TEXT,
  in_stock BOOLEAN NOT NULL DEFAULT TRUE,
  rating NUMERIC(2, 1) DEFAULT 0.0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS collections (
  id SERIAL PRIMARY KEY,
  name VARCHAR(150) NOT NULL,
  slug VARCHAR(150) NOT NULL UNIQUE,
  description TEXT,
  image_url TEXT,
  featured BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

INSERT INTO products (name, slug, price, category, description, image_url, in_stock, rating)
VALUES
  ('Beanie 1', 'beanie-1', 1500, 'beanie', 'well crafted beanie for all types of styling.', 'https://images.unsplash.com/photo-1576871337632-b9aef4c17ab9?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8YmVhbmllcyUyMHdpdGglMjByaXZldHN8ZW58MHx8MHx8fDA%3D', TRUE, 8.8),
  ('jeans', 'custom-made-jeans', 5000, 'jeans', 'Custom made jeans for a perfect fit.', 'https://images.unsplash.com/photo-1697678207628-6758ecf9a2cc?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fGN1c3RvbSUyMGJhZ2d5JTIwamVhbnN8ZW58MHx8MHx8fDA%3D', TRUE, 9.7),
  ('CALIM leather jacket', 'jacket', 2000, 'jacket', 'a Genuine Generic leather jacket for all styling options and desings', 'https://plus.unsplash.com/premium_photo-1731950912462-9caa3905627d?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8Y3VzdG9tJTIwbGVhdGhlciUyMGphY2tldHxlbnwwfHwwfHx8MA%3D%3D', TRUE, 9.9);

INSERT INTO collections (name, slug, description, image_url, featured)
VALUES
  ('Winter Essentials', 'winter-essentials', 'Cozy staples for cold weather.', 'https://images.unsplash.com/photo-1512436991641-6745cdb1723f?w=800&auto=format&fit=crop&q=60', TRUE),
  ('Signature Denim', 'signature-denim', 'Tailored denim for everyday style.', 'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=800&auto=format&fit=crop&q=60', FALSE);
