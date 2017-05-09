import React, {Component} from "react";
import {Button, Modal, ModalHeader, ModalBody, ModalFooter} from "reactstrap";
import Api from "../../Api";
import StatusBadge from "../../components/StatusBadge";

const DEFAULT_USER = {
  accountType: "user",
  permission: "readOnly",
  isNew: true
};
export default class UsersList extends Component {
  constructor() {
    super();
    this.state = {};

  }

  componentWillMount() {
    this.fetchStatusInterval = setInterval(this.fetchStatus.bind(this), 3000);
    this.fetchStatus();
  }

  componentWillUnmount() {
    clearInterval(this.fetchStatusInterval)
  }

  fetchStatus() {
    Api.fetch("/app/status", {method: "GET"}).then(response => {
      this.setState({status: response})
    })
  }


  render() {
    let rows = []
    console.log(this.state);
    if (this.state.status) {
      rows = [...rows,this.getComponentRows("executors")];
      rows = [...rows,this.getComponentRows("kafka")];
    }

    return <div className="animated fadeIn">
      <div className="row">
        <div className="col-lg-12">
          <h2>System status</h2>
        </div>
      </div>
      <div className="row">
        <div className="col-lg-12">
          <div className="card">
            <div className="card-header">
              <i className="fa fa-align-justify"></i> Components list
            </div>
            <div className="card-block">
              <table className="table">
                <thead>
                <tr>
                  <th>Name</th>
                  <th>Type</th>
                  <th>Status</th>
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
  }

  getComponentRows(type) {
    let rows = [];
    let components = this.state.status[type];
    for (let componentName in components) {
      let status = components[componentName];
      rows.push(
        <tr>
          <td>
            {componentName}
          </td>
          <td>{type}</td>
          <td><h5><StatusBadge status={status}/></h5></td>
        </tr>)
    }
    console.log(rows)
    return rows;
  }
}