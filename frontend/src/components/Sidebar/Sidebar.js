import React, {Component} from "react";
import {Link} from "react-router";
import Util from "../../Util";

class Sidebar extends Component {

  handleClick(e) {
    e.preventDefault();
    e.target.parentElement.classList.toggle('open');
  }

  activeRoute(routeName) {
    return this.props.location.pathname.indexOf(routeName) > -1 ? 'nav-item nav-dropdown open' : 'nav-item nav-dropdown';
  }

  // secondLevelActive(routeName) {
  //   return this.props.location.pathname.indexOf(routeName) > -1 ? "nav nav-second-level collapse in" : "nav nav-second-level collapse";
  // }

  render() {
    return (

      <div className="sidebar">
        <nav className="sidebar-nav">
          <ul className="nav">
            <li className="nav-item">
              <Link to={'/dashboard'} className="nav-link" activeClassName="active"><i className="icon-speedometer"></i>
                Dashboard <span className="badge badge-info">NEW</span></Link>
            </li>
            <li className="nav-title">
              Mediation
            </li>
            <li className="nav-item nav-dropdown open">
              <ul className="nav-dropdown-items">
                <li className="nav-item">
                  <Link to={'/mediation/monitoring/CZ'} className="nav-link" activeClassName="active">
                    <img src={Util.countryToFlagPath("CZ")} alt="Czech Republic" style={{height: 15 + 'px'}}/>
                    &nbsp; Monitoring
                  </Link>
                </li>
                <li className="nav-item">
                  <Link to={'/mediation/monitoring/AT'} className="nav-link" activeClassName="active">
                    <img src={Util.countryToFlagPath("AT")} alt="Czech Republic" style={{height: 15 + 'px'}}/>&nbsp;
                    Monitoring</Link>
                </li>
                <li className="nav-item">
                  <Link to={'/mediation/monitoring/NL'} className="nav-link" activeClassName="active">
                    <img src={Util.countryToFlagPath("NL")} alt="Czech Republic" style={{height: 15 + 'px'}}/>&nbsp;
                    Monitoring</Link>
                </li>
                <li className="nav-item">
                  <Link to={'/mediation/monitoring/DE'} className="nav-link" activeClassName="active">
                    <img src={Util.countryToFlagPath("DE")} alt="Czech Republic" style={{height: 15 + 'px'}}/>&nbsp;
                    Monitoring</Link>
                </li>
                <li className="nav-item">
                  <Link to={'/mediation/settings'} className="nav-link" activeClassName="active">
                    <i className="icon-wrench"></i>Settings</Link>
                </li>
              </ul>
            </li>
            <li className="nav-title">
            </li>
            <li className="nav-title">
              Big data tools
            </li>
            <li className="nav-item">
              <Link to={'/zookeeper'} className="nav-link" activeClassName="active">Zookeeper</Link>
              <Link to={'/hadoop'} className="nav-link" activeClassName="active">Hadoop</Link>
            </li>
            <li className="nav-title">
            </li>
            <li className="nav-title">
              Incidents
            </li>

            <li className="nav-item">
              <Link to={'/incidents/active'} className="nav-link" activeClassName="active">Active</Link>
            </li>
            <li className="nav-item">
              <Link to={'/incidents/archive'} className="nav-link" activeClassName="active">Archive</Link>
            </li>

            <li className="nav-title">
            </li>
            <li className="nav-title">
              Settings
            </li>
            <li className="nav-item">
              <Link to={'/settings/users'} className="nav-link" activeClassName="active">Users</Link>
            </li>

          </ul>
        </nav>
      </div>
    )
  }
}

export default Sidebar;
