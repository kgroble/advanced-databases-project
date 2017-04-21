
/*
   Imports
*/

import React from 'react';
import * as axios from 'axios';


/*
   Code
*/

export default class LoginForm extends React.Component {


  constructor(props) {
    super(props);

    this.state = {
      usernameStarted: false,
      username: ''
    }
  }


  usernameChanged(event) {
    this.setState({usernameStarted: true});
    this.setState({username: event.target.value});
  }


  isValidUsername(uname) {
    return /^\w+$/.test(uname);
  }


  createUserRequest(data) {
    let username = this.state.username;
    let loc = '/users/'

    if (!this.isValidUsername(username)) {
      alert('bad username');
      return;
    }

    axios.post(loc, {
      username: this.state.username
    }).then(resp => {
      console.log('Created user');
    });
  }


  render() {
    let invalidUsername;

    if (!this.isValidUsername(this.state.username) && this.state.usernameStarted) {
      invalidUsername = <label>Invalid username.</label>
    }

    return (
      <form>

        {/* Entering username */}
        <label htmlFor="username-input">Username:</label>
        <input id="username-input"
               type="text"
               value={this.state.username}
               onChange={this.usernameChanged.bind(this)}/>
        {invalidUsername}

        <p>This is changing, right?</p>

        <p>{this.state.username}</p>

        {/* End of form */}
        <button type="button" onClick={this.createUserRequest.bind(this)}>
          Create profile
        </button>
      </form>
    );
  }
}
