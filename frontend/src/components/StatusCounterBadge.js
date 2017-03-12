import React, {Component} from "react";

export default class StatusCounterBadge extends Component {
  constructor() {
    super();
    this.state = {statuses: null}
  }

  componentWillMount() {
    this.propChange(this.props)
  }

  componentWillReceiveProps(nextProps) {
    this.propChange(nextProps)
  }

  propChange(props) {
    this.setState({statuses: props.statuses})
  }

  render() {
    if (!this.state.statuses) {
      return <span></span>
    }
    let statuses = this.state.statuses
    return <div>
    <span style={{minWidth: 3 + "em"}} title="ok"
          className="badge badge-pill badge-success">{statuses.OK}</span>
      &nbsp;
      <span style={{minWidth: 3 + "em"}} title="warning"
            className="badge badge-pill badge-warning">{statuses.WARNING}</span>
      &nbsp;
      <span style={{minWidth: 3 + "em"}} title="outage"
            className="badge badge-pill badge-danger">{statuses.OUTAGE + statuses.N_A}</span>
      &nbsp;
      {statuses.DISABLED > 0 &&
      <span style={{minWidth: 3 + "em"}} title="Disabled"
            className="badge badge-pill badge-default">{statuses.DISABLED}</span>
      }
    </div>
  }
}
