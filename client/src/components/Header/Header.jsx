
import React from 'react';

import { NavLink } from 'react-router-dom';

export default class Header extends React.Component {
  constructor(props) {
    super(props);
    this.state = {

    }
  }

  render() {
    return (
      <nav>
        <ul>
          <li>
            Welcome
          </li>
          <li>
            {/* <NavLink to="/home">
                <button>
                Home
                </button>
                </NavLink> */}
          </li>
        </ul>
      </nav>
    );
  }
}
