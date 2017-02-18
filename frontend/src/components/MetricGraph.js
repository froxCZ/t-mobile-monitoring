import React, {Component} from "react";
import {bindActionCreators} from "redux";
import {connect} from "react-redux";
import {LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer} from "recharts"; // Expects that Highcharts was loaded in the code.
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
    //MetricGraph.adjustDate(data);
    let lines = [];
    let colors = ["red", "blue", "orange", "yellow"];
    for (let i in metrics) {
      lines.push(<Line type={lineType} dataKey={metrics[i]} stroke={colors[i]} dot={false} activeDot={true}
                       isAnimationActive={false}/>)
    }


    return <ResponsiveContainer height='100%' width='100%'  aspect={4.0/1.5}>
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
      row._id = row._id.split("T")[0];
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