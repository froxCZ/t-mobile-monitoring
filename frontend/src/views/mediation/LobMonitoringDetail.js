import React, {Component} from "react";
import Api from "../../Api";
import Util from "../../Util";
import classnames from "classnames";
import {
  TabContent,
  TabPane,
  Nav,
  NavItem,
  NavLink,
  Button,
  Modal,
  ModalHeader,
  ModalBody,
  ModalFooter
} from "reactstrap";
import LobOverviewCharts from "../../components/LobOverviewCharts";
import _ from "lodash";
import StatusBadge from "../../components/StatusBadge";
import {Link, browserHistory} from "react-router";
const LIST_TAB = 'listTab'
const CHART_TAB = 'chartTab'
const CONFIG_TAB = 'configTab'
class LobMonitoringDetail extends Component {
  constructor() {
    super()
    this.state = {activeTab: LIST_TAB, optionsString: '', expand: false}
    this.isRoot = false;
    this.closeModal = this.closeModal.bind(this);
  }

  componentWillMount() {
    this.propChange(this.props)
  }

  componentWillReceiveProps(nextProps) {
    this.propChange(nextProps)
  }

  propChange(props) {
    let country = props.params.country;
    let lobName = props.params.lobName;
    if (this.state.lobName != lobName || country != this.state.country) {
      this.reloadLob(country, lobName);
    }
  }

