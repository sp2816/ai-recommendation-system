import {
  BrowserRouter,
  Routes,
  Route,
  useLocation
} from "react-router-dom";

import Dashboard from "../pages/Dashboard/Dashboard";
import Login from "../pages/Login/Login";
import Register from "../pages/Register/Register";
import ProductDetails from "../pages/ProductDetails/ProductDetails";
import Wishlist from "../pages/Wishlist/Wishlist";
import Profile from "../pages/Profile/Profile";
import History from "../pages/History/History";
import NotFound from "../pages/NotFound/NotFound";

import Header from "../components/Header/Header";
import Footer from "../components/Footer/Footer";

function Layout() {
  const location = useLocation();

  const hideLayout =
    location.pathname === "/login" ||
    location.pathname === "/register";

  if (hideLayout) {
    document.body.classList.add("auth-page");
  } else {
    document.body.classList.remove("auth-page");
  }

  return (
    <>
      {!hideLayout && <Header />}

      <main>
        <Routes>
          <Route
            path="/"
            element={<Dashboard />}
          />

          <Route
            path="/login"
            element={<Login />}
          />

          <Route
            path="/register"
            element={<Register />}
          />

          <Route
            path="/product/:id"
            element={<ProductDetails />}
          />

          <Route
            path="/wishlist"
            element={<Wishlist />}
          />

          <Route
            path="/profile"
            element={<Profile />}
          />

          <Route
            path="/history"
            element={<History />}
          />

          <Route
            path="*"
            element={<NotFound />}
          />
        </Routes>
      </main>

      {!hideLayout && <Footer />}
    </>
  );
}

function AppRouter() {
  return (
    <BrowserRouter>
      <Layout />
    </BrowserRouter>
  );
}

export default AppRouter;