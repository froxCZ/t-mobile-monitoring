import React, {Component} from 'react';
import ReactDOM from 'react-dom';
import {bindActionCreators} from 'redux';
import {connect} from 'react-redux';
import Button from 'react-bootstrap/lib/Button';
import LoadingButton from '../components/LoadingButton'
import Panel from 'react-bootstrap/lib/Panel';
import {FormControl, Checkbox} from 'react-bootstrap';
import {Actions as AuthActions} from '../actions/Auth';


function mapStateToProps(state) {
  return {auth: state.auth};
}
function mapDispatchToProps(dispatch) {
  return bindActionCreators(AuthActions, dispatch);
}
export class Login extends Component {

  constructor(props) {
    super(props);
  }

  login(e) {
    e.preventDefault();

    this.props.login(this.getValueOfRef(this._username), this.getValueOfRef(this._password));

  }

  getValueOfRef(ref) {
    return ReactDOM.findDOMNode(ref).value;
  }

  render() {
    console.log(this.props.auth.isLoading);
    return <div className="col-md-4 col-md-offset-4">
      <div className="text-center">
        <h1 className="login-brand-text">Monitoring Tool</h1>
      </div>

      <Panel header={<h3>Please Sign In</h3>} className="login-panel">

        <form role="form" onSubmit={this.login.bind(this)}>
          <fieldset>
            {this.props.auth.loginFailed && <div className="has-error">
              <label className="control-label">Login failed, try again.</label>
            </div>
            }
            <div className="form-group">
              <FormControl
                type="text"
                className="form-control"
                placeholder="Username"
                name="name"
                ref={e =>this._username = e}
              />
            </div>

            <div className="form-group">
              <FormControl
                className="form-control"
                placeholder="Password"
                type="password"
                name="password"
                ref={e =>this._password = e}
              />
            </div>
            <Checkbox label="Remember Me"> Remember Me </Checkbox>
            <LoadingButton isLoading={this.props.auth.isLoading} type="submit" bsSize="large" bsStyle="success" block>Login</LoadingButton>
          </fieldset>
        </form>

      </Panel>

    </div>
  }
}

Login = connect(mapStateToProps, mapDispatchToProps)(Login);
export default Login