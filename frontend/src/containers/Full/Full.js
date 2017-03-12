import React, {Component} from "react";
import Header from "../../components/Header/";
import Sidebar from "../../components/Sidebar/";
import Aside from "../../components/Aside/";
import Footer from "../../components/Footer/";
import Breadcrumbs from "react-breadcrumbs";
import {browserHistory} from "react-router";
import {bindActionCreators} from "redux";
import {connect} from "react-redux";
import {Actions as AuthActions} from "../../Store";
function mapStateToProps(state) {
  return {auth: state.auth};
}
function mapDispatchToProps(dispatch) {
  return bindActionCreators(AuthActions, dispatch);
}
class Full extends Component {

  componentWillMount() {
    this.checkUser(this.props);
  }

  componentWillUpdate(nextProps, nextState) {
    this.checkUser(nextProps);
  }

  checkUser(props) {
    if (props.auth.user == null) {
      browserHistory.push("/public/login");
    }
  }

  render() {
    return (
      <div className="app">

        <Header />
        <div className="app-body">
          <Sidebar {...this.props}/>
          <main className="main">
            <Breadcrumbs
              wrapperElement="ol"
              wrapperClass="breadcrumb"
              itemClass="breadcrumb-item"
              separator=""
              routes={this.props.routes}
              params={this.props.params}
            />
            <div className="container-fluid">
              {this.props.children}
            </div>
          </main>
          <Aside />
        </div>
        <Footer />
      </div>
    );
  }
}

Full = connect(mapStateToProps, mapDispatchToProps)(Full);
export default Full
