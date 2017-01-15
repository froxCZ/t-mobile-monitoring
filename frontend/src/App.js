import React, {Component} from 'react';
import logo from './logo.svg';
import './App.css';
import {connect} from 'react-redux';

function mapStateToProps(state) {
  return {user: state.user};
}
class App extends Component {
  componentWillMount() {
    this.routeToLoginIfNeeded();
  }

  componentDidUpdate(prevProps, prevState) {
    this.routeToLoginIfNeeded();
  }

  routeToLoginIfNeeded() {
    const router = this.props.router;
    if (this.props.user == null) {
      if (!router.isActive("/login")) {
        router.push("/login");
      }
    } else {
      if (router.isActive("/login")) {
        router.push("/app");
      }
    }
  }
  render() {
    return this.props.children;
  }
}

App = connect(mapStateToProps)(App);
export default App


