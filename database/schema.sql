-- ==========================
-- USERS TABLE
-- ==========================
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    age INT,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================
-- PRODUCTS TABLE
-- ==========================
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    article_id BIGINT UNIQUE NOT NULL,
    product_name VARCHAR(255),
    product_type_name VARCHAR(255),
    product_group_name VARCHAR(255),
    colour_group_name VARCHAR(255),
    price DECIMAL(10,2),
    description TEXT,
    image_url TEXT,
    product_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================
-- WISHLIST TABLE
-- ==========================
CREATE TABLE wishlist (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    product_id INT REFERENCES products(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================
-- VIEW HISTORY TABLE
-- ==========================
CREATE TABLE view_history (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    product_id INT REFERENCES products(id) ON DELETE CASCADE,
    viewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================
-- SEARCH HISTORY TABLE
-- ==========================
CREATE TABLE search_history (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    search_query TEXT,
    searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================
-- USER INTERACTIONS TABLE
-- ==========================
CREATE TABLE user_interactions (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    product_id INT REFERENCES products(id) ON DELETE CASCADE,
    interaction_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);