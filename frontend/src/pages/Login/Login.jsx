import "./Login.css";
import { Link } from "react-router-dom";

function Login() {
  return (
    <div className="login-page">

      <div className="login-container">

        <Link
          to="/"
          className="back-home"
        >
          ← Back to Home
        </Link>

        <h1>Login</h1>

        <form className="login-form">

          <input
            type="email"
            placeholder="Enter email"
          />

          <input
            type="password"
            placeholder="Enter password"
          />

          <button type="submit">
            Login
          </button>

        </form>

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