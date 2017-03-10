import React, {Component} from "react";
import Api from "../../Api";
import ChatControl from "../../components/ChartControl";
import "react-datepicker/dist/react-datepicker.css";
import LobChart from "../../components/LobChart";
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
        //todolet flow= response[flowType][flowName]
        this.setState({
          lob: response,
          options: response[flowType][flowName].options,
          flow: response[flowType][flowName],
          flowName: flowName,
          optionsString: JSON.stringify(response[flowType][flowName].options, null, 2)
        });
      });
    }
  }

  loadData(controlSettings) {
    this.setState({controlSettings: controlSettings});
    Api.lobData(
      controlSettings.fromDate,
      controlSettings.toDate,
      this.state.lobName,
      this.state.inputs,
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
                {this.renderOptions()}
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
              {this.state.options &&
              <LobChart data={this.state.data} metrics={this.state.metadata.metrics}
                        difference={true}
                        softAlarmLevel={this.state.options.softAlarmLevel}
                        hardAlarmLevel={this.state.options.hardAlarmLevel}/>
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

  isValidJson(str) {
    try {
      JSON.parse(str);
    } catch (e) {
      return false;
    }
    return true;
  }

  renderOptions() {
    let isValidJson = this.isValidJson(this.state.optionsString)
    let buttonText = isValidJson ? "Save" : "Invalid JSON"
    return (

      <div className="col-md-5">
                <textarea id="textarea-input"
                          name="textarea-input"
                          rows="5"
                          className="form-control" value={this.state.optionsString}
                          onChange={(e) => {
                            let state = {optionsString: e.target.value}
                            try {
                              state.options = JSON.parse(e.target.value);
                            } catch (e) {
                            }
                            this.setState(state)
                          }}
                />
        <div style={{display: "block"}}>
          <button type="button"
                  className="btn btn-primary"
                  disabled={!isValidJson}
                  onClick={
                    () => {
                      this.saveOptions()
                    }}>{buttonText}
          </button>
        </div>

      </div>)
  }

  saveOptions() {
    if (!this.isValidJson(this.state.optionsString)) {
      return
    }
    let myInit = {
      method: 'PUT',
      body: this.state.optionsString
    };
    Api.fetch("/lobs/" + this.state.lobName +
      "/flow/" + this.state.flow.name, myInit).then(response => {
      this.setState({
        options: response,
        optionsString: JSON.stringify(response, null, 2)
      })
    })
  }
}