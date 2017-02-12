import React, {Component, PropTypes} from "react";
import {bindActionCreators} from "redux";
import {connect} from "react-redux";
import PageHeader from "react-bootstrap/lib/PageHeader";
import {performFetchPromise} from "../actions/ApiRequest";
import {showLoading, hideLoading} from "react-redux-loading-bar";
import {LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend} from "recharts";
import MetricGraph from "../components/MetricGraph"; // Expects that Highcharts was loaded in the code.

function mapStateToProps(state) {
  return {auth: state.auth};
}
function mapDispatchToProps(dispatch) {
  var actions = {showLoading: showLoading, hideLoading: hideLoading};
  return bindActionCreators(actions, dispatch);
}
class DataFlow extends Component {

  constructor() {
    super();
    this.state = {};
  }

  componentWillMount() {
    this.loadData();
  }

  loadData() {
    var myInit = {
      method: 'POST',
      body: {
        "from": "2016-09-01T08:15:00.000Z",
        "to": "2016-09-08T23:17:00.000Z",
        "aggregation": {
          "sum": ["CZ.GSM", "CZ.MMS"]
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
    return <div>
      <div className="col-lg-12">
        <PageHeader>DataFlow</PageHeader>
      </div>

      <div className="col-lg-12">
        <h2>asdasd</h2>
        { this.state.response &&
        <MetricGraph source={this.state.response} relative={false}/>
        }
      </div>

      <div className="row ng-scope">

      </div>


    </div>
  }
}
DataFlow = connect(mapStateToProps, mapDispatchToProps)(DataFlow)
export default DataFlow