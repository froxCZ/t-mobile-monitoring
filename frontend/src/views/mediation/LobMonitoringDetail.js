import React, {Component} from "react";
import {hashHistory} from "react-router";
import Api from "../../Api";
import classnames from "classnames";
import {TabContent, TabPane, Nav, NavItem, NavLink} from "reactstrap";
import LobOverviewCharts from "../../components/LobOverviewCharts";
import _ from "lodash";

const LIST_TAB = 'listTab'
const CHART_TAB = 'chartTab'
const CONFIG_TAB = 'configTab'
export default class LobMonitoringDetail extends Component {
  constructor() {
    super()
    this.state = {activeTab: LIST_TAB, optionsString: ''}

  }

  goToFlowDetail(flowName) {
    hashHistory.push(this.props.location.pathname + "/" + flowName);
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
      this.reloadLob(lobName);
    }
  }

  reloadLob(lobName) {
    this.setState({lobName: lobName});
    Api.fetch("/mediation/config/" + lobName, {method: 'GET'}).then((response) => {
      this.setState({lob: response, optionsString: JSON.stringify(response.options, null, 2)});
    });
    Api.fetch("/mediation/status/lob/" + lobName, {method: 'GET'}).then((response) => {
      this.setState({status: response})
    });
  }

  toggle(tab) {
    if (this.state.activeTab !== tab) {
      this.setState({
        activeTab: tab
      });
    }
  }

  render() {

    return (
      <div className="animated fadeIn">
        <div className="row">
          <div className="col-lg-12">
            <h2>{this.state.lobName}</h2>
          </div>
        </div>
        <div className="row">
          <div className="col-lg-12">
            <Nav tabs>
              <NavItem>
                <NavLink
                  className={classnames({active: this.state.activeTab === LIST_TAB})}
                  onClick={() => {
                    this.toggle(LIST_TAB);
                  }}
                >
                  List
                </NavLink>
              </NavItem>
              <NavItem>
                <NavLink
                  className={classnames({active: this.state.activeTab === CHART_TAB})}
                  onClick={() => {
                    this.toggle(CHART_TAB);
                  }}
                >
                  Charts Overview
                </NavLink>
              </NavItem>
              <NavItem>
                <NavLink
                  className={classnames({active: this.state.activeTab === CONFIG_TAB})}
                  onClick={() => {
                    this.toggle(CONFIG_TAB);
                  }}
                >
                  Config
                </NavLink>
              </NavItem>
            </Nav>
            <TabContent activeTab={this.state.activeTab}>
              <TabPane tabId={LIST_TAB}>
                {this.renderList()}
              </TabPane>
              <TabPane tabId={CHART_TAB}>
                {this.renderCharts()}
              </TabPane>
              <TabPane tabId={CONFIG_TAB}>
                {this.renderConfig()}
              </TabPane>
            </TabContent>
          </div>
        </div>
      </div>
    )
  }

  renderCharts() {
    return <div>
      <LobOverviewCharts lobName={this.state.lobName} lob={this.state.lob}/>
    </div>
  }

  isValidJson(str) {
    try {
      JSON.parse(str);
    } catch (e) {
      return false;
    }
    return true;
  }

  renderConfig() {
    let isValidJson = this.isValidJson(this.state.optionsString)
    let buttonText = isValidJson ? "Save" : "Invalid JSON"
    return (
      <div className="row">
        <div className="col-sm-3">
          <div className="card">
            <div className="card-header">
              Lob Options
            </div>
            <div className="card-block">

                <textarea id="textarea-input"
                          name="textarea-input"
                          rows="15"
                          className="form-control" value={this.state.optionsString}
                          onChange={(e) => this.setState({optionsString: e.target.value})}
                />
              <div style={{display: "block"}}>
                <button type="button"
                        className="btn btn-primary"
                        disabled={!isValidJson}
                        onClick={
                          () => {
                            this.saveOptions()
                          }}>{buttonText}
                </button>
              </div>

            </div>
          </div>
        </div>
      </div>)
  }

  saveOptions() {
    if (!this.isValidJson(this.state.optionsString)) {
      return
    }
    var myInit = {
      method: 'PUT',
      body: this.state.optionsString
    };
    Api.fetch("/mediation/config/" + this.state.lobName + "/options", myInit);
  }

  getTrafficDifference(flow) {
    let flowName = flow.name
    if (this.state.status && flowName in this.state.status && this.state.status[flowName].difference) {
      return this.state.status[flowName].difference
    } else {
      return "-"
    }
  }


  getStatusBadge(flow) {
    let flowName = flow.name;
    if (this.state.status && flowName in this.state.status) {
      let flowStatus = this.state.status[flowName].status
      let badge = null;
      if(flowStatus == "DISABLED"){
        badge = <span className="badge badge-default">disabled</span>
      }else if (flowStatus == "OK") {
        badge = <span className="badge badge-success">ok</span>
      } else if (flowStatus == "WARNING") {
        badge = <span className="badge badge-warning">warning</span>
      } else if (flowStatus == "OUTAGE") {
        badge = <span className="badge badge-danger">outage</span>
      } else if (flowStatus == "N_A") {
        badge = <span className="badge badge-danger">n/a</span>
      }
      return badge;
    } else {
      return "-"
    }
  }


  flowEnabledChange(e, flow) {
    let body = {enable: e.target.checked}
    var myInit = {
      method: 'PUT',
      body: body
    };
    let type = flow.type
    Api.fetch("/mediation/config/" + flow.lobName + "/flow/" + flow.name + "/enable", myInit)
      .then(response => {
        let newState = _.extend({}, this.state);
        newState.lob[type][flow.name].options = response
        this.setState(newState);
      });

  }

  renderList() {
    let neidRows = []
    let forwardRows = []
    if (this.state.lob) {
      for (let flowName in this.state.lob.inputs) {
        let flow = this.state.lob.inputs[flowName]
        neidRows.push(
          <tr onClick={this.goToFlowDetail.bind(this, flowName)}>
            <td>{flowName}</td>
            <td>{flow.options.granularity}</td>
            <td>{flow.options.softAlarmLevel}</td>
            <td>{flow.options.hardAlarmLevel}</td>
            <td>{this.getTrafficDifference(flow)}</td>
            <td>
              <h4>{this.getStatusBadge(flow)}</h4>
            </td>
            <td>
              <label className="switch switch-3d switch-primary" onClick={(e) => e.stopPropagation()}>
                <input type="checkbox" className="switch-input"
                       checked={flow.options.enabled}
                       onChange={(e) => this.flowEnabledChange(e, flow)}
                />
                <span className="switch-label"></span>
                <span className="switch-handle"></span>
              </label>
            </td>
          </tr>)
      }
      for (let flowName in this.state.lob.forwards) {
        let flow = this.state.lob.forwards[flowName]
        forwardRows.push(
          <tr onClick={this.goToFlowDetail.bind(this, flowName)}>
            <td>{flowName}</td>
            <td>{flow.options.granularity}</td>
            <td>{flow.options.softAlarmLevel}</td>
            <td>{flow.options.hardAlarmLevel}</td>
            <td>{this.getTrafficDifference(flow)}</td>
            <td>
              <h4>{this.getStatusBadge(flow)}</h4>
            </td>
            <td>
              <label className="switch switch-3d switch-primary" onClick={(e) => e.stopPropagation()}>
                <input type="checkbox" className="switch-input"
                       checked={flow.options.enabled}
                       onChange={(e) => this.flowEnabledChange(e, flow)}
                />
                <span className="switch-label"></span>
                <span className="switch-handle"></span>
              </label>
            </td>
          </tr>)
      }
    }
    return (<div>
      <div className="row">
        <div className="col-lg-12">
          <div className="card">
            <div className="card-header">
              <i className="fa fa-align-justify"></i> Inputs list
            </div>
            <div className="card-block">
              <table className="table">
                <thead>
                <tr>
                  <th>Neid</th>
                  <th>Granularity</th>
                  <th>Soft Alarm</th>
                  <th>Hard Alarm</th>
                  <th>Traffic level</th>
                  <th>Status</th>
                  <th>Enabled</th>
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
                  <th>Forward</th>
                  <th>Granularity</th>
                  <th>Soft Alarm</th>
                  <th>Hard Alarm</th>
                  <th>Traffic level</th>
                  <th>Status</th>
                  <th>Enabled</th>

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
    </div>)
  }
}