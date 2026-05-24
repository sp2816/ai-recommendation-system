import "./Header.css";
import { Link, NavLink, useNavigate } from "react-router-dom";
import { useState } from "react";
import axios from "axios";

function Header() {

  const navigate =
    useNavigate();

  const [search,
    setSearch] =
    useState("");

  const user =
    JSON.parse(
      localStorage.getItem(
        "user"
      )
    );

  const handleLogout =
    () => {

      localStorage.removeItem(
        "token"
      );

      localStorage.removeItem(
        "user"
      );

      window.location.reload();
    };

  const handleSearch =
  async (e) => {

    e.preventDefault();

    if (
      !search.trim()
    ) {

      navigate("/");

      return;
    }

    const user =
      JSON.parse(
        localStorage.getItem(
          "user"
        )
      );

    try {

      if (user) {

        await axios.post(
          "http://127.0.0.1:8000/api/search/save",
          {
            user_id:
            user.id,

            search_query:
            search
          }
        );
      }

    } catch (error) {

      console.log(error);
    }

    navigate(
      `/?search=${search}`
    );
  };

  return (
    <header className="header">

      <div className="header-inner">

        <div className="logo">
          H&M Recommender
        </div>

        <form
          className="search-form"
          onSubmit={
            handleSearch
          }
        >

          <input
            type="text"
            placeholder="Search products..."

            value={search}

            onChange={(e) =>
              setSearch(
                e.target.value
              )
            }
          />

          <button
            type="submit"
          >
            Search
          </button>

        </form>

        <nav className="nav-links">

          <NavLink to="/">
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

                Welcome,
                {" "}
                {
                  user.full_name
                }!

              </span>

              <button
                className="logout-btn"

                onClick={
                  handleLogout
                }
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