

/*
   Imports
*/

// libraries
import React from 'react';
import { Router
       , Route
       , Switch } from 'react-router';
import { BrowserRouter } from 'react-router-dom'

// other components
import Login from './Login/Login.jsx'
import Home from './Home/Home.jsx'
import Dashboard from './Dashboard/Dashboard.jsx'

// css


/*
   Code
*/

export default class App extends React.Component {
    render() {
        return (
          <BrowserRouter>
            <div>
              <Route exact path="/" component={Home} />
              <Route exact path="/login" component={Login} />
              <Route exact path="/home/:username" component={Dashboard} />
            </div>
          </BrowserRouter>
        );
    }
}
