import React, {Component} from "react";
import Util from "../Util";


export default class JSONEditor extends Component {
  constructor() {
    super();
    this.state = {originalJson: null, jsonString: null}
  }

  componentWillMount() {
    this.propChange(this.props)
  }

  componentWillReceiveProps(nextProps) {
    this.propChange(nextProps)
  }

  propChange(props) {
    if (JSON.stringify(props.json) !== JSON.stringify(this.state.originalJson)) {
      this.setState({originalJson: props.json, jsonString: JSON.stringify(props.json, null, 2)})
    }
  }

  render() {
    let hasData = this.state.originalJson != null
    let isValidJson = Util.isValidJson(this.state.jsonString);
    let buttonText = isValidJson ? "Save" : "Invalid JSON";
    return <div>
                <textarea
                  rows="30"
                  value={this.state.jsonString}
                  className="form-control"
                  disabled={!hasData}
                  onChange={(e) => {
                    let state = {jsonString: e.target.value}
                    this.setState(state)
                  }}
                />
      <div style={{display: "block"}}>
        <button type="button"
                className="btn btn-primary"
                disabled={!isValidJson}
                onClick={
                  () => {
                  }}>{buttonText}
        </button>
      </div>
    </div>
  }

}