import React, {Component} from "react";
import {Button, Modal, ModalHeader, ModalBody, ModalFooter} from "reactstrap";
import Api from "../../Api";
export default class UsersList extends Component {
  constructor() {
    super();
    this.state = {users: []}
  }

  componentWillMount() {
    this.getUsers()
  }

  getUsers() {
    Api.fetch("/app/users", {method: "GET"}).then(response => {
      this.setState({users: response})
    })
  }

  render() {
    let rows = []
    for (let user of this.state.users) {
      rows.push(<tr>
        <td>{user._id}</td>
        <td>{user.name}</td>
        <td>{user.permission}</td>
        <td>{user.accountType}</td>
        <td>{user.apiKey}</td>
        <td>
          <i className="icon-trash icons font-2xl" style={{cursor: 'pointer'}}
             onClick={() => {
             }}></i>
          <i className="icon-pencil icons font-2xl" style={{cursor: 'pointer'}}
             onClick={() => {
             }}></i>
        </td>
      </tr>)
    }
    return (
      <div className="animated fadeIn">
        <Modal isOpen={true} toggle={this.togglePrimary} className={'modal-primary ' + this.props.className}>
          <ModalHeader toggle={this.togglePrimary}>User</ModalHeader>
          <ModalBody>

          </ModalBody>
          <ModalFooter>
            <Button color="primary" onClick={this.togglePrimary}>Save</Button>{' '}
            <Button color="secondary" onClick={this.togglePrimary}>Cancel</Button>
          </ModalFooter>
        </Modal>

        <div className="row">
          <div className="col-lg-6">
            <div className="card">
              <div className="card-header">
                <i className="fa fa-align-justify"></i> Users list
              </div>
              <div className="card-block">
                <table className="table">
                  <thead>
                  <tr>
                    <th>Login</th>
                    <th>Name</th>
                    <th>Permission</th>
                    <th>Type</th>
                    <th>Api Key</th>
                    <th>Actions</th>
                  </tr>
                  </thead>
                  <tbody>
                  {rows}
                  {<tr>
                    <button type="button" className="btn btn-primary active" onClick={() => {}}>Add</button>
                  </tr>}
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