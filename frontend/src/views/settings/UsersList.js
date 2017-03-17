import React, {Component} from "react";
import {Button, Modal, ModalHeader, ModalBody, ModalFooter} from "reactstrap";
import Api from "../../Api";
import _ from "lodash";

const DEFAULT_USER = {
  accountType: "user",
  permission: "readOnly",
  isNew: true
};
export default class UsersList extends Component {
  constructor() {
    super();
    this.state = {users: [], userToEdit: null, userToDelete: null, accountType: null};
    this.closeModal = this.closeModal.bind(this);
  }

  closeModal() {
    this.setState({
      userToEdit: null,
      userToDelete: null,
    });
  }

  componentWillMount() {
    this.getUsers()
  }

  getUsers() {
    Api.fetch("/app/users", {method: "GET"}).then(response => {
      this.setState({users: response})
    })
  }

  saveUser(isNew) {
    let saveUser = {};
    let refs = this.refs;
    let login = refs.login.value;
    if (isNew) {
      saveUser.login = login
    }
    saveUser.name = refs.name.value;
    saveUser.accountType = refs.accountType.value;
    saveUser.permission = refs.permission.value;
    if (this.refs.generateNewApiKey) {
      saveUser.generateNewApiKey = this.refs.generateNewApiKey.checked;
    }
    if (refs.password) {
      saveUser.password = this.refs.password.value;
    }
    let req = {
      method: isNew ? "POST" : "PUT",
      body: saveUser
    };
    let path = isNew ? "/app/users" : "/app/user/" + login;
    Api.fetch(path, req).then(response => {
      this.setState({users: response, userToEdit: null})
    })

  }

  render() {
    let rows = [];
    for (let user of this.state.users) {
      rows.push(<tr>
        <td>{user.login}</td>
        <td>{user.name}</td>
        <td>{user.accountType}</td>
        <td>{user.apiKey}</td>
        <td>{user.permission}</td>
        <td>
          <i className="icon-pencil icons font-2xl" style={{cursor: 'pointer'}}
             onClick={() => {
               this.setState({userToEdit: user})
             }}></i>
          <i className="icon-trash icons font-2xl" style={{cursor: 'pointer'}}
             onClick={() => {
               this.setState({userToDelete: user})
             }}></i>
        </td>
      </tr>)
    }
    let modal = null;
    if (this.state.userToEdit) {
      let modalUser = this.state.userToEdit;
      modal = this.createEditModal(modalUser)
    } else if (this.state.userToDelete) {
      modal = this.createDeleteModal(this.state.userToDelete)
    }
    return (
      <div className="animated fadeIn">
        {modal}

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
                    <th>Type</th>
                    <th>Api Key</th>
                    <th>Permission</th>
                    <th>Actions</th>
                  </tr>
                  </thead>
                  <tbody>
                  {rows}
                  {<tr>
                    <button type="button" className="btn btn-primary active" onClick={() => {
                      this.setState({userToEdit: _.cloneDeep(DEFAULT_USER)})
                    }}>Add
                    </button>
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

  createEditModal(modalUser) {

    return <Modal isOpen={modalUser != null}
                  toggle={this.closeModal} className={'modal-primary ' + this.props.className}>
      <ModalHeader toggle={this.closeModal}>User</ModalHeader>
      <ModalBody>
        <div className="form-group">
          <label for="vat">Type</label>
          <select id="select" name="select"
                  className="form-control"
                  disabled={!modalUser.isNew}
                  size="1"
                  defaultValue={modalUser.accountType}
                  ref="accountType"
                  onChange={(e) => this.setState({modalUser: this.refs.accountType.value})}
          >
            <option value="user">User</option>
            <option value="app">App</option>
          </select>
        </div>

        <div className="form-group">
          <label>Login*</label>
          <input type="text" className="form-control"
                 disabled={!modalUser.isNew}
                 defaultValue={modalUser.login}
                 ref="login"
          />
        </div>

        <div className="form-group">
          <label for="vat">Name*</label>
          <input type="text" className="form-control"
                 ref="name"
                 defaultValue={modalUser.name} id="vat" placeholder="PL1234567890"/>
        </div>

        {(modalUser.isNew || modalUser.accountType == "user") &&
        <div className="form-group">
          <label for="vat">Password{modalUser.isNew ? "*" : ""}</label>
          <input type="password" id="password-input" name="password-input" className="form-control"
                 defaultValue={modalUser.password}
                 ref="password"
                 placeholder="Password"/>
        </div>
        }

        <div className="form-group">
          <label for="vat">Permission</label>
          <select id="select" name="select" className="form-control" size="1"
                  ref="permission"
                  defaultValue={modalUser.permission}>
            <option value="readOnly">Read only</option>
            <option value="root">root</option>
          </select>
        </div>
        {!modalUser.isNew && modalUser.accountType == "app" &&
        <div className="checkbox">
          <label for="checkbox1">
            <input type="checkbox" id="checkbox1" name="checkbox1" ref="generateNewApiKey"/> Generate New Api key
          </label>
        </div>
        }


      </ModalBody>
      <ModalFooter>
        <Button color="primary" onClick={() => this.saveUser(modalUser.isNew)}>Save</Button>{' '}
        <Button color="secondary" onClick={this.closeModal}>Cancel</Button>
      </ModalFooter>
    </Modal>

  }


  createDeleteModal(userToDelete) {
    return <Modal isOpen={userToDelete != null}
                  toggle={this.closeModal} className={'modal-primary ' + this.props.className}>
      <ModalHeader toggle={this.closeModal}>Delete User</ModalHeader>
      <ModalBody>
        Do you want to delete {userToDelete.login}?
      </ModalBody>
      <ModalFooter>
        <Button color="danger" onClick={() => this.deleteUser(userToDelete)}>Delete</Button>{' '}
        <Button color="secondary" onClick={this.closeModal}>Cancel</Button>
      </ModalFooter>
    </Modal>
  }

  deleteUser(userToDelete) {
    Api.fetch("/app/user/" + userToDelete.login, {method: "DELETE"}).then(response => {
      this.setState({users: response, userToDelete: null})
    })

  }
}