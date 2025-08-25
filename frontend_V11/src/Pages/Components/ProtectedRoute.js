import React, { useEffect, useState } from 'react';
import { Route, Redirect } from 'react-router-dom';
import axios from 'axios';
import Loading from '../Loading';

const ProtectedRoute = ({ component: Component, ...rest }) => {
  const API_BASE_URL = process.env.REACT_APP_BASE_URL;
  const [isAuth, setIsAuth] = useState(null); // null = loading, false = not auth, true = auth

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/user/me`, {
          withCredentials: true, 
        });

        // Check if userName exists in response
        if (response.status === 200 && response.data?.userName?.username) {
          setIsAuth(true);
        } else {
          setIsAuth(false);
        }
      } catch (error) {
        setIsAuth(false);
      }
    };

    checkAuth();
  }, []);

  if (isAuth === null) return <Loading />;

  return (
    <Route
      {...rest}
      render={(props) =>
        isAuth ? <Component {...props} /> : <Redirect to="/Login" />
      }
    />
  );
};

export default ProtectedRoute;
