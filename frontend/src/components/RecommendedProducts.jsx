import {
  useEffect,
  useState
} from "react";

import {
  Link,
  useLocation
} from "react-router-dom";

import API from "../api/productApi";

import {
  getRecommendations
} from "../services/recommendationService";

import {
  getLoggedInUser,
  rankAnonymousProducts,
  buildAnonymousProfile
} from "../services/recommendationContext";

function RecommendedProducts() {

  const location = useLocation();

  const fallbackImage =
    "data:image/svg+xml;charset=UTF-8," +
    encodeURIComponent(
      '<svg xmlns="http://www.w3.org/2000/svg" width="300" height="400" viewBox="0 0 300 400"><rect width="300" height="400" fill="#f3f4f6"/><text x="150" y="190" text-anchor="middle" font-family="Arial, sans-serif" font-size="20" fill="#6b7280">No Image</text><text x="150" y="220" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" fill="#9ca3af">Available</text></svg>'
    );

  const [
    recommendations,
    setRecommendations
  ] = useState([]);

  const [
    loading,
    setLoading
  ] = useState(true);

  const [
    error,
    setError
  ] = useState("");

  useEffect(() => {

    let isActive = true;

    const fetchRecommendations =
      async () => {

        if (!isActive) {
          return;
        }

        setLoading(true);
        setError("");

        try {

          const currentUser =
            getLoggedInUser();

          // ==========================
          // LOGGED IN USER
          // ==========================
          if (currentUser?.id) {

            const data =
              await getRecommendations(
                currentUser.id
              );

            if (!isActive) {
              return;
            }

            if (
              data &&
              Array.isArray(
                data.recommendations
              )
            ) {

              setRecommendations(
                data.recommendations
              );

              setError("");

            } else {

              const trendingResponse =
                await API.get(
                  "/products/trending"
                );

              if (!isActive) {
                return;
              }

              setRecommendations(
                trendingResponse.data.products || []
              );

              setError("");
            }

          }

          // ==========================
          // ANONYMOUS USER
          // ==========================
          else {

            const profile =
              buildAnonymousProfile();

            const response =
              await API.get(
                `/products?limit=200&category=${encodeURIComponent(
                  profile.favorite_product_type
                )}`
              );

            if (!isActive) {
              return;
            }

            const ranked =
              rankAnonymousProducts(
                response.data.products || []
              ).slice(0, 10);

            if (ranked.length > 0) {

              setRecommendations(
                ranked
              );

              setError("");

            } else {

              const trendingResponse =
                await API.get(
                  "/products/trending"
                );

              if (!isActive) {
                return;
              }

              setRecommendations(
                trendingResponse.data.products || []
              );

              setError("");
            }
          }

        } catch (fetchError) {

          if (!isActive) {
            return;
          }

          console.log(fetchError);

          setRecommendations([]);
          setError(
            "Failed to load recommendations."
          );

        } finally {

          if (isActive) {
            setLoading(false);
          }
        }
      };

    fetchRecommendations();

    return () => {
      isActive = false;
    };

  }, [
    location.pathname,
    location.search
  ]);

  if (loading) {
    return (
      <h2>
        Loading recommendations...
      </h2>
    );
  }

  return (

    <section className="recommendations-section">

      <div className="recommendations-header">

        <div>

          <p className="recommendations-eyebrow">
            AI Selected
          </p>

          <h2>
            Recommended For You
          </h2>

          <p className="recommendations-copy">
            Fresh picks based on your browsing and purchase signals.
          </p>

        </div>

        {recommendations.length > 0 && (

          <span className="recommendations-pill">

            {recommendations.length}
            {" "}
            products

          </span>

        )}

      </div>

      <div className="recommendations-grid">

        {error ? (

          <p className="recommendations-empty">
            {error}
          </p>

        ) : recommendations.length > 0 ? (

          recommendations.map((item) => (

            <Link
              key={item.article_id}
              to={`/product/${item.article_id}`}
              className="recommendation-link"
            >

              <div className="recommendation-card">

                <div className="recommendation-image-wrap">

                  <img
                    className="recommendation-image"
                    src={
                      item.image_url ||
                      `${import.meta.env.VITE_API_URL}/images/0${String(item.article_id).slice(0, 2)}/0${item.article_id}.jpg`
                    }
                    alt={
                      item.prod_name ||
                      item.product_name
                    }
                    onError={(e) => {
                      e.currentTarget.src =
                        fallbackImage;
                    }}
                  />

                </div>

                <div className="recommendation-body">

                  <span className="recommendation-chip">
                    {item.product_type_name}
                  </span>

                  <h3>
                    {
                      item.prod_name ||
                      item.product_name
                    }
                  </h3>

                  <p className="recommendation-colour">
                    {item.colour_group_name}
                  </p>

                  <p className="recommendation-id">
                    #{item.article_id}
                  </p>

                </div>

              </div>

            </Link>

          ))

        ) : (

          <p className="recommendations-empty">
            No recommendations found.
          </p>

        )}

      </div>

    </section>
  );
}

export default RecommendedProducts;