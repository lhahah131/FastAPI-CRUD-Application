CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL
);

INSERT INTO items(name, description, price) VALUES
('Default Laptop', 'Inisialisasi otomatis dari entrypoint', 1200.0),
('Default Mouse', 'Inisialisasi otomatis dari entrypoint', 25.0);