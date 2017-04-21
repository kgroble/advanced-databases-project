
import React from 'react';
import * as axios from 'axios';

export default class AdminDashboard extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      users: []
    }

    axios.get('/users/', {

    }).then(users => {
      this.setState({
        users: users
      });
    });

  }

  render() {
    return (
      <div>
        <div>
          <h3>All users</h3>
          {this.state.users}
        </div>
      </div>
    );
  }
}
