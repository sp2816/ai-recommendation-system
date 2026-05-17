import "./Register.css";
import { Link } from "react-router-dom";

function Register() {
  return (
    <div className="register-page">

      <div className="register-container">

        <Link
          to="/"
          className="back-home"
        >
          ← Back to Home
        </Link>

        <h1>Register</h1>

        <form className="register-form">

          <input
            type="text"
            placeholder="Enter full name"
          />

          <input
            type="email"
            placeholder="Enter email"
          />

          <input
            type="number"
            placeholder="Enter age"
          />

          <input
            type="password"
            placeholder="Enter password"
          />

          <button type="submit">
            Register
          </button>

        </form>

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