  reloadLob(country, lobName) {
    this.setState({lobName: lobName, country: country});
    Api.fetch("/mediation/flows/" + country + "/" + lobName, {method: 'GET'}).then((response) => {
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
    this.isRoot = Util.isRoot(this.props.user)

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
              {this.isRoot &&
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
              }

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
    Api.fetch("/mediation/flows/" + this.state.country + "/" + this.state.lobName + "/options", myInit);
  }

  flowEnabledChange(e, flow) {
    let body = {enable: e.target.checked}
    var myInit = {
      method: 'PUT',
      body: body
    };
    let type = flow.type
    Api.fetch("/mediation/flows/" + flow.country + "/" + flow.lobName + "/" + flow.name + "/enable", myInit)
      .then(response => {
        let newState = _.extend({}, this.state);
        newState.lob[type][flow.name].options = response
        this.setState(newState);
        this.reloadLob(this.state.country, this.state.lobName)
      });

  }

  renderList() {
    let neidRows = []
    let forwardRows = []
    let maxRows = this.state.expand ? 100000 : 100000
    if (this.state.lob) {
      let counter = 0
      for (let flowName in this.state.lob.inputs) {
        if (counter++ > maxRows)break;
        let flow = this.state.lob.inputs[flowName]
        neidRows.push(
          <tr>
            <td>
              <Link to={this.props.location.pathname + '/' + flowName} className="nav-link" activeClassName="active">
                {flowName}
              </Link>
            </td>
            <td>{flow.options.granularity}</td>
            <td>{flow.options.softAlarmLevel}</td>
            <td>{flow.options.hardAlarmLevel}</td>
            <td>{flow.status.difference}</td>
            <td>
              <h4><StatusBadge status={flow.status.status}/></h4>
            </td>
            <td>
              <label className="switch switch-3d switch-primary" onClick={(e) => e.stopPropagation()}>
                <input type="checkbox" className="switch-input"
                       checked={flow.options.enabled}
                       onChange={(e) => this.isRoot && this.flowEnabledChange(e, flow)}
                />
                <span className="switch-label"></span>
                <span className="switch-handle"></span>
              </label>
            </td>
            <td>
              {this.isRoot &&
              <i className="icon-trash icons font-2xl d-block" style={{cursor: 'pointer'}}
                 onClick={() => this.setState({flowToDelete: flow})}></i>
              }
            </td>
          </tr>)
      }
      if (this.isRoot) {
        neidRows.push(<tr>
            <td><input type="text"
                       id="text-input"
                       name="text-input"
                       className="form-control col-lg-2"
                       style={{display: "inline"}}
                       ref="addFlowinputs"
                       placeholder="Input name"/>
              &nbsp;
              <button type="button"
                      className="btn btn-primary active"
                      onClick={() => this.addFlow("inputs")}>Add
              </button>
            </td>
          </tr>
        );
      }
      counter = 0
      for (let flowName in this.state.lob.forwards) {
        if (counter++ > maxRows)break;
        let flow = this.state.lob.forwards[flowName]
        forwardRows.push(
          <tr>
            <td>
              <Link to={this.props.location.pathname + '/' + flowName} className="nav-link" activeClassName="active">
                {flowName}
              </Link>
            </td>
            <td>{flow.options.granularity}</td>
            <td>{flow.options.softAlarmLevel}</td>
            <td>{flow.options.hardAlarmLevel}</td>
            <td>{flow.status.difference}</td>
            <td>
              <h4><StatusBadge status={flow.status.status}/></h4>
            </td>
            <td>
              <label className="switch switch-3d switch-primary" onClick={(e) => e.stopPropagation()}>
                <input type="checkbox" className="switch-input"
                       checked={flow.options.enabled}
                       onChange={(e) => this.isRoot && this.flowEnabledChange(e, flow)}
                />
                <span className="switch-label"></span>
                <span className="switch-handle"></span>
              </label>
            </td>
            <td>
              {this.isRoot && <i className="icon-trash icons font-2xl d-block" style={{cursor: 'pointer'}}
                                 onClick={() => this.setState({flowToDelete: flow})}></i>
              }
            </td>
          </tr>)
      }
      if (this.isRoot) {
        forwardRows.push(<tr>
            <td><input type="text"
                       id="text-input"
                       name="text-input"
                       className="form-control col-lg-2"
                       style={{display: "inline"}}
                       ref="addFlowforwards"
                       placeholder="Foward name"/>
              &nbsp;
              <button type="button"
                      className="btn btn-primary active"
                      onClick={() => this.addFlow("forwards")}>Add
              </button>
            </td>
          </tr>
        )
      }
    }
    return (<div>
      {this.createDeleteModal()}
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
                  <th>Delete</th>
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
                  <th>Delete</th>

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

  createDeleteModal() {
    if (!this.state.flowToDelete) {
      return <div></div>
    }
    let flowToDelete = this.state.flowToDelete;
    return <Modal isOpen={flowToDelete != null}
                  toggle={this.closeModal} className={'modal-primary ' + this.props.className}>
      <ModalHeader toggle={this.closeModal}>Delete Flow</ModalHeader>
      <ModalBody>
        Do you want to delete flow {flowToDelete.name}?
      </ModalBody>
      <ModalFooter>
        <Button color="danger" onClick={() => this.deleteFlow(flowToDelete)}>Delete</Button>{' '}
        <Button color="secondary" onClick={this.closeModal}>Cancel</Button>
      </ModalFooter>
    </Modal>
  }

  addFlow(type) {
    let country = this.state.country;
    let lobName = this.state.lobName;
    let name = this.refs["addFlow" + type].value;
    let req = {
      method: "POST",
      body: {country: country, lobName: lobName, type: type, name: name}
    };
    Api.fetch("/mediation/flows/" + country + "/" + lobName, req).then(response => {
      this.reloadLob(country, lobName)
    })

  }

  deleteFlow(flowToDelete) {
    let req = {
      method: "DELETE"
    };
    Api.fetch("/mediation/flows/" + flowToDelete.country + "/" + flowToDelete.lobName + "/" + flowToDelete.name, req)
      .then(response => {
        this.setState({flowToDelete: null})
        this.reloadLob(this.state.country, this.state.lobName);
      })

  }

  closeModal() {
    this.setState({
      flowToDelete: null,
    });
  }
}
export default Util.injectUserProp(LobMonitoringDetail)