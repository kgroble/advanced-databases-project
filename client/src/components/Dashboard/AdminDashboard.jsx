
import React from 'react';
import * as axios from 'axios';

export default class AdminDashboard extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      users: []
    }

    this.refreshUsers();
  }


  refreshUsers() {
    axios.get('/users/', {
      params: {
        username: 'jcolemang'
      }
    }).then(resp => {
      let users = resp.data;
      console.log(users);
      this.setState({
        users: users
      });
    });
  }


  render() {

    let userHtml = this.state.users.map(x => {
      return (
        <p key={x._id}>{x.uname}</p>
      )
    });

    return (
      <div>
        <div>
          <h3>All users</h3>
          {userHtml}
        </div>
      </div>
    );
  }
}
