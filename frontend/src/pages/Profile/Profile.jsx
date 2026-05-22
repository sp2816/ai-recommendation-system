import "./Profile.css";
import { useNavigate } from "react-router-dom";

function Profile() {

  const navigate =
    useNavigate();

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

      navigate("/login");
    };

  if (!user) {

    return (
      <div className="profile-page">

        <div className="profile-card">

          <h1>
            Please Login
          </h1>

        </div>

      </div>
    );
  }

  return (
    <div className="profile-page">

      <div className="profile-card">

        <div className="profile-avatar">

          {
            user.full_name
            ?.charAt(0)
            .toUpperCase()
          }

        </div>

        <h1>
          Welcome,
          {" "}
          {
            user.full_name
          }
        </h1>

        <div className="profile-info">

          <div className="profile-item">
            <span>
              Full Name
            </span>

            <p>
              {
                user.full_name
              }
            </p>
          </div>

          <div className="profile-item">
            <span>
              Email
            </span>

            <p>
              {
                user.email
              }
            </p>
          </div>

          <div className="profile-item">
            <span>
              Age
            </span>

            <p>
              {
                user.age
              }
            </p>
          </div>

        </div>

        <button
          className="profile-logout-btn"
          onClick={
            handleLogout
          }
        >
          Logout
        </button>

      </div>

    </div>
  );
}

export default Profile;