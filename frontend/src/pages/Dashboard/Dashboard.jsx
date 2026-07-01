import "./Dashboard.css";

import {
  useEffect,
  useState
} from "react";

import {
  Link,
  useLocation
} from "react-router-dom";

import API from "../../api/productApi";

import RecommendedProducts from "../../components/recommendedProducts";

import {
  getLoggedInUser
} from "../../services/recommendationContext";

import {
  getRecommendations
} from "../../services/recommendationService";

const FALLBACK_IMAGE =
  "data:image/svg+xml;charset=UTF-8," +
  encodeURIComponent(`
<svg xmlns="http://www.w3.org/2000/svg"
     width="300"
     height="400">

<rect width="100%" height="100%" fill="#f5f5f5"/>

<text
x="50%"
y="45%"
text-anchor="middle"
font-size="58">
🖼️
</text>

<text
x="50%"
y="58%"
text-anchor="middle"
font-size="18"
fill="#777"
font-family="Arial">
No Image
</text>

<text
x="50%"
y="66%"
text-anchor="middle"
font-size="15"
fill="#999"
font-family="Arial">
Available
</text>

</svg>
`);


function Dashboard() {
  const location = useLocation();
  const currentUser = getLoggedInUser();
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const searchParams = new URLSearchParams(location.search);
  const searchQuery = searchParams.get("search") || "";

  useEffect(() => {
    let isActive = true;

    const fetchProducts = async () => {
      setLoading(true);
      setError("");

      try {
        let endpoint;

        if (searchQuery) {
          endpoint = `/products/search?query=${encodeURIComponent(searchQuery)}`;
        } else if (currentUser?.id) {
          const recommendationResponse = await getRecommendations(currentUser.id);
          const preferredCategory =
            recommendationResponse?.user_profile?.interest_categories?.[0] ||
            recommendationResponse?.user_profile?.favorite_product_type;

          endpoint = preferredCategory
            ? `/products/trending?category=${encodeURIComponent(preferredCategory)}`
            : "/products/trending";
        } else {
          const response = await API.get("/products?limit=80");

          if (!isActive) {
            return;
          }

          setProducts(response.data.products || []);
          return;
        }

        const response = await API.get(endpoint);

        if (!isActive) {
          return;
        }

        setProducts(response.data.products || []);
      } catch (fetchError) {
        if (!isActive) {
          return;
        }

        setProducts([]);
        setError("Failed to load products.");
        console.log(fetchError);
      } finally {
        if (isActive) {
          setLoading(false);
        }
      }
    };

    fetchProducts();

    return () => {
      isActive = false;
    };
  }, [searchQuery, currentUser?.id]);

  if (loading) {
    return (
      <div className="dashboard">
        <section className="products-section">
          <h2>Loading products...</h2>
        </section>
      </div>
    );
  }

  return (
    <div className="dashboard">
      {!searchQuery && <RecommendedProducts />}

      <section className="products-section">
        <h2>
          {searchQuery
            ? `Search Results for "${searchQuery}"`
            : "Trending Fashion"}
        </h2>

        <div className="product-grid">
          {error ? (
            <div className="empty-search">
              <h2>{error}</h2>
              <p>Please try again.</p>
            </div>
          ) : products.length > 0 ? (
            products.map((product) => (
              <Link
                key={product.article_id}
                to={`/product/${product.article_id}`}
                className="product-link"
              >
                <div className="product-card">
                  <img
                    src={product.image_url}
                    alt={product.product_name}
                    onError={(e) => {
                      e.currentTarget.src = FALLBACK_IMAGE;
                    }}
                  />

                  <h3>{product.product_name}</h3>
                  <p>₹{product.price}</p>
                </div>
              </Link>
            ))
          ) : (
            <div className="empty-search">
              <h2>No Products Found</h2>
              <p>Try another search.</p>
            </div>
          )}
        </div>
      </section>
    </div>
  );
}

export default Dashboard;
