import React, {Component} from "react";
import Api from "../../Api";
import Util from "../../Util";
class Dashboard extends Component {
  constructor() {
    super();
    this.state = {events: [], omitOK: true}
  }

  componentDidMount() {
    this.loadEvents(0, this.state.omitOK)
  }

  loadEvents(offset, omitOK) {
    let req = {method: "GET"};
    let events = this.state.events;
    if (offset == 0) {
      events = []
    }
    Api.fetch("/mediation/events?offset=" + offset + "&omitOK=" + omitOK, req).then(response => {
      this.setState({events: events.concat(response)})
    })
  }

  loadMore() {
    this.loadEvents(this.state.events.length, this.state.omitOK)
  }

  omitOKChanged(omitOK) {
    this.loadEvents(0, omitOK);
    this.setState({omitOK: omitOK})
  }

  renderEvents() {
    if (this.state.events == null) {
      return <p></p>
    }
    let rows = [];
    for (let event of this.state.events) {
      let row = <tr>
        <td><img src={Util.countryToFlagPath(event.country)} alt="Czech Republic" style={{height: 15 + 'px'}}/></td>
        <td>{event.lobName}</td>
        <td>{event.flowName}</td>
        <td>{Util.formatIsoDateStrToDateTimeStr(event.time)}</td>
        <td>{Util.formatIsoDateStrToDateTimeStr(event.ticTime)}</td>
        <td>{event.message}</td>
        <td>{event.newStatus}</td>

      </tr>;
      rows.push(row)
    }
    return <div className="row">
      <div className="col-lg-12">
        <div className="card">
          <div className="card-header">
            Events
          </div>
          <div className="card-block">
            <table className="table">
              <thead>
              <tr>
                <th>Country</th>
                <th>Lob</th>
                <th>Flow</th>
                <th>Time</th>
                <th>Tic time</th>
                <th>Message</th>
                <th>Status&nbsp;&nbsp;<br/>
                  <input type="checkbox"
                         id="checkbox3"
                         name="checkbox3"
                         checked={this.state.omitOK}
                         onChange={(e) => this.omitOKChanged(e.target.checked)}/>Omit OK
                </th>
              </tr>
              </thead>
              <tbody>
              {rows}
              </tbody>
            </table>
            <div style={{textAlign: "center"}}>
              <button type="button" className="btn btn-primary btn-lg" onClick={() => {
                this.loadMore()
              }}>More...
              </button>
            </div>

          </div>
        </div>
      </div>
    </div>
  }

  render() {
    return (
      <div className="animated fadeIn">

        {this.renderOverview()}
        {this.renderEvents()}
      </div>
    )
  }

  renderOverview() {
    return <div className="row">
      <div className="col-sm-3">
        <div className="card">
          <div className="card-header">
            <i><img src={'img/flags/Germany.png'} alt="Czech Republic"/></i>Overview
          </div>
          <div className="card-block">
            <h2>
                  <span style={{minWidth: 3 + "em"}} title="ok"
                        className="badge badge-pill badge-success">1</span>
              &nbsp;
              <span style={{minWidth: 3 + "em"}} title="warning"
                    className="badge badge-pill badge-warning">3</span>
              &nbsp;
              <span style={{minWidth: 3 + "em"}} title="outage"
                    className="badge badge-pill badge-danger">8</span>
              &nbsp;
              <span style={{minWidth: 3 + "em"}} title="Disabled"
                    className="badge badge-pill badge-default">5</span>
            </h2>
          </div>
        </div>
      </div>
      <div className="col-sm-3">
        <div className="card">
          <div className="card-header">
            <i><img src={'img/flags/Germany.png'} alt="Czech Republic"/></i>Overview
          </div>
          <div className="card-block">
            <h2>
                  <span style={{minWidth: 3 + "em"}} title="ok"
                        className="badge badge-pill badge-success">1</span>
              &nbsp;
              <span style={{minWidth: 3 + "em"}} title="warning"
                    className="badge badge-pill badge-warning">3</span>
              &nbsp;
              <span style={{minWidth: 3 + "em"}} title="outage"
                    className="badge badge-pill badge-danger">8</span>
              &nbsp;
              <span style={{minWidth: 3 + "em"}} title="Disabled"
                    className="badge badge-pill badge-default">5</span>
            </h2>
          </div>
        </div>
      </div>
      <div className="col-sm-3">
        <div className="card">
          <div className="card-header">
            <i><img src={'img/flags/Germany.png'} alt="Czech Republic"/></i>Overview
          </div>
          <div className="card-block">
            <h2>
                  <span style={{minWidth: 3 + "em"}} title="ok"
                        className="badge badge-pill badge-success">1</span>
              &nbsp;
              <span style={{minWidth: 3 + "em"}} title="warning"
                    className="badge badge-pill badge-warning">3</span>
              &nbsp;
              <span style={{minWidth: 3 + "em"}} title="outage"
                    className="badge badge-pill badge-danger">8</span>
              &nbsp;
              <span style={{minWidth: 3 + "em"}} title="Disabled"
                    className="badge badge-pill badge-default">5</span>
            </h2>
          </div>
        </div>
      </div>
      <div className="col-sm-3">
        <div className="card">
          <div className="card-header">
            <i><img src={'img/flags/Germany.png'} alt="Czech Republic"/></i>Overview
          </div>
          <div className="card-block">
            <h2>
                  <span style={{minWidth: 3 + "em"}} title="ok"
                        className="badge badge-pill badge-success">1</span>
              &nbsp;
              <span style={{minWidth: 3 + "em"}} title="warning"
                    className="badge badge-pill badge-warning">3</span>
              &nbsp;
              <span style={{minWidth: 3 + "em"}} title="outage"
                    className="badge badge-pill badge-danger">8</span>
              &nbsp;
              <span style={{minWidth: 3 + "em"}} title="Disabled"
                    className="badge badge-pill badge-default">5</span>
            </h2>
          </div>
        </div>
      </div>

    </div>
  }
}

export default Dashboard;
