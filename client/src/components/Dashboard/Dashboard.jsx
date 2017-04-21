
import React from 'react';

import { NavLink } from 'react-router-dom';
import AdminDashboard from './AdminDashboard.jsx';

export default class Dashboard extends React.Component {
  constructor(props) {
    super(props);
    this.state = {

    }
  }

  render() {
    let user = /\/home\/(.*?)\/?$/.exec(this.props.location.pathname)[1];

    return (
      <div>
        <h1>Welcome, {user}!</h1>
        <AdminDashboard />
      </div>
    );
  }
}
