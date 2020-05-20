import { useState } from "react";

const useSimpleAuth = () => {
  const [loggedIn, setIsLoggedIn] = useState(false);

  const isAuthenticated = () =>
    loggedIn || localStorage.getItem("kennywood_token") !== null;

  const register = async (userInfo) => {
    const res = await fetch("http://127.0.0.1:8000/register/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify(userInfo),
    });
    const res_1 = await res.json();
    if ("token" in res_1) {
      localStorage.setItem("kennywood_token", res_1.token);
      setIsLoggedIn(true);
    }
  };

  const login = async (credentials) => {
    const res = await fetch("http://127.0.0.1:8000/login/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify(credentials),
    });
    const res_1 = await res.json();
    if ("valid" in res_1 && res_1.valid && "token" in res_1) {
      localStorage.setItem("kennywood_token", res_1.token);
      setIsLoggedIn(true);
    }
  };

  const logout = () => {
    setIsLoggedIn(false);
    localStorage.removeItem("kennywood_token");
  };

  return { isAuthenticated, logout, login, register };
};

export default useSimpleAuth;
