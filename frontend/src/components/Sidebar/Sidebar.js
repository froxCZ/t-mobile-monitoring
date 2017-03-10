import React, {Component} from "react";
import {Link} from "react-router";

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
              Lobs
            </li>
            <li className="nav-item">
              <Link to={'/lobs/monitoring'} className="nav-link" activeClassName="active">Monitoring</Link>
            </li>
            <li className="nav-item">
              <Link to={'/lobs/tuning'} className="nav-link" activeClassName="active">Tuning</Link>
            </li>
            <li className="nav-item">
              <Link to={'/lobs/settings'} className="nav-link" activeClassName="active">Settings</Link>
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
