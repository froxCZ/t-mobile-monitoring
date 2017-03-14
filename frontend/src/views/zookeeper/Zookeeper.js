import React, {Component} from "react";
import Api from "../../Api";
export default class Zookeeper extends Component {

  constructor() {
    super()
    this.state = {}
  }

  componentWillMount() {
    Api.fetch("/zookeeper/cluster", {method: "GET"}).then(response => {
      this.setState({cluster: response})
    })
  }

  removeNode(socketAddress) {
    let req = {
      method: "DELETE"
    };
    Api.fetch("/zookeeper/node/" + socketAddress, req).then(response => {
      this.setState({cluster: response})
    })
  }

  addNode() {
    let socketAddress = this.refs.inputSocketAddress.value
    let req = {
      method: "POST",
      body: {}
    };
    Api.fetch("/zookeeper/node/" + socketAddress, req).then(response => {
      this.setState({cluster: response})
    })
  }

  monitoringEnabledChange(shouldEnable) {
    let path = null
    if (shouldEnable) {
      path = "enable"
    } else {
      path = "disable"
    }
    Api.fetch("/zookeeper/cluster/" + path, {method: "POST"}).then(response => {
      this.setState({cluster: response})
    })
  }

  render() {
    if (!this.state.cluster) {
      return <p></p>
    }
    let rows = []
    if (this.state.cluster) {
      for (let socket in this.state.cluster.nodes) {
        let instance = this.state.cluster.nodes[socket]
        let mode = "unknown"
        if (this.state.status) {
          let nodeStatus = this.state.status.nodes[socket]
          if (nodeStatus) {
            mode = nodeStatus.mode
          }
        }
        rows.push(
          <tr>
            <td>{socket}</td>
            <td>{mode}</td>
            <td>
              <span className="badge badge-success">OK</span>
            </td>
            <td><i className="icon-trash icons font-2xl d-block" style={{cursor: 'pointer'}}
                   onClick={() => this.removeNode(socket)}></i></td>
          </tr>)
      }

      rows.push(<tr>
        <td>
          <input type="text"
                 id="text-input"
                 name="text-input"
                 className="form-control col-lg-6"
                 style={{display: "inline"}}
                 ref="inputSocketAddress"
                 placeholder="Text"/>
          &nbsp;
          <button type="button" className="btn btn-primary active" onClick={() => this.addNode()}>Add</button>
        </td>
        <td></td>
        <td></td>
        <td></td>

      </tr>)
    }

    return (
      <div className="animated fadeIn">
        <div className="row">
          <div className="col-lg-6">
            <div className="card">
              <div className="card-header">
                <i className="fa fa-align-justify"></i> Monitorig
              </div>
              <div className="card-block">
                enabled:<label className="switch switch-3d switch-primary" onClick={(e) => e.stopPropagation()}>
                <input type="checkbox" className="switch-input"
                       checked={this.state.cluster.enabled}
                       onChange={(e) => {
                         this.monitoringEnabledChange(e.target.checked)
                       }}
                />
                <span className="switch-label"></span>
                <span className="switch-handle"></span>
              </label>
                <br/>
                status:asd<br/>

              </div>
            </div>
          </div>

        </div>
        <div className="row">
          <div className="col-lg-6">
            <div className="card">
              <div className="card-header">
                <i className="fa fa-align-justify"></i> Cluster Configuration
              </div>
              <div className="card-block">
                <table className="table">
                  <thead>
                  <tr>
                    <th>Socket address</th>
                    <th>Mode</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                  </thead>
                  <tbody>
                  {rows}
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