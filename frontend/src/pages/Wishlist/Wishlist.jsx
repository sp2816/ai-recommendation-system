import "./Wishlist.css";

function Wishlist() {
  return (
    <div className="wishlist-page">
      <div className="wishlist-header">
        <h1>My Wishlist</h1>
        <p>
          Your saved fashion items
          will appear here.
        </p>
      </div>

      <div className="wishlist-empty">
        <h2>No products saved yet</h2>
        <p>
          Start exploring and add
          products to wishlist.
        </p>
      </div>
    </div>
  );
}

export default Wishlist;