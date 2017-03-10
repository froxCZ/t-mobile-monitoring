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
    Api.fetch("/lobs/", {method: 'GET'}).then((response) => {
      this.setState({lobs: response.lobs});
    });
  }

  render() {
    let lobRows = [];
    if (this.state.lobs) {
      for (let lobName in this.state.lobs) {
        lobRows.push(
          <tr onClick={this.goToLobDetail.bind(this, lobName)}>
            <td>{lobName}</td>
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
                    <th>Traffic Level</th>
                    <th>Forwardings</th>
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