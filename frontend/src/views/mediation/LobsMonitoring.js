import React, {Component} from "react";
import {Link, browserHistory} from "react-router";
import {bindActionCreators} from "redux";
import {connect} from "react-redux";
import {showLoading, hideLoading} from "react-redux-loading-bar";
import Api from "../../Api";
import StatusBadge from "../../components/StatusBadge";
import StatusCounterBadge from "../../components/StatusCounterBadge";


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
    browserHistory.push(this.props.location.pathname + "/" + lobName);
  }

  propChange(props) {
    let country = props.params.country;
    if (country != this.state.country) {
      this.reloadData(country)
    }
  }

  reloadData(country) {
    this.setState({country: country})
    Api.fetch("/mediation/flows/" + country, {method: 'GET'}).then((response) => {
      this.setState({lobs: response});
    });
  }

  componentWillMount() {
    this.propChange(this.props)
  }

  componentWillReceiveProps(nextProps) {
    this.propChange(nextProps)
  }

  render() {
    let lobRows = [];
    if (this.state.lobs) {
      for (let lobName in this.state.lobs) {
        let lob = this.state.lobs[lobName]
        let flowStatuses = null
        let statusSpan = [<span className="badge badge-primary"></span>]

        let status = lob.status
        flowStatuses = (<div>
          <h5>
            <StatusCounterBadge statuses={status}/>
          </h5>
        </div>)
        if (status.OUTAGE > 0) {
          statusSpan = [<StatusBadge style={{marginRight: "3px"}} status="OUTAGE"/>]
        } else if (status.WARNING > 0) {
          statusSpan = [<StatusBadge style={{marginRight: "3px"}} status="WARNING"/>]
        } else if (status.OK > 0) {
          statusSpan = [<StatusBadge style={{marginRight: "3px"}} status="OK"/>]
        }
        if (status.N_A > 0) {
          statusSpan.push([<StatusBadge style={{marginRight: "3px"}} status="N_A"/>])
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
    if (this.props.params) {
      lobRows.push(<tr>
          <td>
            {this.props.params.country}_<input type="text"
                                               id="text-input"
                                               name="text-input"
                                               className="form-control col-lg-1"
                                               style={{display: "inline"}}
                                               ref="newLobName"
                                               placeholder="Lob name"/>
            &nbsp;
            <button type="button" className="btn btn-primary active" onClick={() => this.addLob()}>Add</button>
          </td>
        </tr>
      )
    }
    console.log(lobRows)
    return (
      <div className="animated fadeIn">
        <div className="row">
          <div className="col-lg-12">
            <h2>{this.state.country} monitoring</h2>
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

  addLob() {
    let country = this.props.params.country;
    let lobName = this.refs.newLobName.value;
    if (lobName == null || lobName.length == 0)return;
    let req = {
      method: "POST",
      body: {country: country, lobName: country + "_" + lobName}
    }
    Api.fetch("/mediation/flows/", req).then(response => {
      this.reloadData(this.props.params.country);
    })

  }
}

LobsMonitoring = connect(mapStateToProps, mapDispatchToProps)(LobsMonitoring)
export default LobsMonitoring