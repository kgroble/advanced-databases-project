
/*
   Imports
*/

import React from 'react';

export default class LoginForm extends React.Component {


  constructor(props) {
    super(props);

    console.log('Constructor called');

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
    return /^\w+$/.test(uname) || !this.state.usernameStarted;
  }



  render() {

    let invalidUsername;

    if (!this.isValidUsername(this.state.username)) {
      invalidUsername = <label>Invalid username.</label>
    }

    return (
      <form>

        <label htmlFor="username-input">Username:</label>
        <input id="username-input"
               type="text"
               value={this.state.username}
               onChange={this.usernameChanged.bind(this)}/>
        {invalidUsername}

        <p>{this.state.username}</p>

        <button type="button">Create profile</button>
      </form>
    );
  }


}
