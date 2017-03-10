import React, {Component} from "react";
import {Link} from "react-router";
import classNames from "classnames";

class Sidebar extends Component {

  constructor(props) {
    super(props);
    this.state = {
      uiElementsCollapsed: true,
      chartsElementsCollapsed: true,
      multiLevelDropdownCollapsed: true,
      thirdLevelDropdownCollapsed: true,
      samplePagesCollapsed: true,
    };
  }

  push(url){
    console.log("url this.push not implemented");

  }

  render() {
    return (
      <div className="navbar-default sidebar" style={{ marginLeft: '-20px' }} role="navigation">
        <div className="sidebar-nav navbar-collapse collapse">
          <ul className="nav in" id="side-menu">
            <li className="sidebar-search">
              <div className="input-group custom-search-form">
                <input type="text" className="form-control" placeholder="Search..." />
                <span className="input-group-btn">
                  <button className="btn btn-default" type="button">
                    <i className="fa fa-search" />
                  </button>
                </span>
              </div>
            </li>

            <li>
              <a href="" onClick={(e) => { e.preventDefault(); this.push('/'); }} >
                <i className="fa fa-dashboard fa-fw" /> &nbsp;Dashboard
              </a>
            </li>

            <li className={classNames({ active: !this.state.chartsElementsCollapsed })}>
              <a
                href=""
                onClick={(e) => {
                  e.preventDefault();
                  this.setState({ chartsElementsCollapsed: !this.state.chartsElementsCollapsed });
                  return false;
                }}
              >
                <i className="fa fa-bar-chart-o fa-fw" /> &nbsp;Lobs monitoring
                <span className="fa arrow" />
              </a>
              <ul
                className={
                  classNames({
                    'nav nav-second-level': true,
                    collapse: this.state.chartsElementsCollapsed,
                  })
              }
              >
                <li>
                    <Link to="/app/lob/chart">Charts</Link>
                </li>
                <li>
                  <a
                    href=""
                    onClick={(e) => { e.preventDefault(); this.push('/morrisjscharts'); }}
                  >
                    Morrisjs Charts
                  </a>
                </li>
              </ul>
            </li>


            <li>
              <a href="" onClick={(e) => { e.preventDefault(); this.push('/table'); }} >
                <i className="fa fa-table fa-fw" /> &nbsp;Tables
              </a>
            </li>

            <li>
              <a href="" onClick={(e) => { e.preventDefault(); this.push('/forms'); }} >
                <i className="fa fa-table fa-fw" /> &nbsp;Forms
              </a>
            </li>

            <li className={classNames({ active: !this.state.uiElementsCollapsed })}>
              <a
                href=""
                onClick={(e) => {
                  e.preventDefault();
                  this.setState({ uiElementsCollapsed: !this.state.uiElementsCollapsed,
                }); return false;
                }}
              >
                <i className="fa fa-edit fa-fw" /> UI Elements<span className="fa arrow" />
              </a>

              <ul
                className={classNames({
                  'nav nav-second-level': true,
                  collapse: this.state.uiElementsCollapsed,
                })}
              >
                <li>
                  <a href="" onClick={(e) => { e.preventDefault(); this.push('/panelwells'); }} >
                    Panels And Wells
                  </a>
                </li>
                <li>
                  <a href="" onClick={(e) => { e.preventDefault(); this.push('/button'); }} >
                    Buttons
                  </a>
                </li>
                <li>
                  <a
                    href=""
                    onClick={(e) => { e.preventDefault(); this.push('/notification'); }}
                  >
                    Notification
                  </a>
                </li>
                <li>
                  <a href="" onClick={(e) => { e.preventDefault(); this.push('/typography'); }} >
                    Typography
                  </a>
                </li>
                <li>
                  <a href="" onClick={(e) => { e.preventDefault(); this.push('/icons'); }} >
                    Icons
                  </a>
                </li>
                <li>
                  <a href="" onClick={(e) => { e.preventDefault(); this.push('/grid'); }} >
                    Grid
                  </a>
                </li>
              </ul>
            </li>

            <li className={classNames({ active: !this.state.multiLevelDropdownCollapsed })}>
              <a
                href=""
                onClick={(e) => {
                  e.preventDefault();
                  this.setState({
                    multiLevelDropdownCollapsed: !this.state.multiLevelDropdownCollapsed,
                  });
                  return false;
                }}
              >
                <i className="fa fa-sitemap fa-fw" />
                &nbsp;Management
                <span className="fa arrow" />
              </a>
              <ul
                className={
                  classNames({
                    'nav nav-second-level': true, collapse: this.state.multiLevelDropdownCollapsed,
                  })}
              >
                <li>
                  <Link to="/app/user">Users</Link>
                </li>
                <li>
                  <a href="" onClick={(e) => { e.preventDefault(); }}>Second Level Item</a>
                </li>
                <li className={classNames({ active: !this.state.thirdLevelDropdownCollapsed })}>
                  <a
                    href=""
                    onClick={(e) => {
                      e.preventDefault();
                      this.setState({
                        thirdLevelDropdownCollapsed: !this.state.thirdLevelDropdownCollapsed,
                      });
                      return false;
                    }}
                  >
                    Third Level<span className="fa arrow" />
                  </a>
                  <ul
                    className={
                      classNames({
                        'nav nav-second-level': true,
                        collapse: this.state.thirdLevelDropdownCollapsed,
                      })}
                  >
                    <li>
                      <a href="" onClick={(e) => { e.preventDefault(); }}>Third Level Item</a>
                    </li>
                    <li>
                      <a href="" onClick={(e) => { e.preventDefault(); }}>Third Level Item</a>
                    </li>
                    <li>
                      <a href="" onClick={(e) => { e.preventDefault(); }}>Third Level Item</a>
                    </li>
                    <li>
                      <a href="" onClick={(e) => { e.preventDefault(); }}>Third Level Item</a>
                    </li>
                  </ul>
                </li>
              </ul>
            </li>

            <li className={classNames({ active: !this.state.samplePagesCollapsed })}>
              <a
                href=""
                onClick={(e) => {
                  e.preventDefault();
                  this.setState({
                    samplePagesCollapsed: !this.state.samplePagesCollapsed,
                  });
                  return false;
                }}
              >
                <i className="fa fa-files-o fa-fw" />
                &nbsp;Sample Pages
                <span className="fa arrow" />
              </a>
              <ul
                className={
                  classNames({
                    'nav nav-second-level': true,
                    collapse: this.state.samplePagesCollapsed,
                  })}
              >
                <li>
                  <a href="" onClick={(e) => { e.preventDefault(); this.push('/blank'); }} >
                    Blank
                  </a>
                </li>
                <li>
                  <a href="" onClick={(e) => { e.preventDefault(); this.push('/login'); }} >
                    Login
                  </a>
                </li>
              </ul>
            </li>

            <li>
              <a href="http://www.strapui.com/">Premium React Themes</a>
            </li>
          </ul>
        </div>
      </div>
    );
  }
}


export default Sidebar;
