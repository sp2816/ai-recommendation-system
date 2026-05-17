import { Link } from "react-router-dom";
import "./Header.css";

function Header() {
  return (
    <header className="header">
      <div className="header-inner">
        <div className="logo">H&M Recommender</div>

        <nav className="nav-links">
          <Link to="/">Home</Link>
          <Link to="/wishlist">Wishlist</Link>
          <Link to="/history">History</Link>
          <Link to="/profile">Profile</Link>
          <Link to="/login">Login</Link>
        </nav>
      </div>
    </header>
  );
}

export default Header;
