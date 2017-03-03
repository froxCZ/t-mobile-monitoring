import React, {Component} from "react";
import Api from "../../Api";
import ChatControl from "../../components/ChartControl";
import "react-datepicker/dist/react-datepicker.css";

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
export default class LobMonitoringDetailNeid extends Component {
  constructor() {
    super()
    this.state = {};

  }

  componentWillMount() {
    this.propChange(this.props)
  }

  componentWillReceiveProps(nextProps) {
    this.propChange(nextProps)
  }

  propChange(props) {
    let lobName = props.params.lobName;
    let neidName = props.params.neidName;
    if (this.state.lobName != lobName || this.state.neidName != neidName) {
      this.setState({lobName: lobName, neidName: neidName});
      Api.fetch("/lobs/" + lobName, {method: 'GET'}).then((response) => {
        this.setState({lob: response});
      });
    }
  }

  loadData(fromDate, toDate, granularity) {
    Api.lobInputs(fromDate, toDate, this.state.lobName, this.state.neidName, granularity)
      .then(response => {
        console.log(response)
      })
  }

  render() {
    return (
      <div className="animated fadeIn">
        <div className="row">
          <div className="col-lg-12">
            <h2>{this.state.lobName} - {this.state.neidName}</h2>
          </div>
        </div>
        <div className="row">
          <div className="col-sm-6">
            <div className="card">
              <div className="card-header">
                <strong>Chart control</strong>
              </div>
              <div className="card-block">
                <ChatControl onApply={this.loadData.bind(this)}/>
              </div>
            </div>

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