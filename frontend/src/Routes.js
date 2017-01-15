import React, {Component} from 'react';
import App from './App';
import {Router, Route, Link, IndexRoute, IndexRedirect, hashHistory, browserHistory} from 'react-router'
import Login from './pages/Login'
import BasePage from './pages/BasePage'
import Home from './pages/Home'
const NotFound = () => (
  <h1>404.. This page is not found!</h1>)
export default class Routes extends Component {

  render() {
    return <Router history={hashHistory}>
      <Route path="/" component={App}>
        <IndexRedirect to="login"/>
        <Route path='/app' component={BasePage}>
          <IndexRoute component={Home}/>
          <Route path='/' component={NotFound}/>
        </Route>
        <Route path='/login' component={Login}/>
      </Route>
    </Router>
  }

}