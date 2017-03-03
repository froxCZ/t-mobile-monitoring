import React, {Component} from "react";
import {hashHistory} from "react-router";
import Api from "../../Api";
export default class LobMonitoringDetail extends Component {
  constructor() {
    super()
    this.state = {}

  }

  goToForwardDetail(forwardName) {
    hashHistory.push(this.props.location.pathname + "/" + forwardName);
  }

  componentWillMount() {
    this.propChange(this.props)
  }

  componentWillReceiveProps(nextProps) {
    this.propChange(nextProps)
  }

  propChange(props) {
    let lobName = props.params.lobName;
    if (this.state.lobName != lobName) {
      this.setState({lobName: lobName});
      new Api().fetch("/lobs/" + lobName, {method: 'GET'}).then((response) => {
        this.setState({lob: response});
      });
    }
  }

  render() {
    let neidRows = []
    let forwardRows = []
    if (this.state.lob) {
      for (let neidName in this.state.lob.neids) {
        neidRows.push(
          <tr onClick={this.goToForwardDetail.bind(this, neidName)}>
            <td>{neidName}</td>
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
      for (let forward of this.state.lob.forwards) {
        forwardRows.push(
          <tr onClick={this.goToForwardDetail.bind(this, forward.neid)}>
            <td>{forward.neid}</td>
            <td>{forward.target}</td>
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
          <div className="col-lg-12">
            <h2>{this.state.lobName}</h2>
          </div>
        </div>
        <div className="row">
          <div className="col-lg-12">
            <div className="card">
              <div className="card-header">
                <i className="fa fa-align-justify"></i> Neid list
              </div>
              <div className="card-block">
                <table className="table">
                  <thead>
                  <tr>
                    <th>Neid</th>
                    <th>Traffic level</th>
                    <th>Forwardings</th>
                    <th>Status</th>
                  </tr>
                  </thead>
                  <tbody>
                  {neidRows}
                  </tbody>
                </table>
              </div>
            </div>
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
                    <th>Neid</th>
                    <th>Target</th>
                    <th>Forwardings</th>
                    <th>Status</th>
                  </tr>
                  </thead>
                  <tbody>
                  {forwardRows}
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