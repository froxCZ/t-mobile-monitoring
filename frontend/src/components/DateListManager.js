import React, {Component} from "react";
import DatePicker from "react-datepicker";
import _ from "lodash";
import "react-datepicker/dist/react-datepicker.css";


export default class DateListManager extends Component {
  constructor() {
    super();
    this.state = {dates: []}
  }

  componentWillMount() {
    this.propChange(this.props)
  }

  componentWillReceiveProps(nextProps) {
    this.propChange(nextProps)
  }

  propChange(props) {
    let dateFormat = "DD.MM.YYYY";
    if (props.daysOnly) {
      dateFormat = "DD.MM";
    }
    let dates = []
    if (props.dates) {
      dates = props.dates;
    }
    this.setState({dateFormat: dateFormat, dates: dates})
  }

  removeDay(dateStr) {
    let dates = this.state.dates;
    dates = _.pull(dates, dateStr);
    this.setState({dates: dates})
  }

  addDay(date) {
    let dates = this.state.dates;
    dates.push(date.format(this.state.dateFormat));
    this.setState({dates: dates})
  }

  render() {
    let datesList = [];
    for (let date of this.state.dates) {
      datesList.push(
        <h5 style={{display: "inline"}}>
          <span className="badge badge-default">{date}&nbsp;
            <i style={{cursor: "pointer"}}
               onClick={() => {
                 this.removeDay(date)
               }}
               className="icon-close">
          </i>
          </span>
          &nbsp;
        </h5>)
    }

    return <div>{datesList}
      <DatePicker
        id="fromDate"
        dateFormat={this.state.dateFormat}
        className="form-control"
        onChange={(date) => {
          this.addDay(date)
        }}
      /></div>
  }

}