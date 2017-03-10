import React, {Component} from "react";
import {hashHistory} from "react-router";
import Api from "../../Api";
import classnames from "classnames";
import {TabContent, TabPane, Nav, NavItem, NavLink} from "reactstrap";
import LobOverviewCharts from "../../components/LobOverviewCharts";
const LIST_TAB = 'listTab'
const CHART_TAB = 'chartTab'
const CONFIG_TAB = 'configTab'
export default class LobMonitoringDetail extends Component {
  constructor() {
    super()
    this.state = {activeTab: LIST_TAB, optionsString: ''}

  }

  goToForwardDetail(forwardName) {
    hashHistory.push(this.props.location.pathname + "/forward/" + forwardName);
  }

  goToNeidDetail(neidName) {
    hashHistory.push(this.props.location.pathname + "/neid/" + neidName);
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
    Api.fetch("/lobs/config/" + lobName, {method: 'GET'}).then((response) => {
      this.setState({lob: response, optionsString: JSON.stringify(response.options, null, 2)});
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
    if(!this.isValidJson(this.state.optionsString)){
      return
    }
    var myInit = {
      method: 'PUT',
      body: this.state.optionsString
    };
    Api.fetch("/lobs/config/" + this.state.lobName + "/options", myInit);
  }

  renderList() {
    let neidRows = []
    let forwardRows = []
    if (this.state.lob) {
      for (let neidName in this.state.lob.inputs) {
        let neidConfig = this.state.lob.inputs[neidName]
        neidRows.push(
          <tr onClick={this.goToNeidDetail.bind(this, neidName)}>
            <td>{neidName}</td>
            <td>{neidConfig.options.granularity}</td>
            <td>{neidConfig.options.softAlarmLevel}</td>
            <td>{neidConfig.options.hardAlarmLevel}</td>
            <td>-- compare with parent --</td>
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
      for (let forwardName in this.state.lob.forwards) {
        let forward = this.state.lob.forwards[forwardName]
        forwardRows.push(
          <tr onClick={this.goToForwardDetail.bind(this, forwardName)}>
            <td>{forwardName}</td>
            <td>{forward.options.granularity}</td>
            <td>{forward.options.softAlarmLevel}</td>
            <td>{forward.options.hardAlarmLevel}</td>
            <td>--</td>
            <td>70%</td>
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
                  <th>Override</th>
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
                  <th>Forward</th>
                  <th>Granularity</th>
                  <th>Soft Alarm</th>
                  <th>Hard Alarm</th>
                  <th>Override</th>
                  <th>Traffic level</th>
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
    </div>)
  }
}