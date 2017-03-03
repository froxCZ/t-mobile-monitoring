import React, {Component} from "react";

export default class UsersList extends Component {
  SettingsUsers() {

  }

  render() {
    return (
      <div className="animated fadeIn">

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
                    <th>Actions</th>
                  </tr>
                  </thead>
                  <tbody>
                  <tr>
                    <td>vojta</td>
                    <td>Vojta Udržal</td>
                    <td>e e e </td>
                  </tr>
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