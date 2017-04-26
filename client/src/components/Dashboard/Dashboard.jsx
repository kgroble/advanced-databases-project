
import React from 'react';
import { NavLink } from 'react-router-dom';
import { Redirect } from 'react-router';
import * as axios from 'axios';

import { isAuthenticated } from '../auth.js';
import AdminDashboard from './AdminDashboard.jsx';


export default class Dashboard extends React.Component {
  constructor(props) {
    super(props);

    let user = /\/home\/(.*?)\/?$/.exec(this.props.location.pathname)[1];
    this.state = {
      username: user,
      usernameExists: true
    };

    axios.get('/user/' + user, {})
         .then(resp => {
           let users = resp.data;
           console.log(users);
           this.setState({
             users: users
           });
         }, uhoh => {

           this.setState({
             usernameExists: false
           });
         });
  };

  render() {
    let user = this.state.username;

    return !isAuthenticated() || !this.state.usernameExists ? (
      <Redirect to='/login' />
    ) : (
      <div>
        <h1>Welcome, {user}!</h1>
        <AdminDashboard />
      </div>
    );
  }
}
