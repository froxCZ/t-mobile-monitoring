import React, {Component} from "react";
import {bindActionCreators} from "redux";
import {connect} from "react-redux";
import {LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer} from "recharts"; // Expects that Highcharts was loaded in the code.

/*class CustomActiveDot extends Component {
 render() {
 const {cx, cy, stroke, payload} = this.props;
 console.log(this.props)
 return <svg x={cx - 10} y={cy - 10} width={20} height={20} fill="red" viewBox="0 0 1024 1024">
 <path
 d="M512 1009.984c-274.912 0-497.76-222.848-497.76-497.76s222.848-497.76 497.76-497.76c274.912 0 497.76 222.848 497.76 497.76s-222.848 497.76-497.76 497.76zM340.768 295.936c-39.488 0-71.52 32.8-71.52 73.248s32.032 73.248 71.52 73.248c39.488 0 71.52-32.8 71.52-73.248s-32.032-73.248-71.52-73.248zM686.176 296.704c-39.488 0-71.52 32.8-71.52 73.248s32.032 73.248 71.52 73.248c39.488 0 71.52-32.8 71.52-73.248s-32.032-73.248-71.52-73.248zM772.928 555.392c-18.752-8.864-40.928-0.576-49.632 18.528-40.224 88.576-120.256 143.552-208.832 143.552-85.952 0-164.864-52.64-205.952-137.376-9.184-18.912-31.648-26.592-50.08-17.28-18.464 9.408-21.216 21.472-15.936 32.64 52.8 111.424 155.232 186.784 269.76 186.784 117.984 0 217.12-70.944 269.76-186.784 8.672-19.136 9.568-31.2-9.12-40.096z"/>
 </svg>
 }
 }*/
const DAY_NR_TO_NAME = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
class MetricGraph extends Component {

  constructor() {
    super();
  }

  render() {
    let data = [];
    let metrics = []
    if (this.props.metrics) {
      metrics = this.props.metrics;
    } else {
      for (let i in this.props.source.metadata.metrics) {
        metrics.push(i);
      }
    }
    let lineType = "basis";
    if (this.props.interpolate) {
      lineType = "basis"
    } else {
      lineType = "linear"
    }
    if (this.props.relative) {
      data = MetricGraph.createRelativeValues(this.props.source.metadata.metrics, this.props.source.data);
    } else {
      data = MetricGraph.scaleValues(this.props.source.metadata.metrics, this.props.source.data);
    }
    MetricGraph.adjustDate(data);
    let lines = [];
    let colors = ["red", "blue", "orange", "yellow"];
    for (let i in metrics) {
      lines.push(<Line type={lineType} dataKey={metrics[i]} stroke={colors[i]} dot={false}
                       activeDot={true}
                       isAnimationActive={false}/>)
    }


    return <ResponsiveContainer height='100%' width='100%' aspect={4.0 / 1.5}>
      <LineChart data={data}>
        <XAxis dataKey="_id"/>
        <YAxis/>
        <Tooltip/>
        <Legend />
        {lines}
      </LineChart>
    </ResponsiveContainer>
  }

  static adjustDate(data) {
    for (let row of data) {
      row._id = row._id + " - " + DAY_NR_TO_NAME[new Date(row._id).getDay()] + "";
    }
  }

  static scaleValues(metrics, data) {
    let max = 0;
    for (let v in metrics) {
      max = Math.max(metrics[v].max, max);
    }
    let scaleFactor = 1;
    if (max > 1000000) {
      scaleFactor = 1000000;
    } else if (max > 1000) {
      scaleFactor = 1000;
    }

    let newData = [];
    for (let row of data) {
      var newRow = {...row};
      for (let k in metrics) {
        var o = metrics[k]
        newRow[k] = (row[k]) / scaleFactor;
      }
      newData.push(newRow);
    }
    return newData;
  }

  static createRelativeValues(metrics, data) {
    for (let v in metrics) {
      metrics[v].diff = metrics[v].max - metrics[v].min
    }
    let newData = [];
    for (let row of data) {
      var newRow = {...row};
      for (let k in metrics) {
        var o = metrics[k]
        newRow[k] = (row[k] - o.min) / o.diff
      }
      newData.push(newRow);
    }
    return newData;
  }
}
export default MetricGraph