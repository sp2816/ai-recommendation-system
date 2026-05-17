import "./Dashboard.css";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import API from "../../api/productApi";

function Dashboard() {
  const [products, setProducts] =
    useState([]);

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts =
    async () => {
      try {
        const response =
          await API.get("/products");

        setProducts(
          response.data.products
        );
      } catch (error) {
        console.log(error);
      }
    };

  return (
  <div className="dashboard">

    <section className="hero-section">
      <h1>
        AI Fashion Recommendation
      </h1>

      <p>
        Discover personalized
        fashion recommendations
        based on your style.
      </p>

      <button>
        Explore Now
      </button>
    </section>


    {/* Recommended Products */}
    <section className="products-section">

      <h2>
        Recommended For You
      </h2>

      <div className="product-grid">

        {products
          .slice(0, 8)
          .map((product) => (

          <Link
            key={product.article_id}
            to={`/product/${product.article_id}`}
            className="product-link"
          >
            <div className="product-card">

              <img
                src={
                  product.image_url ||
                  "https://via.placeholder.com/250"
                }
                alt={
                  product.product_name
                }
              />

              <h3>
                {
                  product.product_name
                }
              </h3>

              <p>
                ₹{product.price}
              </p>

            </div>
          </Link>

        ))}

      </div>

    </section>


    {/* Trending Products */}
    <section className="products-section">

      <h2>
        Trending Fashion
      </h2>

      <div className="product-grid">

        {products
          .slice(8, 16)
          .map((product) => (

          <Link
            key={product.article_id}
            to={`/product/${product.article_id}`}
            className="product-link"
          >
            <div className="product-card">

              <img
                src={
                  product.image_url ||
                  "https://via.placeholder.com/250"
                }
                alt={
                  product.product_name
                }
              />

              <h3>
                {
                  product.product_name
                }
              </h3>

              <p>
                ₹{product.price}
              </p>

            </div>
          </Link>

        ))}

      </div>

    </section>

  </div>
);
}

export default Dashboard;