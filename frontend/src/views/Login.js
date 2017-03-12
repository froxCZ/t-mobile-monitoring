import React, {Component} from "react";
import {bindActionCreators} from "redux";
import {connect} from "react-redux";
import {Actions as AuthActions} from "../Store";
import {browserHistory} from "react-router";
import Api from "../Api";
function mapStateToProps(state) {
  return {auth: state.auth};
}
function mapDispatchToProps(dispatch) {
  return bindActionCreators(AuthActions, dispatch);
}
class Login extends Component {
  constructor() {
    super()
    this.state = {errorMessage: null}
  }

  componentWillMount() {
    this.checkUser(this.props);
  }

  componentWillUpdate(nextProps, nextState) {
    this.checkUser(nextProps);
  }

  checkUser(props) {
    if (props.auth.user != null) {
      browserHistory.push("/");
    }
  }

  login() {
    let req = {
      method: "POST",
      body: {username: this.refs.username.value, password: this.refs.password.value}
    }
    Api.fetch("/app/login", req).then(response => {
      this.props.loggedIn(response)
    }).catch(e => {
      e.json.then(json => {
        this.setState({errorMessage: json.message})
      })
    })
  }

  render() {
    console.log(this.props)
    return (
      <div className="container">
        <div className="row justify-content-center">
          <div className="col-md-8">
            <div className="card-group mb-0">
              <div className="card p-2">
                <div className="card-block">
                  <h1>Login</h1>
                  <p className="text-muted">Sign In to your account</p>
                  <div className="input-group mb-1">
                    <span className="input-group-addon"><i className="icon-user"></i></span>
                    <input type="text" ref="username" className="form-control" placeholder="Username"/>
                  </div>
                  <div className="input-group mb-2">
                    <span className="input-group-addon"><i className="icon-lock"></i></span>
                    <input type="password" ref="password" className="form-control" placeholder="Password"/>
                  </div>
                  {this.state.errorMessage && <p className="text-muted">{this.state.errorMessage}</p>}
                  <div className="row">
                    <div className="col-6">
                      <button type="button" className="btn btn-primary px-2" onClick={() => {
                        this.login()
                      }}>Login
                      </button>
                    </div>
                    <div className="col-6 text-right">
                      <button type="button" className="btn btn-link px-0">Forgot password?</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

Login = connect(mapStateToProps, mapDispatchToProps)(Login);
export default Login
