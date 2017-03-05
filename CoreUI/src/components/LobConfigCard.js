import React, {Component} from "react";
import "react-datepicker/dist/react-datepicker.css";
import Api from "../Api";
const MINUTE_RANGES = [
  0,
  5,
  10,
  15,
  30,
  60,
  120,
  180,
  240,
  360,
  480,
  720,
  1440
];
export default class LobConfigCard extends Component {
  constructor() {
    super()
    this.state = {}

  }

  apply() {

  }

  componentWillMount() {
    this.propChange(this.props)
  }

  componentWillReceiveProps(nextProps) {
    this.propChange(nextProps)
  }

  propChange(props) {
    this.setState({flow: props.flow})
  }


  saveConfig() {
    let lobDataPath;
    if (this.props.flowType == "both") {
      lobDataPath = ".";
    } else {
      lobDataPath = this.props.flowType + "." + this.props.flowName + ".";
    }

    let updateObj = {};
    for (let attribute in this.state.flow) {
      updateObj[lobDataPath + attribute] = this.state.flow[attribute]
    }
    Api.updateLobConfig(this.props.lobName, updateObj).then(res => {

    })
  }

  render() {
    return (<div>{this.renderConfig()}</div>)
  }

  renderConfig() {
    let lobInfo = null;
    if (this.state.flow) {
      lobInfo =
        <div className="row">
          <div className="form-group col-sm-2">
            <label htmlFor="ccmonth">Granularity</label>
            <select className="form-control" id="ccmonth"
                    defaultValue={this.state.flow.granularity}
                    onChange={(e) => {
                      this.props.onChange();
                      this.setState({
                        flow: Object.assign(this.state.flow, {granularity: Number(e.target.value)})
                      })
                    }}>
              {MINUTE_RANGES.map(function (minuteRange) {
                return <option>{minuteRange}</option>
              })
              }
            </select>
          </div>
          <div className="form-group col-sm-2">
            <label htmlFor="fromDate">Soft Level</label>
            <input className="form-control" type="text" defaultValue={this.state.flow.softAlarmLevel}
                   onChange={(e) => {
                     this.props.onChange();
                     this.setState({
                       flow: Object.assign(this.state.flow, {softAlarmLevel: Number(e.target.value)})
                     })
                   }}/>
          </div>
          <div className="form-group col-sm-2">
            <label htmlFor="fromDate">Hard level</label>
            <input className="form-control" type="text" defaultValue={this.state.flow.hardAlarmLevel}
                   onChange={(e) => {
                     this.props.onChange();
                     this.setState({
                       flow: Object.assign(this.state.flow, {hardAlarmLevel: Number(e.target.value)})
                     })
                   }}/>
          </div>
          <div className="form-group col-sm-2">
            <label>&nbsp;</label>
            <div style={{display: "block"}}>
              <button type="button" className="btn btn-primary" onClick={
                () => {
                  this.saveConfig()
                }}>Save
              </button>
            </div>
          </div>
        </div>
    } else {
      lobInfo = <div>loading...</div>
    }
    return lobInfo;
  }

}