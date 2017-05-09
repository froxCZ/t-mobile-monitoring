import React, {Component} from "react";
import {Dropdown, DropdownMenu, DropdownItem} from "reactstrap";
import LoadingBar from "react-redux-loading-bar";
import {Link, browserHistory} from "react-router";
import Util from "../../Util";
import Api from "../../Api";
import Moment from "moment";
import {bindActionCreators} from "redux";
import {connect} from "react-redux";
import {Actions as AuthActions} from "../../Store";

function mapStateToProps(state) {
  return {auth: state.auth};
}
function mapDispatchToProps(dispatch) {
  return bindActionCreators(AuthActions, dispatch);
}
class Header extends Component {

  constructor(props) {
    super(props);

    this.toggle = this.toggle.bind(this);
    this.state = {
      dropdownOpen: false,
    };
  }

  toggle() {
    this.setState({
      dropdownOpen: !this.state.dropdownOpen
    });
  }

  sidebarToggle(e) {
    e.preventDefault();
    document.body.classList.toggle('sidebar-hidden');
  }

  mobileSidebarToggle(e) {
    e.preventDefault();
    document.body.classList.toggle('sidebar-mobile-show');
  }

  asideToggle(e) {
    e.preventDefault();
    document.body.classList.toggle('aside-menu-hidden');
  }

  componentDidMount() {
    Api.fetch("/app/currentTime", {method: "GET"}).then(response => {
      let serverTimeStr = response.currentTime
      let serverTime = Util.parseIsoDateString(serverTimeStr)
      let serverTimeDiff = Moment.duration(Moment().diff(serverTime))
      Util.setServerTimeDifference(serverTimeDiff)
      this.timerID = setInterval(
        () => this.tick(),
        1000
      );
    })

  }

  componentWillUnmount() {
    clearInterval(this.timerID);
  }

  tick() {
    let serverTime = Util.getCurrentTime()
    this.setState({
      time: serverTime.format("LTS") + " " + serverTime.format("L")
    });
  }

  render() {
    return (
      <header className="app-header navbar">
        <LoadingBar/>
        <button className="navbar-toggler mobile-sidebar-toggler hidden-lg-up" onClick={this.mobileSidebarToggle}
                type="button">&#9776;</button>
        <Link className="navbar-brand" to="/dashboard"></Link>
        <ul className="nav navbar-nav hidden-md-down">
          <li className="nav-item">
            <a className="nav-link navbar-toggler sidebar-toggler" onClick={this.sidebarToggle} href="#">&#9776;</a>
          </li>

        </ul>
        <ul className="nav navbar-nav ml-auto">
          <li style={{marginRight: "3em"}}>
            <span style={{fontWeight: "bold", fontSize: "medium"}}>{this.state.time}</span>
          </li>
          <li className="nav-item">
            <Dropdown isOpen={this.state.dropdownOpen} toggle={this.toggle}>
              <a onClick={this.toggle} className="nav-link dropdown-toggle nav-link" data-toggle="dropdown" href="#"
                 role="button" aria-haspopup="true" aria-expanded={this.state.dropdownOpen}>
                <span className="hidden-md-down">{this.props.auth.user && this.props.auth.user.name}</span>
              </a>

              <DropdownMenu className="dropdown-menu-right">
                <DropdownItem>
                  <div onClick={() => {
                    this.props.logout();
                  }}><i className="fa fa-lock"></i> Logout
                  </div>
                </DropdownItem>
              </DropdownMenu>
            </Dropdown>
          </li>
        </ul>
      </header>
    )
  }
}

Header = connect(mapStateToProps, mapDispatchToProps)(Header);
export default Header
