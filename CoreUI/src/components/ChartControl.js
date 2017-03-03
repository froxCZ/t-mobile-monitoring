import React, {Component} from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import Moment from "moment";
const MINUTE_RANGES = [
  0,
  5,
  10,
  15,
  30,
  60,
  120,
  180,
  240,
  480,
  720,
  1440
];
export default class ChatControl extends Component {
  constructor() {
    super()
    this.state = {
      fromDate: Moment().subtract(7, 'days'),
      dayRange: 7,
      granularity: 0
    }
  }

  apply() {
    let dateStr = this.state.fromDate.format("DD.MM.YYYY");
    let toDateStr = this.state.fromDate.add(this.state.dayRange, 'days').format("DD.MM.YYYY");
    this.props.onApply(dateStr, toDateStr, this.state.granularity)
  }

  render() {
    return (
      <div className="row">
        <div className="col-sm-3">

          <div className="form-group">
            <label htmlFor="fromDate">From Date</label>
            <div style={{display: "block"}}>
              <DatePicker
                id="fromDate"
                dateFormat="DD.MM.YYYY"
                selected={this.state.fromDate}
                className="form-control"
                onChange={(date) => this.setState({fromDate: date})}
              />
            </div>
          </div>
        </div>
        <div className="form-group col-sm-2">
          <label htmlFor="ccmonth">Range</label>
          <select className="form-control" id="ccmonth"
                  value={this.state.dayRange}
                  onChange={(e) => this.setState({dayRange: Number(e.target.value)})}>
            {[1, 7, 14, 28].map(function (dayRange) {
              return <option>{dayRange}</option>
            })
            }
          </select>
        </div>
        <div className="form-group col-sm-2">
          <label htmlFor="toDate">Shift date</label>
          <div style={{display: "block"}}>
            <button type="button" className="btn btn-primary">&larr;</button>
            <button type="button" className="btn btn-primary">&rarr;</button>
          </div>
        </div>
        <div className="form-group col-sm-2">
          <label htmlFor="ccmonth">Granularity</label>
          <select className="form-control" id="ccmonth"
                  value={this.state.granularity}
                  onChange={(e) => this.setState({granularity: Number(e.target.value)})}>
            {MINUTE_RANGES.map(function (minuteRange) {
              return <option>{minuteRange}</option>
            })
            }
          </select>
        </div>
        <div className="form-group col-sm-2">
          <label htmlFor="toDate">&nbsp;</label>
          <div style={{display: "block"}}>
            <button type="button" className="btn btn-primary" onClick={
              () => {
                this.apply()
              }}>Apply
            </button>
          </div>
        </div>
      </div>

    )
  }

}