
import React from 'react';
import { NavLink } from 'react-router-dom';
import { Redirect } from 'react-router';

import { isAuthenticated } from '../auth';

export default class Home extends React.Component {

  authenticate() {

  }


  render() {
    return !isAuthenticated() ? (
      <Redirect to='/login' />
    ) : (
      <div>
        <h1>Welcome to our website</h1>
        <NavLink to="/login">
          <button type="button">
            Log in
          </button>
        </NavLink>
      </div>
    );
  }
}
