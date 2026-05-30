import "./Login.css";
import {
  Link,
  useNavigate
} from "react-router-dom";

import {
  useState
} from "react";

import AUTH_API from "../../api/authApi";

function Login() {

  const navigate =
    useNavigate();

  const [
    formData,
    setFormData
  ] = useState({

    email: "",
    password: ""

  });

  const [
    message,
    setMessage
  ] = useState("");


  const handleChange =
    (e) => {

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

            "/login",

            formData
          );


        if (

          response.data.status
          === "success"

        ) {

          // Store token
          localStorage.setItem(

            "token",

            response.data.token
          );


          // Store full user
          localStorage.setItem(

            "user",

            JSON.stringify(

              response.data.user

            )
          );


          // Store the app user id for recommendations and history
          localStorage.setItem(
            "user_id",
            response.data.user.id
          );


          setMessage(
            "Login successful"
          );


          setTimeout(() => {

            navigate("/");

          }, 1000);

        }

        else {

          setMessage(

            response.data.message
          );
        }

      }

      catch (error) {

        console.log(
          error
        );

        setMessage(
          "Something went wrong"
        );
      }
    };


  return (

    <div className="login-page">

      <div className="login-container">

        <Link
          to="/"
          className="back-home"
        >

          ← Back to Home

        </Link>

        <h1>
          Login
        </h1>


        <form

          className="login-form"

          onSubmit={
            handleSubmit
          }
        >

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

            Login

          </button>

        </form>


        {message && (

          <p>
            {message}
          </p>

        )}


        <p>

          Don’t have an account?

          <Link to="/register">

            Register

          </Link>

        </p>

      </div>

    </div>
  );
}

export default Login;