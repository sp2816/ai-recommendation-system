import "./Register.css";
import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";

import AUTH_API from "../../api/authApi";

function Register() {

  const navigate =
    useNavigate();

  const [formData, setFormData] =
    useState({
      full_name: "",
      email: "",
      age: "",
      password: ""
    });

  const [message, setMessage] =
    useState("");

  const handleChange = (e) => {

    setFormData({
      ...formData,
      [e.target.name]:
      e.target.value
    });
  };

  const handleSubmit =
    async (e) => {

      e.preventDefault();

      try {

        const response =
          await AUTH_API.post(
            "/register",
            formData
          );

        setMessage(
          response.data.message
        );

        if (
          response.data.status
          === "success"
        ) {

          setTimeout(() => {

            navigate("/login");

          }, 1500);
        }

      } catch (error) {

        console.log(error);

        setMessage(
          "Something went wrong"
        );
      }
    };

  return (
    <div className="register-page">

      <div className="register-container">

        <Link
          to="/"
          className="back-home"
        >
          ← Back to Home
        </Link>

        <h1>
          Register
        </h1>

        <form
          className="register-form"
          onSubmit={handleSubmit}
        >

          <input
            type="text"
            name="full_name"
            placeholder="Enter full name"
            value={
              formData.full_name
            }
            onChange={
              handleChange
            }
            required
          />

          <input
            type="email"
            name="email"
            placeholder="Enter email"
            value={
              formData.email
            }
            onChange={
              handleChange
            }
            required
          />

          <input
            type="number"
            name="age"
            placeholder="Enter age"
            value={
              formData.age
            }
            onChange={
              handleChange
            }
            required
          />

          <input
            type="password"
            name="password"
            placeholder="Enter password"
            value={
              formData.password
            }
            onChange={
              handleChange
            }
            required
          />

          <button
            type="submit"
          >
            Register
          </button>

        </form>

        {message && (
          <p>
            {message}
          </p>
        )}

        <p>
          Already have an account?

          <Link to="/login">
            Login
          </Link>
        </p>

      </div>
    </div>
  );
}

export default Register;