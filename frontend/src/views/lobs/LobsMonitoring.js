import React, {Component} from "react";
import {Link, hashHistory} from "react-router";
import {bindActionCreators} from "redux";
import {connect} from "react-redux";
import {showLoading, hideLoading} from "react-redux-loading-bar";
import Api from "../../Api";


function mapStateToProps(state) {
  return {auth: state.auth};
}
function mapDispatchToProps(dispatch) {
  var actions = {showLoading: showLoading, hideLoading: hideLoading};
  return bindActionCreators(actions, dispatch);
}
class LobsMonitoring extends Component {
  constructor() {
    super();
    this.state = {}

  }

  goToLobDetail(lobName) {
    hashHistory.push(this.props.location.pathname + "/" + lobName);
  }

  componentDidMount() {
    Api.fetch("/lobs/config/", {method: 'GET'}).then((response) => {
      this.setState({lobs: response.lobs});
    });
    Api.fetch("/lobs/status/", {method: 'GET'}).then((response) => {
      this.setState({status: response});
    });
  }

  render() {
    let lobRows = [];
    if (this.state.lobs) {
      for (let lobName in this.state.lobs) {
        let lob = this.state.lobs[lobName]
        let flowStatuses = null
        let statusSpan = [<span className="badge badge-primary"></span>]
        if (this.state.status) {
          let status = this.state.status[lobName]
          flowStatuses = (<div>
            <h5>
              <span style={{minWidth: 3 + "em"}} title="ok"
                    className="badge badge-pill badge-success">{status.OK}</span>
              &nbsp;
              <span style={{minWidth: 3 + "em"}} title="warning"
                    className="badge badge-pill badge-warning">{status.WARNING}</span>
              &nbsp;
              <span style={{minWidth: 3 + "em"}} title="outage"
                    className="badge badge-pill badge-danger">{status.OUTAGE + status.N_A}</span>
              &nbsp;
              {status.DISABLED > 0 &&
              <span style={{minWidth: 3 + "em"}} title="Disabled"
                    className="badge badge-pill badge-default">{status.DISABLED}</span>
              }
            </h5>
          </div>)
          if (status.OUTAGE > 0) {
            statusSpan = [<span style={{marginRight: "3px"}} className="badge badge-danger">outage</span>]
          } else if (status.WARNING > 0) {
            statusSpan = [<span style={{marginRight: "3px"}} className="badge badge-warning">warning</span>]
          } else if (status.OK > 0) {
            statusSpan = [<span style={{marginRight: "3px"}} className="badge badge-success">ok</span>]
          }
          if (status.N_A > 0) {
            statusSpan.push(<span className="badge badge-danger">n/a</span>)
          }
        }
        lobRows.push(
          <tr onClick={this.goToLobDetail.bind(this, lobName)}>
            <td>{lobName}</td>
            <td>
              {flowStatuses}
            </td>
            <td>
              <h4>{statusSpan}</h4>
            </td>
          </tr>)
      }
    }
    return (
      <div className="animated fadeIn">
        <div className="row">
          <div className="col-lg-2">
            <div className="card">
              <div className="card-block">
                <div style={{fontSize: 2 + "em"}}>
                  <span className="badge badge-pill badge-success">42</span>
                  <span className="badge badge-pill badge-warning">3</span>
                  <span className="badge badge-pill badge-danger">0</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="row">
          <div className="col-lg-12">
            <div className="card">
              <div className="card-header">
                <i className="fa fa-align-justify"></i> Lobs list
              </div>
              <div className="card-block">
                <table className="table">
                  <thead>
                  <tr>
                    <th>Lob Name</th>
                    <th>Flows</th>
                    <th>Status</th>
                  </tr>
                  </thead>
                  <tbody>
                  {lobRows}
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

LobsMonitoring = connect(mapStateToProps, mapDispatchToProps)(LobsMonitoring)
export default LobsMonitoring