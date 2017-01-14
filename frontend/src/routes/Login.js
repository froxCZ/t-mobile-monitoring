import React, {Component} from 'react';
import {bindActionCreators} from 'redux';
import {connect} from 'react-redux';
import * as ActionTypes from '../const/ActionTypes';

function mapStateToProps(state) {
  return {user: state.user};
}
function mapDispatchToProps(dispatch) {
  return {
    login: (user)=> {
      dispatch({
        type: ActionTypes.LOGIN,
        user: user
      })
    }
  }
}


class Login extends Component {

  constructor() {
    super()
  }

  componentWillMount() {
    this.routeToLoginIfNeeded();
  }

  componentDidUpdate(prevProps, prevState) {
    this.routeToLoginIfNeeded();
  }

  routeToLoginIfNeeded(){
    const router = this.props.router;
    if (this.props.user == null) {
      if(!router.isActive("/login")){
        router.push("/login");
      }
    } else {
      if(!router.isActive("/push")){
        router.push("/app");
      }
    }
  }

  login(e) {
    e.preventDefault();
    var body = {
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
    })
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

Login = connect(mapStateToProps, mapDispatchToProps)(Login);
export default Login