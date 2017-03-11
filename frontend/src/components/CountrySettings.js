import React, {Component} from "react";
import DateListEditor from "./DateListEditor";


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
      <DateListEditor
        dates={this.state.country.lazyDays}
        />
      <br/>
      <h4>Holidays</h4>
      <DateListEditor
        dates={this.state.country.holidays}
        daysOnly={true}
        />
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