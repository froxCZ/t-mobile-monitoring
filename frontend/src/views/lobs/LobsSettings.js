import React, {Component} from "react";
import Api from "../../Api";
export default class LobsSettings extends Component {
  LobsSettings() {

  }

  discover() {
    Api.fetch("/lobs/discover", {method: 'GET'}).then(result => {
      console.log(result)
    })

  }

  render() {
    return (
      <div className="animated fadeIn">
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
                    <th>Traffic Level</th>
                    <th>Forwardings</th>
                    <th>Status</th>
                  </tr>
                  </thead>
                  <tbody>
                  <tr>
                    <td>CZ.SMS</td>
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