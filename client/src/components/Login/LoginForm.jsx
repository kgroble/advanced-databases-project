
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
      username: '',
      errorMsg: false
    }
  }


  usernameChanged(event) {
    this.setState({usernameStarted: true});
    this.setState({username: event.target.value});
    this.setState({errorMsg: false});
  }


  isValidUsername(uname) {
    return /^\w+$/.test(uname);
  }


  createUserRequest(data) {
    let username = this.state.username;
    let loc = '/user/'

    if (!this.isValidUsername(username)) {
      alert('bad username');
      return;
    }

    axios.post(loc, {
      username: this.state.username
    }).then(resp => {
      let uname = resp.data.uname;
      location.replace('/home/'+uname+'/');
    }, err => {
      this.setState({
        errorMsg: true
      });
    });
  }


  login() {
    let username = this.state.username;
  }


  render() {
    let invalidUsername;
    let errorMessage;
    let username = this.state.username;

    if (!this.isValidUsername(this.state.username) && this.state.usernameStarted) {
      invalidUsername = <label>Invalid username.</label>
    }

    if (this.state.errorMsg != false) {
      errorMessage = <p>User already exists.</p>;
    }

    let isDisabled = !this.isValidUsername(username) ? 'disabled' : '';

    return (
      <form>

        {/* Entering username */}
        <label htmlFor="username-input">Username:</label>
        <input id="username-input"
               type="text"
               value={this.state.username}
               onChange={this.usernameChanged.bind(this)}/>

        <div>
          {invalidUsername}
          {errorMessage}
        </div>

        {/* End of form */}
        <button type="button"
                onClick={this.createUserRequest.bind(this)}
                disabled={!this.isValidUsername(username)} >
          Create profile
        </button>
        <button type="button"
                onClick={this.login.bind(this)}
                disabled={!this.isValidUsername(username)} >
          Login
        </button>
      </form>
    );
  }
}
