import React, {Component} from "react";
import Api from "../../Api";
import Util from "../../Util";
import ChatControl from "../../components/ChartControl";
import "react-datepicker/dist/react-datepicker.css";
import LobChart from "../../components/LobChart";
import StatusBadge from "../../components/StatusBadge";
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

class FlowMonitoring extends Component {
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
    let country = props.params.country;
    let lobName = props.params.lobName;
    let flowName = props.params.flowName;

    if (this.state.lobName != lobName || this.state.flowName != flowName) {
      this.setState({
        lobName: lobName,
        flowName: flowName,
        country: country,
        status: null
      });
      Api.fetch("/mediation/flows/" + country + "/" + lobName + "/" + flowName, {method: 'GET'}).then((response) => {
        this.setState({
          options: response.options,
          flow: response,
          flowName: response.name,
          optionsString: JSON.stringify(response.options, null, 2)
        });
        let controlSettings = {};
        let from = Util.getCurrentTime().subtract(7, 'days');
        let to = Util.getCurrentTime().add(7, 'days');
        controlSettings.fromDate = from.format("DD.MM.YYYY");
        controlSettings.toDate = to.format("DD.MM.YYYY");
        controlSettings.granularity = 0;
        this.loadData(controlSettings)
      });
    }
  }

  loadData(controlSettings) {
    this.setState({controlSettings: controlSettings});
    let flowObj = {inputs: [], forwards: []};
    flowObj[this.state.flow.type].push(this.state.flow.name);
    let lobReq = {country: this.state.country, name: this.state.lobName}
    Api.lobData(
      controlSettings.fromDate,
      controlSettings.toDate,
      lobReq,
      flowObj.inputs,
      flowObj.forwards,
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
            <h2>{this.state.lobName} - {this.state.flowName} {this.state.flow &&
            <StatusBadge status={this.state.flow.status.status}/>}</h2>

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
              <LobChart data={this.state.data}
                        metrics={this.state.metadata.metrics}
                        flowName={this.state.metadata.flowName}/>
            </div>
          </div>
        </div>

        <div className="row">

          <div className="col-sm-6">
            <div className="card">

              <div className="card-block">
                <ChatControl ref="chartControl" onApply={this.loadData.bind(this)}/>
              </div>
            </div>
          </div>
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
    console.log(this.props)
    let isValidJson = this.isValidJson(this.state.optionsString)
    let buttonText = isValidJson ? "Save" : "Invalid JSON"
    return (

      <div className="col-md-5">
                <textarea id="textarea-input"
                          name="textarea-input"
                          rows="10"
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
        {Util.isRoot(this.props.user) &&
        <div style={{display: "block"}}>
          <button type="button"
                  className="btn btn-primary"
                  disabled={!isValidJson}
                  onClick={
                    () => {
                      this.saveOptions()
                    }}>{buttonText}
          </button>
          &nbsp;
          <button type="button"
                  className="btn btn-primary"
                  onClick={
                    () => {
                      this.resetStatus()
                    }}>Reset status
          </button>
        </div>
        }

      </div>)
  }

  resetStatus() {
    let myInit = {
      method: 'PUT'
    };
    Api.fetch("/mediation/flows/" + this.state.country + "/" + this.state.lobName +
      "/" + this.state.flow.name + "/resetStatus", myInit).then(response => {
      this.setState({
        options: response.options,
        flow: response,
        flowName: response.name,
        optionsString: JSON.stringify(response.options, null, 2)
      });
    })
  }

  saveOptions() {
    if (!this.isValidJson(this.state.optionsString)) {
      return
    }
    let myInit = {
      method: 'PUT',
      body: this.state.optionsString
    };
    Api.fetch("/mediation/flows/" + this.state.country + "/" + this.state.lobName +
      "/" + this.state.flow.name + "/options", myInit).then(response => {
      this.setState({
        options: response,
        optionsString: JSON.stringify(response, null, 2)
      })
    })
  }
}

export default Util.injectUserProp(FlowMonitoring)