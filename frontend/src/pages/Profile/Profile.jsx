import "./Profile.css";

function Profile() {
  return (
    <div className="profile-page">

      <div className="profile-card">

        <div className="profile-top">
          <div className="profile-avatar">
            S
          </div>

          <div>
            <h1>Selin Parmar</h1>
            <p>
              Fashion Explorer
            </p>
          </div>
        </div>

        <div className="profile-info">

          <div className="info-box">
            <h3>Email</h3>
            <p>
              selin@example.com
            </p>
          </div>

          <div className="info-box">
            <h3>Age</h3>
            <p>20</p>
          </div>

          <div className="info-box">
            <h3>Preferred Style</h3>
            <p>
              Casual & Streetwear
            </p>
          </div>

        </div>

      </div>

    </div>
  );
}

export default Profile;