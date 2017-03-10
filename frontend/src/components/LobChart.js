import React, {Component} from "react";
import "react-datepicker/dist/react-datepicker.css";
import Util from "../Util";
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
  "dayDifference": "#FF0080",
  "ticDifference": "#4b4c4c",
  "expected": "#648dbd"
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
    if (!this.props.data || !this.props.metrics) {
      return <p></p>
    }
    LobChart.adjustData(this.props.data);
    let referenceLines = [];
    if (this.props.difference) {
      referenceLines.push(<ReferenceLine y={1} label="expected" stroke="gray"/>)
      referenceLines.push(<ReferenceLine y={this.props.softAlarmLevel} label="expected" stroke="#bd8f1d"/>)
      referenceLines.push(<ReferenceLine y={this.props.hardAlarmLevel} label="expected" stroke="#bd3e39"/>)
    }
    return (
      <ResponsiveContainer height='100%' width='100%' aspect={4.0 / 1.5}>
        <LineChart data={this.props.data} syncId="anyId">
          <XAxis dataKey="tickValue"/>
          <YAxis/>
          <Tooltip /*wrapperStyle={{backgroundColor:'#ff000000'}}*//>
          <Legend />
          {referenceLines}
          {this.renderLines()}
          {this.renderOutages()}
        </LineChart>
      </ResponsiveContainer>
    )
  }

  renderOutages() {
    let outageLines = []
    if (this.props.metrics["status"] == null) {
      return outageLines
    }
    let inOutage = false;
    let outageStart = null;
    let outageEnd = null;
    let tick = null
    for (let i = 0; i < this.props.data.length; i++) {
      tick = this.props.data[i]
      if (tick.status == "OUTAGE") {
        if (!inOutage) {
          outageStart = tick.tickValue
          inOutage = true;
        }
        outageEnd = tick.tickValue
      } else if (inOutage) {
        outageLines.push(
          <ReferenceArea x1={outageStart}
                         x2={outageEnd}
                         stroke="red"
                         strokeOpacity={0.3}/>
        )
        outageStart = null;
        outageEnd = null;
        inOutage = false
      }
    }
    if(inOutage){
      outageLines.push(
        <ReferenceArea x1={outageStart}
                       x2={outageEnd}
                       stroke="red"
                       strokeOpacity={0.3}/>
      )
    }
    return outageLines;


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
      if (i.includes("outage")) {
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

  static adjustData(data) {
    for (let row of data) {
      if (!row.tickValue) {
        row.tickValue = LobChart.dateToTickValue(row._id)
      }
    }
  }

  static dateToTickValue(_id) {
    return Util.formatIsoDateString(_id, "DD.MM.YYYY hh:mm a ddd");
  }

}