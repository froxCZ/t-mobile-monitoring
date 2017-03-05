import React, {Component} from "react";
import Api from "../../Api";
import ChatControl from "../../components/ChartControl";
import "react-datepicker/dist/react-datepicker.css";
import LobChart from "../../components/LobChart";
import LobConfigCard from "../../components/LobConfigCard";
const MINUTE_RANGES = [
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
]

export default class LobMonitoringDetailForward extends Component {
  constructor() {
    super()
    this.state = {data: [], metadata: {}};

  }

  componentWillMount() {
    this.propChange(this.props)
  }

  componentWillReceiveProps(nextProps) {
    this.propChange(nextProps)
  }

  propChange(props) {
    let lobName = props.params.lobName;
    let flowType = null;
    let flowName = null;
    let inputs = []
    let forwards = []
    if (this.props.params.forwardName) {
      flowType = "forwards"
      flowName = props.params.forwardName;
      forwards.push(flowName)
    } else {
      flowType = "inputs"
      flowName = props.params.neidName;
      inputs.push(flowName)
    }
    if (this.state.lobName != lobName || this.state.flowName != flowName) {
      this.setState({lobName: lobName, flowName: flowName, flowType: flowType, inputs: inputs, forwards: forwards});
      Api.fetch("/lobs/" + lobName, {method: 'GET'}).then((response) => {
        this.setState({lob: response, flow: response[flowType][flowName], flowName: flowName});
      });
    }
  }

  loadData(controlSettings) {
    this.setState({controlSettings: controlSettings});
    Api.lobData(
      controlSettings.fromDate,
      controlSettings.toDate,
      this.state.lobName,
      this.state.neids,
      this.state.forwards,
      controlSettings.granularity)
      .then(response => {
        this.setState({data: response.data, metadata: response.metadata})
      })
  }

  render() {
    return (
      <div className="animated fadeIn">
        <div className="row">
          <div className="col-lg-12">
            <h2>{this.state.lobName} - {this.state.flowName}</h2>
          </div>
        </div>
        <div className="row">
          <div className="col-sm-6">
            <div className="card">
              <div className="card-header">
                Config
              </div>
              <div className="card-block">
                <LobConfigCard flow={this.state.flow}
                               lobName={this.state.lobName}
                               flowType={this.state.flowType}
                               flowName={this.state.flowName}
                               onChange={() => this.forceUpdate()}
                />
              </div>
            </div>
          </div>
          <div className="col-sm-6">
            <div className="card">
              <div className="card-header">
                Chart controls
              </div>
              <div className="card-block">
                <ChatControl onApply={this.loadData.bind(this)}/>
              </div>
            </div>
          </div>

        </div>
        <div className="row">
          <div className="col-lg-6">
            <div className="card">
              <div className="card-header">
                Traffic difference
              </div>
              {this.state.flow &&
              <LobChart data={this.state.data} metrics={this.state.metadata.metrics}
                        difference={true}
                        softAlarmLevel={this.state.flow.softAlarmLevel}
                        hardAlarmLevel={this.state.flow.hardAlarmLevel}/>
              }
            </div>
          </div>
          <div className="col-lg-6">
            <div className="card">
              <div className="card-header">
                Traffic
              </div>
              <LobChart data={this.state.data} metrics={this.state.metadata.metrics}/>
            </div>
          </div>
        </div>


      </div>

    )
  }
}