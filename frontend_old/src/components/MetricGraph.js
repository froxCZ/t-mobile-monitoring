import React, {Component} from "react";
import {bindActionCreators} from "redux";
import {connect} from "react-redux";
import Modal from "react-bootstrap/lib/Modal";
import Button from "react-bootstrap/lib/Button";
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

const CustomizedDot = React.createClass({
  render () {
    const {cx, cy, stroke, payload} = this.props;

    if (payload.value > 2500) {
      return (
        <svg x={cx - 10} y={cy - 10} width={20} height={20} fill="red" viewBox="0 0 1024 1024">
          <path
            d="M512 1009.984c-274.912 0-497.76-222.848-497.76-497.76s222.848-497.76 497.76-497.76c274.912 0 497.76 222.848 497.76 497.76s-222.848 497.76-497.76 497.76zM340.768 295.936c-39.488 0-71.52 32.8-71.52 73.248s32.032 73.248 71.52 73.248c39.488 0 71.52-32.8 71.52-73.248s-32.032-73.248-71.52-73.248zM686.176 296.704c-39.488 0-71.52 32.8-71.52 73.248s32.032 73.248 71.52 73.248c39.488 0 71.52-32.8 71.52-73.248s-32.032-73.248-71.52-73.248zM772.928 555.392c-18.752-8.864-40.928-0.576-49.632 18.528-40.224 88.576-120.256 143.552-208.832 143.552-85.952 0-164.864-52.64-205.952-137.376-9.184-18.912-31.648-26.592-50.08-17.28-18.464 9.408-21.216 21.472-15.936 32.64 52.8 111.424 155.232 186.784 269.76 186.784 117.984 0 217.12-70.944 269.76-186.784 8.672-19.136 9.568-31.2-9.12-40.096z"/>
        </svg>
      );
    }

    return (
      <svg x={cx - 10} y={cy - 10} width={20} height={20} fill="green" viewBox="0 0 1024 1024">
        <path
          d="M517.12 53.248q95.232 0 179.2 36.352t145.92 98.304 98.304 145.92 36.352 179.2-36.352 179.2-98.304 145.92-145.92 98.304-179.2 36.352-179.2-36.352-145.92-98.304-98.304-145.92-36.352-179.2 36.352-179.2 98.304-145.92 145.92-98.304 179.2-36.352zM663.552 261.12q-15.36 0-28.16 6.656t-23.04 18.432-15.872 27.648-5.632 33.28q0 35.84 21.504 61.44t51.2 25.6 51.2-25.6 21.504-61.44q0-17.408-5.632-33.28t-15.872-27.648-23.04-18.432-28.16-6.656zM373.76 261.12q-29.696 0-50.688 25.088t-20.992 60.928 20.992 61.44 50.688 25.6 50.176-25.6 20.48-61.44-20.48-60.928-50.176-25.088zM520.192 602.112q-51.2 0-97.28 9.728t-82.944 27.648-62.464 41.472-35.84 51.2q-1.024 1.024-1.024 2.048-1.024 3.072-1.024 8.704t2.56 11.776 7.168 11.264 12.8 6.144q25.6-27.648 62.464-50.176 31.744-19.456 79.36-35.328t114.176-15.872q67.584 0 116.736 15.872t81.92 35.328q37.888 22.528 63.488 50.176 17.408-5.12 19.968-18.944t0.512-18.944-3.072-7.168-1.024-3.072q-26.624-55.296-100.352-88.576t-176.128-33.28z"/>
      </svg>
    );
  }
});
const DAY_NR_TO_NAME = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
class MetricGraph extends Component {

  constructor() {
    super();
    this.state = {}
  }

  handleChartMove(event) {
    if (this.state.from != null && event.activeTooltipIndex != null) {
      this.setState({to: event.activeTooltipIndex})
    }
  }

  handleChartMouseDown(event) {
    this.setState({from: event.activeTooltipIndex, to: null})
  }

  handleChartMouseUp(event) {
    if (this.state.from != null && event.activeTooltipIndex != null) {
      console.log("ASd")
      this.setState({showModal: true, to: event.activeTooltipIndex})
    }
  }

