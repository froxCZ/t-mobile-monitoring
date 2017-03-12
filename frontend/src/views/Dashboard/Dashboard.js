import React, {Component} from "react";

class Dashboard extends Component {

  render() {
    return (
      <div className="animated fadeIn">

        <div className="row">
          <div className="col-sm-3">
            <div className="card">
              <div className="card-header">
                <i><img src={'img/flags/Germany.png'} alt="Czech Republic"/></i>Overview
              </div>
              <div className="card-block">
                <h2>
                  <span style={{minWidth: 3 + "em"}} title="ok"
                        className="badge badge-pill badge-success">1</span>
                  &nbsp;
                  <span style={{minWidth: 3 + "em"}} title="warning"
                        className="badge badge-pill badge-warning">3</span>
                  &nbsp;
                  <span style={{minWidth: 3 + "em"}} title="outage"
                        className="badge badge-pill badge-danger">8</span>
                  &nbsp;
                  <span style={{minWidth: 3 + "em"}} title="Disabled"
                        className="badge badge-pill badge-default">5</span>
                </h2>
              </div>
            </div>
          </div>
          <div className="col-sm-3">
            <div className="card">
              <div className="card-header">
                <i><img src={'img/flags/Germany.png'} alt="Czech Republic"/></i>Overview
              </div>
              <div className="card-block">
                <h2>
                  <span style={{minWidth: 3 + "em"}} title="ok"
                        className="badge badge-pill badge-success">1</span>
                  &nbsp;
                  <span style={{minWidth: 3 + "em"}} title="warning"
                        className="badge badge-pill badge-warning">3</span>
                  &nbsp;
                  <span style={{minWidth: 3 + "em"}} title="outage"
                        className="badge badge-pill badge-danger">8</span>
                  &nbsp;
                  <span style={{minWidth: 3 + "em"}} title="Disabled"
                        className="badge badge-pill badge-default">5</span>
                </h2>
              </div>
            </div>
          </div>
          <div className="col-sm-3">
            <div className="card">
              <div className="card-header">
                <i><img src={'img/flags/Germany.png'} alt="Czech Republic"/></i>Overview
              </div>
              <div className="card-block">
                <h2>
                  <span style={{minWidth: 3 + "em"}} title="ok"
                        className="badge badge-pill badge-success">1</span>
                  &nbsp;
                  <span style={{minWidth: 3 + "em"}} title="warning"
                        className="badge badge-pill badge-warning">3</span>
                  &nbsp;
                  <span style={{minWidth: 3 + "em"}} title="outage"
                        className="badge badge-pill badge-danger">8</span>
                  &nbsp;
                  <span style={{minWidth: 3 + "em"}} title="Disabled"
                        className="badge badge-pill badge-default">5</span>
                </h2>
              </div>
            </div>
          </div>
          <div className="col-sm-3">
            <div className="card">
              <div className="card-header">
                <i><img src={'img/flags/Germany.png'} alt="Czech Republic"/></i>Overview
              </div>
              <div className="card-block">
                <h2>
                  <span style={{minWidth: 3 + "em"}} title="ok"
                        className="badge badge-pill badge-success">1</span>
                  &nbsp;
                  <span style={{minWidth: 3 + "em"}} title="warning"
                        className="badge badge-pill badge-warning">3</span>
                  &nbsp;
                  <span style={{minWidth: 3 + "em"}} title="outage"
                        className="badge badge-pill badge-danger">8</span>
                  &nbsp;
                  <span style={{minWidth: 3 + "em"}} title="Disabled"
                        className="badge badge-pill badge-default">5</span>
                </h2>
              </div>
            </div>
          </div>

        </div>
      </div>
    )
  }
}

export default Dashboard;
