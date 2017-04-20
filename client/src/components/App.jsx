

/*
   Imports
*/

// libraries
import React from 'react';
import { Router
       , Switch } from 'react-router';
import { BrowserRouter
       , Route } from 'react-router-dom'

// other components
import Login from './Login/Login.jsx'
import Home from './Home/Home.jsx'

// css


/*
   Code
*/

export default class App extends React.Component {
    render() {
        return (
          <BrowserRouter>
            <div>
              <Route path="/" component={Home} />
              <Route path="/login" component={Login} />
            </div>
          </BrowserRouter>
        );
    }
}
