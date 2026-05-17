import "./ProductDetails.css";
import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";

import API from "../../api/productApi";

function ProductDetails() {

  const { id } = useParams();

  const [product, setProduct] =
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

        <img
          src={product.image_url}
          alt={
            product.product_name
          }
        />

        <div className="details-info">

          <h1>
            {
              product.product_name
            }
          </h1>

          <h2>
            ₹{product.price}
          </h2>

          <p>
            {
              product.description
            }
          </p>

          <button>
            Add to Wishlist
          </button>

        </div>

      </div>

    </div>
  );
}

export default ProductDetails;