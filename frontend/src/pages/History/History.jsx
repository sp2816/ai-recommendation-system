import "./History.css";

function History() {
  return (
    <div className="history-page">

      <div className="history-header">
        <h1>Recommendation History</h1>

        <p>
          Track your viewed and
          recommended products.
        </p>
      </div>

      <div className="history-empty">
        <h2>No activity yet</h2>

        <p>
          Your recommendation
          history will appear here.
        </p>
      </div>

    </div>
  );
}

export default History;