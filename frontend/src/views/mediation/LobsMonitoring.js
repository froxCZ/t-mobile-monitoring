import React, {Component} from "react";
import {Link, browserHistory} from "react-router";
import {bindActionCreators} from "redux";
import {connect} from "react-redux";
import {showLoading, hideLoading} from "react-redux-loading-bar";
import Api from "../../Api";
import Util from "../../Util";
import StatusBadge from "../../components/StatusBadge";
import StatusCounterBadge from "../../components/StatusCounterBadge";
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

function mapStateToProps(state) {
  return {user: state.auth.user};
}
function mapDispatchToProps(dispatch) {
  var actions = {showLoading: showLoading, hideLoading: hideLoading};
  return bindActionCreators(actions, dispatch);
}
class LobsMonitoring extends Component {
  constructor() {
    super();
    this.state = {countryEnabled: null}
    this.closeModal = this.closeModal.bind(this);

  }

  propChange(props) {
    let country = props.params.country;
    if (country != this.state.country) {
      this.reloadData(country)
    }
  }

  reloadData(country) {
    this.setState({country: country});
    Api.fetch("/mediation/flows/" + country + "/enable", {method: 'GET'}).then((response) => {
      this.setState({countryEnabled: response.enabled});
    });
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

  countryEnableChange(enabled) {
    let body = {enable: enabled}
    var req = {
      method: 'PUT',
      body: body
    };
    Api.fetch("/mediation/flows/" + this.state.country + "/enable", req)
      .then(lobOptionsResponse => {
        this.reloadData(this.state.country)
      });
  }

  lobEnableChange(enabled, lob) {
    let body = {enable: enabled}
    var req = {
      method: 'PUT',
      body: body
    };
    Api.fetch("/mediation/flows/" + lob.country + "/" + lob.name + "/enable", req)
      .then(lobOptionsResponse => {
        let changedLob = {...lob, options: lobOptionsResponse}
        let newLobs = {...this.state.lobs, [lob.name]: changedLob}
        this.setState({lobs: newLobs})
      });

  }

  render() {
    this.isRoot = Util.isRoot(this.props.user);
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
          <tr >
            <td>
              <Link to={this.props.location.pathname + '/' + lobName} className="nav-link" activeClassName="active">
                {lobName}
              </Link>
            </td>
            <td>
              {flowStatuses}
            </td>
            <td>
              <h4>{statusSpan}</h4>
            </td>
            <td>
              {this.isRoot && <label className="switch switch-3d switch-primary"
                                     onClick={(e) => e.stopPropagation()}>
                <input type="checkbox" className="switch-input"
                       checked={lob.options.enabled}
                       onChange={(e) => {
                         this.lobEnableChange(e.target.checked, lob)
                       }}
                />
                <span className="switch-label"></span>
                <span className="switch-handle"></span>
              </label>
              }
            </td>
            <td>
              {this.isRoot &&
              <i className="icon-trash icons font-2xl d-block" style={{cursor: 'pointer'}}
                 onClick={() => this.setState({lobToDelete: lob})}></i>
              }
            </td>
          </tr>)
      }
    }
    if (this.isRoot) {
      if (this.props.params) {
        lobRows.push(<tr>
            <td>
              <input type="text"
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
    }
    return (
      <div className="animated fadeIn">
        {this.createDeleteModal()}
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
                    <th>Enabled<br/><label className="switch switch-3d switch-primary"
                                           onClick={(e) => e.stopPropagation()}>
                      <input type="checkbox" className="switch-input"
                             checked={this.state.countryEnabled}
                             onChange={(e) => {
                               this.countryEnableChange(e.target.checked)
                             }}
                      />
                      <span className="switch-label"></span>
                      <span className="switch-handle"></span>
                    </label></th>
                    <th>Delete</th>
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

  createDeleteModal() {
    if (!this.state.lobToDelete) {
      return <div></div>
    }
    let lobToDelete = this.state.lobToDelete;
    return <Modal isOpen={lobToDelete != null}
                  toggle={this.closeModal} className={'modal-primary ' + this.props.className}>
      <ModalHeader toggle={this.closeModal}>Delete Lob</ModalHeader>
      <ModalBody>
        Do you want to delete lob {lobToDelete.name}?
      </ModalBody>
      <ModalFooter>
        <Button color="danger" onClick={() => this.deleteFlow(lobToDelete)}>Delete</Button>{' '}
        <Button color="secondary" onClick={this.closeModal}>Cancel</Button>
      </ModalFooter>
    </Modal>
  }

  addLob() {
    let country = this.props.params.country;
    let lobName = this.refs.newLobName.value;
    if (lobName == null || lobName.length == 0)return;
    let req = {
      method: "POST",
      body: {country: country, lobName: lobName}
    }
    Api.fetch("/mediation/flows/", req).then(response => {
      this.reloadData(this.props.params.country);
    })

  }

  deleteFlow(lobToDelete) {
    let req = {
      method: "DELETE"
    };
    Api.fetch("/mediation/flows/" + lobToDelete.country + "/" + lobToDelete.name, req)
      .then(response => {
        this.setState({lobToDelete: null})
        this.reloadData(this.state.country);
      })

  }

  closeModal() {
    this.setState({
      lobToDelete: null,
    });
  }
}

LobsMonitoring = connect(mapStateToProps, mapDispatchToProps)(LobsMonitoring)
export default LobsMonitoring