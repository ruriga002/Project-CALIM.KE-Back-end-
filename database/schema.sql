CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    stock INTEGER DEFAULT 0,
    image VARCHAR(255),
    collection_id INTEGER NOT NULL,
    FOREIGN KEY (collection_id) REFERENCES collections(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS collections (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL
);
INSERT INTO products
(name, description, price, stock, image, collection_id)
VALUES
(
'CALIM Beanie',
'Soft custom beanie with a premium finish.',
3500,
25,
'https://images.unsplash.com/photo-1517841905240-472988babdf9?w=500&auto=format&fit=crop&q=60',
1
),
(
'CALIM Leather Jacket',
'100% genuine leather jacket.',
5800,
40,
'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500&auto=format&fit=crop&q=60',
2
),
(
'CALIM jeans',
'custom jeans with CALIM logo.',
1500,
50,
'https://images.unsplash.com/photo-1588850561407-ca4c6f2f3f4a?w=500&auto=format&fit=crop&q=60',
1
);

INSERT INTO collections (name)
VALUES
('Accessories'),
('Outerwear'),
('Bottoms');