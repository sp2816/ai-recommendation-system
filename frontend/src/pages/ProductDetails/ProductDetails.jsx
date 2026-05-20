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

        setProduct(
          response.data.product
        );

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