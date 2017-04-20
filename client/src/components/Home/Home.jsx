
import React from 'react';

import { NavLink } from 'react-router-dom';

export default class Home extends React.Component {
  render() {
    return (
      <div>
        <h1>Welcome to our website</h1>
        <NavLink to="/login">
          <button type="button">
            Uhhhhhhhhhhhh
          </button>
        </NavLink>
      </div>
    )
  }
}
