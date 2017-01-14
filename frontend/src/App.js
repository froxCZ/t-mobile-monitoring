import React, {Component} from 'react';
import logo from './logo.svg';
import './App.css';
import MyNavigation from './components/MyNavigation'
import {Router, Route, Link, IndexRoute, hashHistory, browserHistory} from 'react-router'


class App extends Component {
  fetchApi() {
    console.log("a");
    fetch("/api/")
      .then((response) => {
        console.log(response.json());
      })
  }

  render() {
    return (
      <Router history={hashHistory}>
        <Route path='/' component={ForwardingRoute}>
          <Route path='/app' component={Container}>
            <IndexRoute component={Home}/>
            <Route path='*' component={NotFound}/>
          </Route>
        </Route>
        <Route path='/login' component={Login}/>

      </Router>
    )
  }
}

class ForwardingRoute extends Component {

  constructor() {
    super();
    this.state = {user: null};
  }

  componentWillMount() {
    const router = this.props.router;
    router.push('/app');
  }

  login() {
    this.setState({user: {name: "a"}});
  }

  render() {
    if (this.props.children == null) {
      return this.props.children;
    } else {
      var clonedChildren = React.cloneElement(this.props.children, {login: this.login, state: this.state});
      return clonedChildren;
    }
  }

}
class Login extends Component {

  constructor() {
    super()
  }

  render() {
    return <h1>Login</h1>
  }
}
class Container extends Component {

  constructor() {
    super();
    this.state = this.props.state;
  }

  componentWillMount() {
    if (this.state.user == null) {
      const router = this.props.router;
      if (!router.isActive('/login')) {
        router.push('/login');
      }
    }
  }

  render() {
    return <div>
      <MyNavigation user={this.state.user}/>
      {this.props.children}
    </div>
  }
}


const Home = () => <h1>Hello from Home!</h1>
const NotFound = () => (
  <h1>404.. This page is not found!</h1>)
export default App;
