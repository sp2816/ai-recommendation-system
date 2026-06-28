import "./Header.css";
import { Link, NavLink, useNavigate } from "react-router-dom";
import { useState } from "react";
import axios from "axios";
import API from "../../api/productApi";

import {
  saveAnonymousSearch,
  getLoggedInUser
} from "../../services/recommendationContext";

function Header() {

  const navigate = useNavigate();

  const [search, setSearch] = useState("");

  const user = getLoggedInUser();

  const handleLogout = () => {

    localStorage.removeItem("token");
    localStorage.removeItem("user");
    localStorage.removeItem("user_id");

    navigate("/login");
  };

  const handleSearch = async (e) => {

    e.preventDefault();

    if (!search.trim()) {

      navigate("/dashboard");
      return;
    }

    const currentUser = getLoggedInUser();

    try {

      if (currentUser) {

        await axios.post(
          "/search/save",
          {
            user_id: currentUser.id,
            search_query: search
          }
        );

      } else {

        saveAnonymousSearch(search);
      }

    } catch (error) {

      console.log(error);
    }

    navigate(`/dashboard?search=${encodeURIComponent(search)}`);
  };

  return (
    <header className="header">

      <div className="header-inner">

        <div className="logo">
          H&M Recommender
        </div>

        <form
          className="search-form"
          onSubmit={handleSearch}
        >

          <input
            type="text"
            placeholder="Search products..."
            value={search}
            onChange={(e) =>
              setSearch(e.target.value)
            }
          />

          <button type="submit">
            Search
          </button>

        </form>

        <nav className="nav-links">

          <NavLink to="/dashboard">
            Home
          </NavLink>

          <NavLink to="/wishlist">
            Wishlist
          </NavLink>

          <NavLink to="/history">
            History
          </NavLink>

          <NavLink to="/profile">
            Profile
          </NavLink>

          {user ? (
            <>
              <span className="welcome-user">

                Welcome, {user.full_name}!

              </span>

              <button
                className="logout-btn"
                onClick={handleLogout}
              >
                Logout
              </button>
            </>
          ) : (
            <Link to="/login">
              Login
            </Link>
          )}

        </nav>

      </div>

    </header>
  );
}

export default Header;