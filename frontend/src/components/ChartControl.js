import React, {Component} from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import Moment from "moment";
import _ from "lodash"; // Expects that Highcharts was loaded in the code.
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
  360,
  480,
  720,
  1440
];
const LOCAL_STORAGE = "chartControls";
export default class ChatControl extends Component {
  constructor() {
    super()
    let storageObject = null
    if (localStorage.getItem(LOCAL_STORAGE)) {
      try {
        storageObject = JSON.parse(localStorage.getItem(LOCAL_STORAGE));
        storageObject.fromDate = Moment(storageObject.fromDate, "DD.MM.YYYY")
      } catch (e) {
        storageObject = null
      }
    }
    if (storageObject) {
      this.state = storageObject;
    } else {
      this.state = {
        fromDate: Moment().subtract(7, 'days'),
        dayRange: 7,
        granularity: 0
      }
    }
  }

  apply() {
    let dateStr = this.state.fromDate.format("DD.MM.YYYY");
    let toDateStr = Moment(this.state.fromDate).add(this.state.dayRange, 'days').format("DD.MM.YYYY");
    this.props.onApply({fromDate: dateStr, toDate: toDateStr, granularity: this.state.granularity})
  }

  componentDidUpdate() {
    let toStorage = _.pick(this.state, ['dayRange', 'granularity']);
    toStorage.fromDate = this.state.fromDate.format("DD.MM.YYYY");
    localStorage.setItem(LOCAL_STORAGE, JSON.stringify(toStorage));
  }

  shiftDays(direction) {
    this.setState({fromDate: Moment(this.state.fromDate).add(this.state.dayRange * direction, 'days')})
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
            <button type="button" className="btn btn-primary" onClick={() => this.shiftDays(-1)}>&larr;</button>
            <button type="button" className="btn btn-primary" onClick={() => this.shiftDays(1)}>&rarr;</button>
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