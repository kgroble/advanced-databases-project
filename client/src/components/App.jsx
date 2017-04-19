

/*
   Imports
*/

// libraries
import React from 'react';

// other components
import LoginForm from './Login/LoginForm.jsx'

// css


/*
   Code
*/

export default class App extends React.Component {
    render() {
        return (
            <div>
                <h1>Dating for Nerds</h1>

                <LoginForm>
                </LoginForm>
            </div>
        );
    }
}
