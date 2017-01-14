import React, {Component} from 'react';
import logo from './logo.svg';
import './App.css';
import { Router, Route, Link, IndexRoute, hashHistory, browserHistory } from 'react-router'

class App extends Component {
  fetchApi(){
    console.log("a");
    fetch("/api/")
      .then((response) => {
        console.log(response.json());
      })
  }
  render() {
    return (
      <Router history={hashHistory}>
        <Route path='/' component={Container}>
          <IndexRoute component={Home} />
          <Route path='/login' component={Login} />
          <Route path='*' component={NotFound} />
        </Route>
      </Router>
    )
  }
}
const Container = (props) => <div>
  <Nav />
  {props.children}
</div>
const Nav = () => (
  <div>
    <Link to='/'>Home</Link>&nbsp;
    <Link to='/login'>Login</Link>
  </div>
)
const Home = () => <h1>Hello from Home!</h1>
const Login = () => <h1>Login</h1>
const NotFound = () => (
  <h1>404.. This page is not found!</h1>)
export default App;
