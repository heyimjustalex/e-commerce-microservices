import React, { useEffect, useState, useCallback } from "react";
import { jwtDecode } from "jwt-decode";

let logoutTimer;

export const AuthContext = React.createContext({
  email: "",
  accessToken: "",
  role: "",
  isAuthenticated: false,
  login: (accessToken) => {},
  logout: () => {},
});

const calculateRemainingTime = (expTime) => {
  const currentTime = new Date().getTime();
  const adjExpTime = new Date(new Date().getTime() + +expTime);
  const remainingDuration = adjExpTime - currentTime;
  return remainingDuration;
};

const retrieveStoredAccessToken = () => {
  const storedAccessToken = localStorage.getItem("accessToken");
  const storedExpirationDate = localStorage.getItem("exp");
  const role = localStorage.getItem("role");
  const email = localStorage.getItem("email");
  const remaningTime = calculateRemainingTime(storedExpirationDate);

  if (remaningTime <= 60000) {
    localStorage.removeItem("email");
    localStorage.removeItem("accessToken");
    localStorage.removeItem("role");
    localStorage.removeItem("exp");
    return null;
  }
  return {
    email: email,
    accessToken: storedAccessToken,
    duration: remaningTime,
    role: role,
  };
};

export const AuthContextProvider = (props) => {
  const AccessTokenData = retrieveStoredAccessToken();
  let initialAccessToken;
  let initialRole;
  let email;

  if (AccessTokenData) {
    initialAccessToken = AccessTokenData.accessToken;
    initialRole = AccessTokenData.role;
    email = AccessTokenData.email;
  }
  const [accessToken, setAccessToken] = useState(initialAccessToken);
  const [role, setRole] = useState(initialRole);

  const isAuthenticated = !!accessToken;

  const logoutHandler = useCallback(() => {
    setAccessToken(null);
    localStorage.removeItem("accessToken");
    localStorage.removeItem("exp");
    localStorage.removeItem("email");
    localStorage.removeItem("role");

    if (logoutTimer) {
      clearTimeout(logoutTimer);
    }
  }, []);

  const loginHandler = (accessToken) => {
    const decoded = jwtDecode(accessToken);
    const decodedEmail = decoded.email;
    const decodedRole = decoded.role;
    const decodedExp = decoded.exp;

    setAccessToken(accessToken);
    setRole(decoded.role);
    const remainingTime = calculateRemainingTime(decoded.exp);
    logoutTimer = setTimeout(logoutHandler, remainingTime);

    localStorage.setItem("email", decodedEmail);
    localStorage.setItem("role", decodedRole);
    localStorage.setItem("exp", decodedExp);
    localStorage.setItem("accessToken", accessToken);
  };

  useEffect(() => {
    if (AccessTokenData) {
      logoutTimer = setTimeout(logoutHandler, AccessTokenData.duration);
    }
  }, [AccessTokenData, logoutHandler]);

  const contextValue = {
    email: email,
    accessToken: accessToken,
    isAuthenticated: isAuthenticated,
    role: role,
    login: loginHandler,
    logout: logoutHandler,
  };
  return (
    <AuthContext.Provider value={contextValue}>
      {props.children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
