import React, {Component} from "react";
import DateListManager from "./DateListManager";


export default class CountrySettings extends Component {
  constructor() {
    super();
    this.state = {country: null}
  }

  componentWillMount() {
    this.propChange(this.props)
  }

  componentWillReceiveProps(nextProps) {
    this.propChange(nextProps)
  }

  propChange(props) {
    this.setState({country: props.country})
  }

  render() {
    console.log(this.state)
    if (!this.state.country) {
      return <p></p>
    }
    return <div>
      <h4>Lazy days</h4>
      <DateListManager
        dates={this.state.country.lazyDays}
        ref={(editor) => {
          this.lazyDatesEditor = editor
        }}/>
      <br/>
      <h4>Holidays</h4>
      <DateListManager
        dates={this.state.country.holidays}
        daysOnly={true}
        ref={(editor) => {
          this.holidaysEditor = editor
        }}/>
      <div style={{display: "block"}}>
        <button type="button" className="btn btn-primary" onClick={
          () => {
            this.props.onSave(this.state.country)
          }}>Save
        </button>
      </div>
    </div>
  }

}