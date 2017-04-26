

// React nonsense
import React from 'react';
import { Router
       , Route
       , Redirect
       , Switch } from 'react-router';
import { BrowserRouter } from 'react-router-dom';

// My components
import Login        from './Login/Login.jsx';
import Home         from './Home/Home.jsx';
import Dashboard    from './Dashboard/Dashboard.jsx';
import Header       from './Header/Header.jsx';
import PageNotFound from './PageNotFound/PageNotFound.jsx';


/*
   Code
*/

export default class App extends React.Component {
    render() {
        return (
          <div>
            <Header/>
            <BrowserRouter>
              <Switch>
                <Route exact path="/" component={Home} />
                <Route exact path="/login" component={Login} />
                <Route exact path="/home/:username" component={Dashboard} />
                <Route exact path="*" component={PageNotFound} />
              </Switch>
            </BrowserRouter>
          </div>
        );
    }
}
