import "./Dashboard.css";
import {
  useEffect,
  useState,
  useRef
} from "react";

import {
  Link,
  useLocation
} from "react-router-dom";

import API
from "../../api/productApi";

const CATEGORY_MATCHERS = {
  Dress: ["dress", "gown", "jumpsuit"],
  Top: ["top", "blouse", "shirt", "sweater", "cardigan", "t-shirt"],
  Trousers: ["trousers", "jeans", "leggings", "shorts", "pants"],
  Shoes: ["shoe", "shoes", "boot", "boots", "sneaker", "sneakers", "trainer", "trainers", "sandal", "sandals", "heel", "heels", "loafer", "loafers", "flat", "flats", "footwear"],
  Nightwear: ["nightwear", "sleepwear", "sleep", "pyjama", "pajama", "pyjamas", "pajamas", "robe", "underwear", "lingerie"]
};

function getProductSearchText(product) {
  return [
    product?.product_name,
    product?.product_type_name,
    product?.product_group_name,
    product?.description
  ]
    .filter(Boolean)
    .join(" ")
    .toLowerCase();
}

function matchesCategory(product, category) {
  if (category === "All") {
    return true;
  }

  const searchText = getProductSearchText(product);
  const categoryTerms = CATEGORY_MATCHERS[category] || [category.toLowerCase()];

  return categoryTerms.some((term) => searchText.includes(term));
}

function Dashboard() {

  const [products,
    setProducts] =
    useState([]);

  const [
    trendingProducts,
    setTrendingProducts
  ] = useState([]);

  const [
    selectedCategory,
    setSelectedCategory
  ] = useState("All");

  const productsRef =
    useRef(null);

  const location =
    useLocation();

  const searchParams =
    new URLSearchParams(
      location.search
    );

  const searchQuery =
    searchParams.get(
      "search"
    );

  const categories = [
    "All",
    "Dress",
    "Top",
    "Trousers",
    "Shoes",
    "Nightwear"
  ];

  useEffect(() => {

    fetchProducts();
    fetchTrendingProducts();

  }, [
  searchQuery,
  selectedCategory
]);

  const fetchProducts =
    async () => {

      try {

        let response;

        if (
          searchQuery
        ) {

          response =
            await API.get(
              `/products/search?query=${searchQuery}`
            );

        } else if (
          selectedCategory
          !== "All"
        ) {

          response =
            await API.get(
              `/products?category=${encodeURIComponent(
                selectedCategory
              )}`
            );

        } else {

          response =
            await API.get(
              "/products"
            );
        }

        setProducts(
          response.data.products
        );

      } catch (error) {

        console.log(error);
      }
    };

  const fetchTrendingProducts =
    async () => {

      try {

        const response =
          await API.get(
            selectedCategory === "All"
              ? "/products/trending"
              : `/products/trending?category=${encodeURIComponent(
                selectedCategory
              )}`
          );

        setTrendingProducts(
          response.data.products
        );

      } catch (error) {

        console.log(error);
      }
    };

  const handleExplore =
    () => {

      productsRef.current
      ?.scrollIntoView({
        behavior:
        "smooth"
      });
    };

  const displayedProducts =
  searchQuery
  ? products
  : selectedCategory
    === "All"
  ? products
  : products.filter(
      (product) =>
        matchesCategory(
          product,
          selectedCategory
        )
    );

  return (
    <div className="dashboard">

      {!searchQuery && (

        <section className="hero-section">

          <h1>
            AI Fashion Recommendation
          </h1>

          <p>
            Discover personalized
            fashion recommendations
            based on your style.
          </p>

          <button
            onClick={
              handleExplore
            }
          >
            Explore Now
          </button>

        </section>
      )}

      {!searchQuery && (

        <section
          className="category-section"
        >

          {categories.map(
            (category) => (

            <button
              key={category}

              className={
                selectedCategory
                === category
                ? "category-btn active"
                : "category-btn"
              }

              onClick={() =>
                setSelectedCategory(
                  category
                )
              }
            >

              {category}

            </button>
          ))}

        </section>
      )}

      <section
        ref={productsRef}
        className="products-section"
      >

        <h2>

          {searchQuery
            ? `Search Results for "${searchQuery}"`
            : "Recommended For You"
          }

        </h2>

        <div
          className="product-grid"
        >

          {displayedProducts
          .length > 0 ? (

            displayedProducts.map(
              (product) => (

              <Link
                key={
                  product.article_id
                }

                to={`/product/${
                  product.article_id
                }`}

                className="product-link"
              >

                <div
                  className="product-card"
                >

                  <img
                    src={
                      product.image_url
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
                    ₹{
                      product.price
                    }
                  </p>

                </div>

              </Link>
            ))

          ) : (

            <div className="empty-search">

              <h2>
                No Products Found
              </h2>

              <p>
                Try another search.
              </p>

            </div>
          )}

        </div>

      </section>

      {!searchQuery && (

        <section
          className="products-section"
        >

          <h2>
            Trending Fashion
          </h2>

          <div
            className="product-grid"
          >

            {trendingProducts.map(
              (product) => (

              <Link
                key={
                  product.article_id
                }

                to={`/product/${
                  product.article_id
                }`}

                className="product-link"
              >

                <div
                  className="product-card"
                >

                  <img
                    src={
                      product.image_url
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
                    ₹{
                      product.price
                    }
                  </p>

                </div>

              </Link>
            ))}

          </div>

        </section>
      )}

    </div>
  );
}

export default Dashboard;