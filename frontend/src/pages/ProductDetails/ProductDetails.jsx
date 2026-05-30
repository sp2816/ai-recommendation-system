import "./ProductDetails.css";
import { useParams } from "react-router-dom";
import {
  useEffect,
  useState
} from "react";

import API
from "../../api/productApi";

import WISHLIST_API
from "../../api/wishlistApi";

import {
  getLoggedInUser,
  saveAnonymousView
} from "../../services/recommendationContext";

const FALLBACK_IMAGE =
  "data:image/svg+xml;charset=UTF-8," +
  encodeURIComponent(
    '<svg xmlns="http://www.w3.org/2000/svg" width="300" height="400" viewBox="0 0 300 400"><rect width="300" height="400" fill="#f3f4f6"/><text x="150" y="190" text-anchor="middle" font-family="Arial, sans-serif" font-size="20" fill="#6b7280">No Image</text><text x="150" y="220" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" fill="#9ca3af">Available</text></svg>'
  );

function ProductDetails() {

  const { id } =
    useParams();

  const [product,
    setProduct] =
    useState(null);

  useEffect(() => {
    fetchProduct();
  }, [id]);

  const fetchProduct =
    async () => {

      try {

        const response =
          await API.get(
            `/product/${id}`
          );

        const fetchedProduct =
          response.data.product;

        setProduct(
          fetchedProduct
        );

        const user = getLoggedInUser();

        if (user) {
          try {
            await API.post(
              "/api/views/save",
              {
                user_id: user.id,
                article_id: fetchedProduct.article_id
              }
            );
          } catch (error) {
            console.log(error);
          }
        } else {
          saveAnonymousView(fetchedProduct);
        }

      } catch (error) {

        console.log(error);
      }
    };

  const handleWishlist =
    async () => {

      const user =
        JSON.parse(
          localStorage.getItem(
            "user"
          )
        );

      if (!user) {

        alert(
          "Please login first"
        );

        return;
      }

      try {

        const response =
          await WISHLIST_API.post(
            "/wishlist/add",
            {
              user_id:
              user.id,

              article_id:
              product.article_id
            }
          );

        alert(
          response.data.message
        );

      } catch (error) {

        console.log(error);

        alert(
          "Failed to add wishlist"
        );
      }
    };

  if (!product) {

    return (
      <h1>
        Loading Product...
      </h1>
    );
  }

  return (
    <div className="product-details">

      <div className="details-card">

        <div className="details-image">

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

        </div>

        <div className="details-info">

          <h1>
            {
              product.product_name
            }
          </h1>

          <h2>
            ₹{
              product.price
            }
          </h2>

          <div className="product-meta">

            <p>
              <strong>
                Type:
              </strong>
              {" "}
              {
                product
                .product_type_name
              }
            </p>

            <p>
              <strong>
                Category:
              </strong>
              {" "}
              {
                product
                .product_group_name
              }
            </p>

            <p>
              <strong>
                Colour:
              </strong>
              {" "}
              {
                product
                .colour_group_name
              }
            </p>

          </div>

          <div className="description-box">

            <h3>
              Description
            </h3>

            <p>
              {
                product
                .description
              }
            </p>

          </div>

          <button
            onClick={
              handleWishlist
            }
          >
            Add to Wishlist
          </button>

        </div>

      </div>

    </div>
  );
}

export default ProductDetails;  