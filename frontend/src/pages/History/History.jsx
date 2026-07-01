import "./History.css";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import API from "../../api/productApi";

import { getLoggedInUser } from "../../services/recommendationContext";

const FALLBACK_IMAGE =
  "data:image/svg+xml;charset=UTF-8," +
  encodeURIComponent(
    '<svg xmlns="http://www.w3.org/2000/svg" width="300" height="400" viewBox="0 0 300 400"><rect width="300" height="400" fill="#f3f4f6"/><text x="150" y="190" text-anchor="middle" font-family="Arial, sans-serif" font-size="20" fill="#6b7280">No Image</text><text x="150" y="220" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" fill="#9ca3af">Available</text></svg>'
  );

function History() {

  const user = getLoggedInUser();

  const [historyItems, setHistoryItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {

    const fetchHistory = async () => {

      if (!user?.id) {
        setLoading(false);
        return;
      }

      try {

        const response = await API.get(
          `/api/history/recommendations/${user.id}`
        );

        setHistoryItems(
          response.data.products || []
        );

        setError("");

      } catch (err) {

        console.log(err);

        setError(
          "Unable to load recommendation history right now."
        );

        setHistoryItems([]);

      } finally {

        setLoading(false);
      }
    };

    fetchHistory();

  }, [user?.id]);

  if (!user) {

    return (
      <div className="history-page">

        <div className="history-header">

          <h1>
            Recommendation History
          </h1>

          <p>
            Log in to view the recommendations shown to your account.
          </p>

        </div>

        <div className="history-empty">

          <div className="empty-icon">
            🔐
          </div>

          <h2>
            Login Required
          </h2>

          <p>
            Please log in to see your personal recommendation history.
          </p>

          <Link
            className="history-login-btn"
            to="/login"
          >
            Go to Login
          </Link>

        </div>

      </div>
    );
  }

  if (loading) {

    return (
      <div className="history-page">

        <div className="history-empty">
          <h2>Loading history...</h2>
        </div>

      </div>
    );
  }

  return (

    <div className="history-page">

      <div className="history-header">

        <h1>
          Recommendation History
        </h1>

        <p>
          Previously recommended fashion products based on your interests.
        </p>

      </div>

      {error ? (

        <div className="history-empty">
          <h2>{error}</h2>
        </div>

      ) : historyItems.length === 0 ? (

        <div className="history-empty">

          <div className="empty-icon">
            🛍️
          </div>

          <h2>
            No Recommendations Yet
          </h2>

          <p>
            Start exploring fashion products and AI recommendations will appear here.
          </p>

        </div>

      ) : (

        <div className="history-grid">

          {historyItems.map((item) => (

            <Link
              key={`${item.article_id}-${item.created_at}`}
              to={`/product/${item.article_id}`}
              className="history-link"
            >

              <div className="history-card">

                {/* <img
                  // src={item.image_url}
                  alt={item.product_name}
                  // onError={(e) => {
                  //   e.currentTarget.src = FALLBACK_IMAGE;
                  // }}
                /> */}

                <div className="history-card-body">

                  <span className="history-chip">
                    {item.product_type_name}
                  </span>

                  <h3>
                    {item.product_name}
                  </h3>

                  <p>
                    {item.colour_group_name}
                  </p>

                  <small>
                    {new Date(item.created_at).toLocaleString()}
                  </small>

                </div>

              </div>

            </Link>

          ))}

        </div>

      )}

    </div>
  );
}

export default History;