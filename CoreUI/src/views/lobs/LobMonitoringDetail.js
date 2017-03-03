import React, {Component} from "react";
import {hashHistory} from "react-router";
export default class LobMonitoringDetail extends Component {
  constructor() {
    super()


  }

  goToForwardDetail(forwardName) {
    hashHistory.push(this.props.location.pathname + "/" + forwardName);
  }

  render() {
    this.lobName = this.props.params.lobName
    return (
      <div className="animated fadeIn">
        <div className="row">
          <div className="col-lg-12">
            <h2>{this.lobName}</h2>
          </div>
        </div>
        <div className="row">
          <div className="col-lg-12">
            <div className="card">
              <div className="card-header">
                <i className="fa fa-align-justify"></i> Forwards list
              </div>
              <div className="card-block">
                <table className="table">
                  <thead>
                  <tr>
                    <th>Lob Name</th>
                    <th>Traffic Level</th>
                    <th>Forwardings</th>
                    <th>Status</th>
                  </tr>
                  </thead>
                  <tbody>
                  <tr onClick={this.goToForwardDetail.bind(this, 'MMFB')}>
                    <td>MMFB</td>
                    <td>80%</td>
                    <td>
                      <span className="badge badge-pill badge-success">42</span>
                      <span className="badge badge-pill badge-warning">3</span>
                      <span className="badge badge-pill badge-danger">0</span>
                    </td>
                    <td>
                      <span className="badge badge-success">OK</span>
                      <span className="badge badge-warning">WARNING</span>
                      <span className="badge badge-danger">ERROR</span>
                    </td>
                  </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

        </div>
      </div>

    )
  }
}