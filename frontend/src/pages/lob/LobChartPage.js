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
import Spinner from "react-spinkit";
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
    this.state.averages = null;
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
    this.setState({loadingLobData: true, loadingCorrelations: true})
    this.props.showLoading();
    performFetchPromise("/analyser/data_query/", myInit).then(result => {
      that.setState({response: result});
      //this.loadCorrelations();
      //this.loadAverages();
      //this.loadDayMedian();
    }).catch(result => {
      this.setState({response: null})
    }).finally(x => {
      that.props.hideLoading();
      this.setState({loadingLobData: false})
    });
  }

  loadDayMedian() {
    var myInit = {
      method: 'GET',
    };
    let that = this;
    performFetchPromise("/analyser/data_query/day_medians?lobName=" +
      this.state.selectedLobs[0] +
      "&date=" + this.state.from, myInit)
      .then(result => {
        that.setState({medians: result})
        console.log(result)
      })
      .finally(r => {
      })

  }

  loadAverages() {
    var myInit = {
      method: 'GET',
    };
    this.setState({averages: null})
    this.setState({loadingAverages: true})
    let that = this;
    performFetchPromise("/analyser/data_query/averages?lobName=" +
      this.state.selectedLobs[0], myInit)
      .then(result => {
        that.setState({averages: result})
        console.log(result)
        console.log("x")
      })
      .finally(r => {
        console.log("f")
        that.setState({loadingAverages: false})
      })
  }

  loadCorrelations() {
    var myInit = {
      method: 'GET',
    };
    this.setState({correlations: null})
    this.setState({loadingCorrelations: true})
    let that = this;
    performFetchPromise("/analyser/data_query/best_correlations?" +
      "lobName=" + this.state.selectedLobs[0] +
      "&granularity=" + that.state.response.metadata.granularity, myInit).then(result => {
      let best4 = result.slice(0, 10);
      //this.setState({correlations: best4})
      let lobsToLoad = []
      for (let obj of best4) {
        lobsToLoad.push(obj.lobName)
      }
      var myInit = {
        method: 'POST',
        body: {
          "from": this.state.from,
          "to": this.state.to,
          "aggregation": {
            "sum": lobsToLoad
          },
          "granularity": that.state.response.metadata.granularity
        }
      };
      return performFetchPromise("/analyser/data_query/", myInit)
    }).then(response => {
      this.setState({bestCorrelations: response})
    }).finally((x) => {
      this.setState({loadingCorrelations: false})
    })
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

    let form = this.renderForm()

    return <div>

      <PageHeader>DataFlow</PageHeader>

      {form}

      { this.state.response &&
      <div>
        <div className="row">
          <div className="col-xs-6">
            <h2>{shownLobName}</h2>
            Minimal granularity: {this.state.lobs[shownLobName].granularity}
            <br/>
            Granularity: {usedGranularity} minutes &nbsp;
            <Button bsSize="xsmall" bsStyle="warning"
                    onClick={() => this.updateLobConfig(shownLobName, {granularity: usedGranularity})}>Set as
              minimal</Button>
          </div>
          <div className="col-xs-6">
            <h3>Correlated lobs</h3>
          </div>
        </div>
        <div className="row">
          <div className="col-xs-6">
            <MetricGraph source={this.state.response} metrics={metrics} relative={false}
                         smooth={this.state.smooth}/>
            {this.state.medians &&
            <MetricGraph source={this.state.medians} metrics={["median"]}/>
            }
            <div className="row">
              <div className="col-xs-6">
                <h3>Day averages</h3>
                {this.renderAverages()}

              </div>
            </div>
          </div>
          {this.renderCorrelations()}
        </div>
      </div>
      }

      <div className="row ng-scope">

      </div>
    </div>
  }

  renderAverages() {
    //console.log(this.state)
    if (this.state.loadingAverages) {
      return <Spinner spinnerName="three-bounce"/>
    }
    if (this.state.averages) {
      return <MetricGraph source={this.state.averages} metrics={this.state.averages.metrics}
                          relative={false}/>
    }

    return <div>No data</div>
  }

  renderCorrelations() {
    if (this.state.loadingCorrelations) {
      return <Spinner spinnerName="three-bounce"/>
    }
    if (this.state.bestCorrelations) {
      let metrics = null;
      if (this.state.response) {
        metrics = [];
        for (let metric in this.state.bestCorrelations.metadata.metrics) {
          if (!metric.includes("smooth")) metrics.push(metric);
        }
      }
      let metricsCount = metrics.length
      let chartRows = []
      for (let i = 0; i < metricsCount; i += 2) {
        let cols = [
          <div className="col-xs-6">
            {metricsCount >= 1 &&
            <MetricGraph source={this.state.bestCorrelations} metrics={[metrics[i]]} relative={false}
                         smooth={this.state.smooth}/>
            }
          </div>,
          <div className="col-xs-6">
            {metrics[i + 1] &&
            <MetricGraph source={this.state.bestCorrelations} metrics={[metrics[i + 1]]} relative={false}
                         smooth={this.state.smooth}/>}
          </div>]
        chartRows.push(<div className="row">{cols}</div>)

      }
      return <div className="col-xs-6">
        {chartRows}
      </div>
    }
    return <div>no data</div>
  }

  renderForm() {
    let lobNames = null;
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
    return <div>{
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
        <form>
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
            <div className="col-xs-2">
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
          </div>
          <FormGroup>
            <Checkbox onChange={(e) => this.setState({smooth: e.target.checked})}
                      checked={this.state.smooth} inline>
              Smooth
            </Checkbox>
            <Checkbox onChange={(e) => this.setState({showCorrelations: e.target.checked})}
                      checked={this.state.showCorrelations} inline>Show correlations
            </Checkbox>
          </FormGroup>

          <Button onClick={this.loadData.bind(this)}>Apply</Button>
        </form>
      </div>
    }</div>
  }

  static shiftDateByDays(date, days) {
    let newDate = new Date(date)
    newDate.setDate(newDate.getDate() + Number(days));
    return newDate;
  }
}
LobChartPage = connect(mapStateToProps, mapDispatchToProps)(LobChartPage)
export default LobChartPage