  indexToDataObject(i) {
    console.log(i)
    return this.props.source.data[i]
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
    let lineType = "linear";
    // if (this.props.relative) {
    //   data = MetricGraph.createRelativeValues(this.props.source.metadata.metrics, this.props.source.data);
    // } else {
    //   data = MetricGraph.scaleValues(this.props.source.metadata.metrics, this.props.source.data);
    // }
    data = this.props.source.data
    MetricGraph.adjustDate(data);
    let lines = [];
    let colors = ["red", "blue", "orange", "green"];
    let outageAreas = []
    console.log(this.props)
    if (this.props.outages) {
      for (let i in this.props.outages) {
        let outage = this.props.outages[i]
        console.log(outage)
        outageAreas.push(<ReferenceArea x1={MetricGraph.dateToTickValue(outage.from)}
                                        x2={MetricGraph.dateToTickValue(outage.to)}
                                        stroke="red"
                                        strokeOpacity={0.3}/>)
      }
    }
    if (this.state.from && this.state.to) {
      let fromLabel = MetricGraph.dateToTickValue(this.indexToDataObject(this.state.from)._id)
      let toLabel = MetricGraph.dateToTickValue(this.indexToDataObject(this.state.to)._id)
      outageAreas.push(
        <ReferenceArea x1={fromLabel}
                       x2={toLabel}
                       stroke="yellow"
                       bgColor="#f0f0f0"
                       strokeOpacity={0.5}/>)
    }
    for (let i in metrics) {
      if (metrics[i].includes("smoothed")) {
        if (this.props.smooth) {
          lines.push(<Line type={lineType} dataKey={metrics[i]} stroke={colors[i]} strokeWidth={0.5} dot={false}
                           activeDot={true}
                           isAnimationActive={false}/>)
        }
      } else {
        lines.push(<Line type={lineType} dataKey={metrics[i]} stroke={colors[i]} dot={false}
                         activeDot={true}
                         label={(name, value) => `${name} asda: ${value}`}
                         isAnimationActive={false}/>)
      }
    }

    return <div>
      {this.confirmNewRangeModal()}
      <ResponsiveContainer height='100%' width='100%' aspect={4.0 / 1.5}>
        <LineChart data={data} syncId="anyId"
                   onMouseDown={this.handleChartMouseDown.bind(this)}
                   onMouseMove={this.handleChartMove.bind(this)}
                   onMouseUp={this.handleChartMouseUp.bind(this)}
        >
          <XAxis dataKey="tickValue"/>
          <YAxis/>
          <Tooltip/>
          <Legend />
          {outageAreas}
          <ReferenceLine y={1} label="expected" stroke="gray"/>
          <ReferenceLine y={0.8} label="expected" stroke="yellow"/>
          <ReferenceLine y={0.6} label="expected" stroke="red"/>
          {lines}
        </LineChart>
      </ResponsiveContainer>
    </div>
  }

  closeModal() {
    this.setState({showModal: false, from: null, to: null})
  }

  confirmNewRange() {
    this.props.onRangeConfirmed({
      from: this.indexToDataObject(this.state.from)._id,
      to: this.indexToDataObject(this.state.to)._id
    })
  }

  confirmNewRangeModal() {
    return <div>{
      this.state.showModal && <Modal show={this.state.showModal} onHide={this.closeModal.bind(this)}>
        <Modal.Header closeButton>
          <Modal.Title>Confirm outage range</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          From: {MetricGraph.dateToTickValue(this.indexToDataObject(this.state.from)._id)} <br/>
          To: {MetricGraph.dateToTickValue(this.indexToDataObject(this.state.to)._id)}
        </Modal.Body>
        <Modal.Footer>
          <Button onClick={this.closeModal.bind(this)}>Close</Button>
          <Button bsStyle="success" onClick={this.confirmNewRange.bind(this)}>Confirm</Button>

        </Modal.Footer>
      </Modal>
    }
    </div>
  }

  static adjustDate(data) {
    for (let row of data) {
      if (!row.tickValue) {
        row.tickValue = MetricGraph.dateToTickValue(row._id)
      }
    }
  }

  static dateToTickValue(_id) {
    return _id + " - " + DAY_NR_TO_NAME[new Date(_id).getDay()] + "";
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