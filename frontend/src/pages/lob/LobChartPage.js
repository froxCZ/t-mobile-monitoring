import React, {Component, PropTypes} from "react";
import {bindActionCreators} from "redux";
import {connect} from "react-redux";
import PageHeader from "react-bootstrap/lib/PageHeader";
import Button from "react-bootstrap/lib/Button";
import Checkbox from "react-bootstrap/lib/Checkbox";
import FormControl from "react-bootstrap/lib/FormControl";
import ControlLabel from "react-bootstrap/lib/ControlLabel";
import FormGroup from "react-bootstrap/lib/FormGroup";
import {performFetchPromise} from "../../actions/ApiRequest";
import {showLoading, hideLoading} from "react-redux-loading-bar";
import {LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend} from "recharts";
import MetricGraph from "../../components/MetricGraph";
import {Typeahead} from "react-bootstrap-typeahead";
import "react-bootstrap-typeahead/css/Typeahead.css";
import "react-bootstrap-typeahead/css/ClearButton.css";
import "react-bootstrap-typeahead/css/Loader.css";
import "react-bootstrap-typeahead/css/Token.css";
import DatePicker from "react-bootstrap-date-picker";
import _ from "lodash"; // Expects that Highcharts was loaded in the code.
// ES2015
// ES2015

const LOCAL_STORAGE = "lobChartPage";

function mapStateToProps(state) {
  return {auth: state.auth};
}
function mapDispatchToProps(dispatch) {
  var actions = {showLoading: showLoading, hideLoading: hideLoading};
  return bindActionCreators(actions, dispatch);
}
class LobChartPage extends Component {

  constructor() {
    super();
    if (localStorage.getItem(LOCAL_STORAGE)) {
      this.state = JSON.parse(localStorage.getItem(LOCAL_STORAGE) || "{}");
    } else {
      this.state = {interpolate: true}
    }
  }

  componentWillMount() {
    this.loadConfig();
  }

  loadConfig() {
    this.props.showLoading();
    var that = this;
    performFetchPromise("/analyser/lobs/configs", {method: 'GET'}).then(result => {
      result.minuteRanges.unshift(0);
      let lobs = {}
      for (let country in result.lobs) {
        for (let lob in result.lobs[country]) {
          lobs[country + "." + lob] = result.lobs[country][lob];
        }
      }
      that.setState({lobs: lobs, minuteRanges: result.minuteRanges});
      that.props.hideLoading();
    })
  }

  updateLobConfig(lobName, newData) {
    var myInit = {
      method: 'POST',
      body: newData
    };
    var that = this;
    this.props.showLoading();
    performFetchPromise("/analyser/lobs/config/" + lobName, myInit).finally(result => {
      that.props.hideLoading();
      that.loadConfig();
    })
  }

  loadData() {
    var myInit = {
      method: 'POST',
      body: {
        "from": this.state.from,
        "to": this.state.to,
        "aggregation": {
          "sum": this.state.selectedLobs
        },
        "granularity": this.state.granularity || 0
      }
    };
    var that = this;
    this.props.showLoading();
    performFetchPromise("/analyser/data_query/", myInit).then(result => {
      that.setState({response: result});
    }).catch(result => {
      this.setState({response: null})
    }).then(x => {
      that.props.hideLoading();
    });
  }

  componentDidUpdate() {
    localStorage.setItem(LOCAL_STORAGE, JSON.stringify(_.pick(this.state, ['from', 'to', 'selectedLobs'])));
  }


  render() {
    let lobNames = null;
    console.log(this.state)
    if (this.state.lobs) {
      lobNames = [];
      for (let lobName in this.state.lobs) {
        lobNames.push(lobName);
      }
    }
    let metrics = null;
    let realMetricName = null
    let usedGranularity = null
    if (this.state.response) {
      metrics = [];
      for (let metric in this.state.response.metadata.metrics) {
        metrics.push(metric);
      }
      realMetricName = metrics[0].replace("_", ".");
      usedGranularity = this.state.response.metadata.granularity;
    }
    return <div>

      <PageHeader>DataFlow</PageHeader>
      {
        lobNames &&
        <div>
          <div className="row">
            <div className="col-xs-3">
              <label>Lob:</label>
              <Typeahead
                onChange={(selected) => this.setState({selectedLobs: selected})}
                //multiple={true}
                options={lobNames}
                selected={this.state.selectedLobs}
              />
            </div>
            <div className="col-xs-3 datePicker">
              <label>From:</label>
              <DatePicker value={this.state.from} dateFormat="DD.MM.YYYY"
                          onChange={(val) => this.setState({from: val})}/>
            </div>
            <div className="col-xs-3 datePicker">
              <label>To:</label>
              <DatePicker value={this.state.to} dateFormat="DD.MM.YYYY" onChange={(val) => this.setState({to: val})}/>
            </div>
            <div className="col-xs-3">
              <label>Interpolate:</label>
              <Checkbox onChange={(e) => this.setState({interpolate: e.target.checked})}
                        checked={this.state.interpolate}>
              </Checkbox>
            </div>
          </div>
          <div className="row">
            <div className="col-xs-1">
              <FormGroup controlId="formControlsSelect">
                <ControlLabel>Granularity</ControlLabel>
                <FormControl bsSize="xsmall" componentClass="select" placeholder="select"
                             onChange={e => this.setState({granularity: e.target.value})}
                             value={this.state.granularity}>
                  {
                    this.state.minuteRanges.map((a) => <option value={a}>{a}</option>)
                  }
                </FormControl>
              </FormGroup>

            </div>
          </div>
          <div className="row">
            <div className="col-lg-3">
              <Button onClick={this.loadData.bind(this)}>Apply</Button>
            </div>
          </div>
        </div>
      }


      <div className="col-lg-6">
        { this.state.response &&
        <div>
          <h2>{realMetricName}</h2>
          <div className="row">
            <div className="col-lg-6">
              Minimal granularity: {this.state.lobs[realMetricName].granularity}
              <br/>
              Granularity: {usedGranularity} minutes
              <Button bsSize="xsmall" bsStyle="warning"
                      onClick={() => this.updateLobConfig(realMetricName, {granularity: usedGranularity})}>Set as
                minimal</Button>
            </div>
          </div>
          <MetricGraph source={this.state.response} metrics={metrics} relative={false}
                       interpolate={this.state.interpolate}/>
        </div>
        }
      </div>

      <div className="row ng-scope">

      </div>
    </div>
  }
}
LobChartPage = connect(mapStateToProps, mapDispatchToProps)(LobChartPage)
export default LobChartPage