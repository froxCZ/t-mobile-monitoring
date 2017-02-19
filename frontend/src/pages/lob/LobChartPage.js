import React, {Component, PropTypes} from "react";
import {bindActionCreators} from "redux";
import {connect} from "react-redux";
import PageHeader from "react-bootstrap/lib/PageHeader";
import Button from "react-bootstrap/lib/Button";
import Checkbox from "react-bootstrap/lib/Checkbox";
import FormControl from "react-bootstrap/lib/FormControl";
import ControlLabel from "react-bootstrap/lib/ControlLabel";
import FormGroup from "react-bootstrap/lib/FormGroup";
import Pager from "react-bootstrap/lib/Pager";
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
const DATE_RANGE = [1, 7, 14, 28];
class LobChartPage extends Component {

  constructor() {
    super();
    if (localStorage.getItem(LOCAL_STORAGE)) {
      this.state = JSON.parse(localStorage.getItem(LOCAL_STORAGE) || "{}");
    } else {
      this.state = {smooth: true}
    }
    this.state.dateRange = DATE_RANGE[1];
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

  loadLob(lobName) {
    this.setState({selectedLobs: [lobName], granularity: 0});
    this.scheduleReloadData = true;
  }

  componentDidUpdate() {
    localStorage.setItem(LOCAL_STORAGE, JSON.stringify(_.pick(this.state, ['from', 'to', 'selectedLobs'])));
    if (this.scheduleReloadData) {
      this.loadData();
      this.scheduleReloadData = false;
    }
  }


  render() {
    let lobNames = null;
    let metrics = null;
    let shownLobName = null
    let usedGranularity = null
    if (this.state.response) {
      metrics = [];
      for (let metric in this.state.response.metadata.metrics) {
        metrics.push(metric);
      }
      shownLobName = metrics[0].replace("_", ".");
      usedGranularity = this.state.response.metadata.granularity;
    }
    let nextLobName, prevLobName;
    if (this.state.lobs) {
      lobNames = [];
      for (let lobName in this.state.lobs) {
        lobNames.push(lobName);
      }
      for (let i in lobNames) {
        if (lobNames[i] == this.state.selectedLobs[0]) {
          let index = Number(i);
          prevLobName = lobNames[index - 1]
          nextLobName = lobNames[index + 1]
        }
      }
    }
    return <div>

      <PageHeader>DataFlow</PageHeader>
      {
        lobNames &&
        <div>
          <div className="row">
            <div className="col-xs-12">
              <Pager>
                {
                  prevLobName &&
                  <Pager.Item previous onClick={() => this.loadLob(prevLobName)}>&larr; {prevLobName}</Pager.Item>
                }
                {
                  nextLobName &&
                  <Pager.Item next onClick={() => this.loadLob(nextLobName)}>{nextLobName}&rarr;</Pager.Item>
                }
              </Pager>
            </div>
          </div>
          <div className="row">
            <div className="col-xs-2">
              <label>Lob:</label>
              <Typeahead
                onChange={(selected) => this.setState({selectedLobs: selected})}
                //multiple={true}
                options={lobNames}
                selected={this.state.selectedLobs}
              />
            </div>
            <div className="col-xs-2 datePicker">
              <label>From:</label>
              <DatePicker value={this.state.from} dateFormat="DD.MM.YYYY"
                          onChange={(val) => this.setState({from: val})}/>
            </div>
            <div className="col-xs-2 datePicker">
              <label>To:</label>
              <DatePicker value={this.state.to} dateFormat="DD.MM.YYYY" onChange={(val) => this.setState({to: val})}/>
            </div>
            <div className="col-xs-1">
              <label>Date range:</label>
              <FormGroup controlId="formControlsSelect">
                <FormControl bsSize="xsmall" componentClass="select" placeholder="select"
                             onChange={e => {
                               let dateRange = Number(e.target.value)
                               let newToDate = LobChartPage.shiftDateByDays(this.state.from, dateRange);
                               this.setState({to: newToDate.toISOString(), dateRange: dateRange})
                               this.scheduleReloadData = true;
                             }}
                             value={this.state.dateRange}>
                  {
                    DATE_RANGE.map((a) => <option value={a}>{a}</option>)
                  }
                </FormControl>
              </FormGroup>
            </div>
            <div className="col-xs-2">
              <label>Shift:</label>
              <Pager style={{margin: 0}}>
                <Pager.Item previous onClick={() => {
                  let newFrom = LobChartPage.shiftDateByDays(this.state.from, this.state.dateRange * -1)
                  let newTo = LobChartPage.shiftDateByDays(this.state.to, this.state.dateRange * -1)
                  this.setState({from: newFrom.toISOString(), to: newTo.toISOString()});
                  this.scheduleReloadData = true;
                }}>&larr; </Pager.Item>
                <Pager.Item next onClick={() => {
                  let newFrom = LobChartPage.shiftDateByDays(this.state.from, this.state.dateRange * 1)
                  let newTo = LobChartPage.shiftDateByDays(this.state.to, this.state.dateRange * 1)
                  this.setState({from: newFrom.toISOString(), to: newTo.toISOString()});
                  this.scheduleReloadData = true;
                }} style={{float: "left"}}>&rarr;</Pager.Item>
              </Pager>
            </div>

          </div>
          <div className="row">
            <div className="col-sm-2">
              <FormGroup controlId="formControlsSelect">
                <ControlLabel>Granularity</ControlLabel>
                <FormControl bsSize="xsmall" componentClass="select" placeholder="select"
                             onChange={e => {
                               this.setState({granularity: e.target.value});
                               this.scheduleReloadData = true;
                             }}
                             value={this.state.granularity}>
                  {
                    this.state.minuteRanges.map((a) => <option value={a}>{a}</option>)
                  }
                </FormControl>
              </FormGroup>
            </div>
            <div className="col-xs-3">
              <label>Smooth:</label>
              <Checkbox onChange={(e) => this.setState({smooth: e.target.checked})}
                        checked={this.state.smooth}>
              </Checkbox>
            </div>
          </div>
          <div className="row">
            <div className="col-lg-3">
              <Button onClick={this.loadData.bind(this)}>Apply</Button>
            </div>
          </div>
        </div>
      }


      { this.state.response &&
      <div>
        <h2>{shownLobName}</h2>
        <div className="row">
          <div className="col-xs-3">
            Minimal granularity: {this.state.lobs[shownLobName].granularity}
            <br/>
            Granularity: {usedGranularity} minutes &nbsp;
            <Button bsSize="xsmall" bsStyle="warning"
                    onClick={() => this.updateLobConfig(shownLobName, {granularity: usedGranularity})}>Set as
              minimal</Button>
          </div>
        </div>
        <div className="row">
          <div className="col-xs-8">
            <MetricGraph source={this.state.response} metrics={metrics} relative={false}
                         smooth={this.state.smooth}/>
          </div>
        </div>
      </div>
      }

      <div className="row ng-scope">

      </div>
    </div>
  }

  static shiftDateByDays(date, days) {
    let newDate = new Date(date)
    newDate.setDate(newDate.getDate() + Number(days));
    return newDate;
  }
}
LobChartPage = connect(mapStateToProps, mapDispatchToProps)(LobChartPage)
export default LobChartPage