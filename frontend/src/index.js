import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import './index.css';
import {createStore, compose} from 'redux'
import reducer from './reducers'
import {Provider} from 'react-redux';
import {Router, Route, Link, IndexRoute, IndexRedirect, hashHistory, browserHistory} from 'react-router'

import Login from './routes/Login'
import BasePage from './routes/BasePage'

// Don't do this! You’re bringing DevTools into the production bundle.
import DevTools from './DevTools';
const initialState = {user: null, apps: null};
const enhancer = compose(
  // Required! Enable Redux DevTools with the monitors you chose
  DevTools.instrument()
);
const store = createStore(reducer, initialState, enhancer);

const Home = () => <h1>Hello from Home!</h1>
const NotFound = () => (
  <h1>404.. This page is not found!</h1>)
ReactDOM.render(
  <Provider store={store}>
    <div id="container">
      <Router history={hashHistory}>
        <Route path="/" component={App}>
          <IndexRedirect to="login"/>
          <Route path='/app' component={BasePage}>
            <IndexRoute component={Home}/>
            <Route path='/' component={NotFound}/>
          </Route>
          <Route path='/login' component={Login}/>
        </Route>
      </Router>
      <DevTools />
    </div>
  </Provider>,
  document.getElementById('root')
);
