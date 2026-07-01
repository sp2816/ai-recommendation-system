import "./Wishlist.css";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import WISHLIST_API
from "../../api/wishlistApi";

const FALLBACK_IMAGE =
  "data:image/svg+xml;charset=UTF-8," +
  encodeURIComponent(
    '<svg xmlns="http://www.w3.org/2000/svg" width="300" height="400" viewBox="0 0 300 400"><rect width="300" height="400" fill="#f3f4f6"/><text x="150" y="190" text-anchor="middle" font-family="Arial, sans-serif" font-size="20" fill="#6b7280">No Image</text><text x="150" y="220" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" fill="#9ca3af">Available</text></svg>'
  );

function Wishlist() {

  const navigate =
    useNavigate();

  const [products,
    setProducts] =
    useState([]);

  useEffect(() => {

    fetchWishlist();

  }, []);

  const fetchWishlist =
    async () => {

      const user =
        JSON.parse(
          localStorage.getItem(
            "user"
          )
        );

      if (!user) return;

      try {

        const response =
          await WISHLIST_API.get(
            `/api/wishlist/${user.id}`
          );

        setProducts(
          response.data.products
        );

      } catch (error) {

        console.log(error);
      }
    };

  const handleRemove =
    async (
      e,
      articleId
    ) => {

      e.stopPropagation();

      const confirmDelete =
        window.confirm(
          "Remove from wishlist?"
        );

      if (
        !confirmDelete
      ) return;

      const user =
        JSON.parse(
          localStorage.getItem(
            "user"
          )
        );

      try {

        await WISHLIST_API.delete(
          "/api/wishlist/remove",
          {
            params: {
              user_id:
              user.id,

              article_id:
              articleId
            }
          }
        );

        fetchWishlist();

      } catch (error) {

        console.log(error);

        alert(
          "Failed to remove"
        );
      }
    };

  return (
    <div className="wishlist-page">

      <h1 className="wishlist-title">
        My Wishlist
      </h1>

      <div className="wishlist-grid">

        {products.map(
          (product) => (

          <div
            key={
              product.article_id
            }
            className="wishlist-card"

            onClick={() =>
              navigate(
                `/product/${
                  product.article_id
                }`
              )
            }
          >

            <img
              src={
                product.image_url
              }
              alt={
                product.product_name
              }
              onError={(e) => {
                e.currentTarget.src = FALLBACK_IMAGE;
              }}
            />

            <div className="wishlist-info">

              <h3>
                {
                  product.product_name
                }
              </h3>

              <p className="wishlist-price">
                ₹{
                  product.price
                }
              </p>

              <p className="wishlist-description">
                {
                  product.description
                }
              </p>

              <button
                className="remove-btn"

                onClick={(e) =>
                  handleRemove(
                    e,
                    product.article_id
                  )
                }
              >
                Remove
              </button>

            </div>

          </div>
        ))}

      </div>

    </div>
  );
}

export default Wishlist;