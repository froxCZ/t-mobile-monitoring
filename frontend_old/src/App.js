import React, {Component} from "react";
import "./App.css";
import {connect} from "react-redux";

function mapStateToProps(state) {
  return {auth: state.auth};
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
    this.isRouting = false;
    if (this.props.auth.user == null) {
      if (!router.isActive("/login")) {
        router.push("/login");
        this.isRouting = true;
      }
    } else {
      if (router.isActive("/login")) {
        router.push("/app");
        this.isRouting = true;
      }
    }
  }
  render() {
    if(!this.isRouting) {
      return this.props.children;
    }else{
      return <div></div>
    }

  }
}

App = connect(mapStateToProps)(App);
export default App


