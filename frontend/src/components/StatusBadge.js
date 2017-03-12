import React, {Component} from "react";

const STATUS_MAP = {
  "OK": {
    class: "badge-success",
    label: "ok"
  },
  "WARNING": {
    class: "badge-warning",
    label: "warning"
  },
  "OUTAGE": {
    class: "badge-danger",
    label: "outage"
  },
  "N_A": {
    class: "badge-danger",
    label: "n/a"
  },
  "DISABLED": {
    class: "badge-default",
    label: "disabled"
  },
}
export default class StatusBadge extends Component {
  constructor() {
    super();
    this.state = {status: null}
  }

  componentWillMount() {
    this.propChange(this.props)
  }

  componentWillReceiveProps(nextProps) {
    this.propChange(nextProps)
  }

  propChange(props) {
    if (props.status != this.state.status) {
      this.setState({status: props.status})
    }
  }

  render() {
    if (!this.state.status) {
      return <span></span>
    }
    let statusProps = STATUS_MAP[this.state.status]
    return <span className={"badge " + statusProps.class} style={this.props.style}>{statusProps.label}</span>
  }

}