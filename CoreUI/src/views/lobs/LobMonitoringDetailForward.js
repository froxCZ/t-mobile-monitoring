import React, {Component} from "react";

export default class LobMonitoringDetailForward extends Component {
  constructor() {
    super()


  }

  goToForwardDetail(forwardName) {

  }

  render() {
    this.forwardName = this.props.params.forwardName
    return (
      <div className="animated fadeIn">
        <div className="row">
          <div className="col-lg-12">
            <h2>{this.forwardName}</h2>
          </div>
        </div>
        <div className="row">
          <div className="col-lg-12">
            <div className="card">
              <div className="card-header">
                Traffic
              </div>
              chart!
            </div>
          </div>

        </div>
      </div>

    )
  }
}