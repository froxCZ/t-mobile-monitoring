import React, {Component} from "react";
import "react-datepicker/dist/react-datepicker.css";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine,
  ReferenceArea
} from "recharts"; // Expects that Highcharts was loaded in the code.

const DAY_NR_TO_NAME = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
const COLORS = ["#FF0080", "#FF6600", "#028482"]
const COLORS_MAP = {
  "scaledDifference": "#e180c7",
  "relativeDifference": "#a7a9af",
  "expected": "#749fd4"
}
export default class LobChart extends Component {
  constructor() {
    super()
    this.state = {}
  }

  componentWillMount() {
    this.propChange(this.props)
  }

  componentWillReceiveProps(nextProps) {
    this.propChange(nextProps)
  }

  propChange(props) {
    //this.setState({metrics: props.metrics, data: props.data})
  }

  render() {
    LobChart.adjustDate(this.props.data);
    return (
      <ResponsiveContainer height='100%' width='100%' aspect={4.0 / 1.5}>
        <LineChart data={this.props.data} syncId="anyId">
          <XAxis dataKey="tickValue"/>
          <YAxis/>
          <Tooltip/>
          <Legend />
          <ReferenceLine y={1} label="expected" stroke="gray"/>
          <ReferenceLine y={0.8} label="expected" stroke="yellow"/>
          <ReferenceLine y={0.6} label="expected" stroke="red"/>
          {this.renderLines()}
        </LineChart>
      </ResponsiveContainer>
    )
  }

  renderLines() {
    let lines = []
    let iColor = 0;
    for (let i in this.props.metrics) {
      if (i.includes("smoothed") && !this.props.smooth) {
        continue;
      }
      if (i.includes("Difference") && !this.props.difference) {
        continue;
      }
      if (this.props.difference && !i.includes("Difference")) {
        continue;
      }
      let color = COLORS_MAP[i]
      if (!color) {
        color = COLORS[iColor++]
      }
      lines.push(<Line type="linear" dataKey={i} stroke={color} isAnimationActive={false} dot={false}/>)
    }
    return lines
  }

  static adjustDate(data) {
    for (let row of data) {
      if (!row.tickValue) {
        row.tickValue = LobChart.dateToTickValue(row._id)
      }
    }
  }

  static dateToTickValue(_id) {
    return _id + " - " + DAY_NR_TO_NAME[new Date(_id).getDay()] + "";
  }

}