import "./History.css";

function History() {

  const historyItems = [];

  return (
    <div className="history-page">

      <div className="history-header">

        <h1>
          Recommendation History
        </h1>

        <p>
          Previously recommended
          fashion products based
          on your interests.
        </p>

      </div>

      {historyItems.length === 0 ? (

        <div className="history-empty">

          <div className="empty-icon">
            🛍️
          </div>

          <h2>
            No Recommendations Yet
          </h2>

          <p>
            Start exploring fashion
            products and AI
            recommendations will
            appear here.
          </p>

        </div>

      ) : (

        <div className="history-grid">

          {historyItems.map(
            (item) => (

            <div
              key={item.id}
              className="history-card"
            >
              Product
            </div>
          ))}

        </div>
      )}

    </div>
  );
}

export default History;