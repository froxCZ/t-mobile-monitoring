import React, {Component} from "react";
import Api from "../Api";
import ChatControl from "./ChartControl";
import "react-datepicker/dist/react-datepicker.css";
import LobChart from "./LobChart";
const MINUTE_RANGES = [
  5,
  10,
  15,
  30,
  60,
  120,
  180,
  240,
  480,
  720,
  1440
]
export default class LobOverviewCharts extends Component {
  constructor() {
    super()
    this.state = {inputs: {metadata: {}}, forwards: {metadata: {}}};

  }

  componentWillMount() {
    this.propChange(this.props)
  }

  componentWillReceiveProps(nextProps) {
    this.propChange(nextProps)
  }

  propChange(props) {
    let lobName = props.lobName;
    let metricName = props.metricName;
    if (this.state.lobName != lobName || this.state.metricName != metricName) {
      this.setState({lobName: lobName, metricName: metricName,lob: this.props.lob});
    }
  }

  loadData(controlSettings) {
    Api.lobData(
      controlSettings.fromDate,
      controlSettings.toDate,
      this.state.lobName, ["*"], [],
      controlSettings.granularity)
      .then(response => {
        this.setState({inputs: response})
      })
    Api.lobData(
      controlSettings.fromDate,
      controlSettings.toDate,
      this.state.lobName, [], ["*"],
      controlSettings.granularity)
      .then(response => {
        this.setState({forwards: response})
      })
  }

  render() {
    return (
      <div className="animated fadeIn">
        <div className="row">
          <div className="col-lg-12">
            <h2>{this.state.lobName} - {this.state.metricName}</h2>
          </div>
        </div>
        <div className="row">
          <div className="col-sm-6">
            <div className="card">
              <div className="card-block">
                <ChatControl onApply={this.loadData.bind(this)}/>
              </div>
            </div>

          </div>
        </div>
        {this.state.inputs.data
        &&
        <div className="row">
          <div className="col-lg-3">
            <div className="card">
              <div className="card-header">
                Inputs difference
              </div>
              <LobChart data={this.state.inputs.data} metrics={this.state.inputs.metadata.metrics} difference={true}/>
            </div>
          </div>
          <div className="col-lg-3">
            <div className="card">
              <div className="card-header">
                Inputs traffic
              </div>
              <LobChart data={this.state.inputs.data} metrics={this.state.inputs.metadata.metrics}/>
            </div>
          </div>
        </div>
        }
        {this.state.forwards.data
        &&
        <div className="row">
          <div className="col-lg-3">
            <div className="card">
              <div className="card-header">
                Forwards difference
              </div>
              <LobChart data={this.state.forwards.data} metrics={this.state.forwards.metadata.metrics}
                        difference={true}/>
            </div>
          </div>
          <div className="col-lg-3">
            <div className="card">
              <div className="card-header">
                Forwards traffic
              </div>
              <LobChart data={this.state.forwards.data} metrics={this.state.forwards.metadata.metrics}/>
            </div>
          </div>
        </div>
        }
      </div>

    )
  }
}