import React, {Component} from 'react';
import {bindActionCreators} from 'redux';
import {connect} from 'react-redux';
import * as ActionTypes from '../const/ActionTypes';
import {Actions as UserActions} from '../actions/User';
function mapStateToProps(state) {
  return {user: state.user};
}
function mapDispatchToProps(dispatch) {
  return bindActionCreators(UserActions, dispatch);
}


export class Login extends Component {

  constructor(props) {
    super(props);
    console.log(props);
  }

  login(e) {
    e.preventDefault();
    this.props.login(this._username.value, this._password.value);
    /*    var body = {
     username: this._username.value,
     password: this._password.value,
     };
     fetch("/login", {
     method: "POST",
     body: body
     }).then((response) => {
     return response.json()
     }).then((bodyJSON) => {
     this.props.login(bodyJSON);
     })*/
  }

  render() {
    // if (this.props.user != null) {
    //   const router = this.props.router;
    //   router.push('/');
    // }
    return <form>
      <input ref={e =>this._username = e}/>
      <input ref={e =>this._password = e}/>
      <button onClick={this.login.bind(this)}></button>
    </form>
  }
}

Login = connect(mapStateToProps,mapDispatchToProps)(Login);
export default Login