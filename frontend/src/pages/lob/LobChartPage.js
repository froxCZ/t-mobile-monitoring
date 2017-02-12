import React, {Component, PropTypes} from "react";
import {bindActionCreators} from "redux";
import {connect} from "react-redux";
import PageHeader from "react-bootstrap/lib/PageHeader";
import Button from "react-bootstrap/lib/Button";
import {performFetchPromise} from "../../actions/ApiRequest";
import {showLoading, hideLoading} from "react-redux-loading-bar";
import {LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend} from "recharts";
import MetricGraph from "../../components/MetricGraph";
import {Typeahead} from "react-bootstrap-typeahead";
import "react-bootstrap-typeahead/css/Typeahead.css";
import "react-bootstrap-typeahead/css/ClearButton.css";
import "react-bootstrap-typeahead/css/Loader.css";
import "react-bootstrap-typeahead/css/Token.css";
import DatePicker from "react-bootstrap-date-picker"; // Expects that Highcharts was loaded in the code.
// ES2015
// ES2015

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
    this.state = {lobs: null};
  }

  componentWillMount() {
    this.loadLobs();
  }

  loadLobs() {
    this.props.showLoading();
    var that = this;
    performFetchPromise("/lobs", {method: 'GET'}).then(lobs=> {
      console.log(lobs);
      that.setState({lobs: lobs});
      that.props.hideLoading();
    })
  }

  dateChanged(a,b){
    console.log(a)
    console.log(b)
  }
  loadData() {
    var myInit = {
      method: 'POST',
      body: {
        "from": this.state.from,
        "to": this.state.to,
        "aggregation": {
          "sum": this.state.selectedLobs
        }
      }
    };
    var that = this;
    this.props.showLoading();
    performFetchPromise("/data/dev", myInit).then(result=> {
      that.setState({response: result});
      that.props.hideLoading();
    });
  }


  render() {
    let lobs = null;
    if (this.state.lobs) {
      lobs = [];
      for (let lob of this.state.lobs.CZ) {
        lobs.push("CZ." + lob);
      }
    }
    let metrics = null;
    if (this.state.response) {
      metrics = [];
      for (let metric in this.state.response.metadata.metrics) {
        metrics.push(metric);
      }
    }
    console.log(this.state);
    return <div>

      <PageHeader>DataFlow</PageHeader>
      {
        lobs &&
        <div>
          <div className="row">
            <div className="col-xs-3">
              <label>Lob:</label>
              <Typeahead
                onChange={(selected)=>this.setState({selectedLobs: selected})}
                //multiple={true}
                options={lobs}
              />
            </div>
            <div className="col-xs-3 datePicker">
              <label>From:</label>
              <DatePicker value={this.state.from} dateFormat="DD.MM.YYYY" onChange={(val)=>this.setState({from:val})}/>
            </div>
            <div className="col-xs-3 datePicker">
              <label>To:</label>
              <DatePicker value={this.state.to} dateFormat="DD.MM.YYYY" onChange={(val)=>this.setState({to:val})}/>
            </div>
          </div>
          <div className="row">
            <div className="col-lg-3">
              <Button onClick={this.loadData.bind(this)}>Filter</Button>
            </div>
          </div>
        </div>
      }


      <div className="col-lg-12">
        <h2>asdasd</h2>
        { this.state.response &&
        <MetricGraph source={this.state.response} metrics={metrics} relative={false}/>
        }
      </div>

      <div className="row ng-scope">

      </div>
    </div>
  }
}
LobChartPage = connect(mapStateToProps, mapDispatchToProps)(LobChartPage)
export default LobChartPage