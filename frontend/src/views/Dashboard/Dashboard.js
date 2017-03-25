import React, {Component} from "react";
import Api from "../../Api";
import Util from "../../Util";
import {Link, browserHistory} from "react-router";
import StatusBadge from "../../components/StatusBadge";
import StatusCounterBadge from "../../components/StatusCounterBadge";
class Dashboard extends Component {
  constructor() {
    super();
    this.state = {events: [], omitOK: true, countries: {}}
  }

  componentDidMount() {
    this.loadEvents(0, this.state.omitOK)
    this.loadCountriesOverview()
  }

  loadCountriesOverview() {
    Api.fetch("/mediation/flows", {method: "GET"}).then(response => {
      this.setState({countries: response})
    })
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

  goToFlowDetail(country, lobName, flowName) {
    browserHistory.push("/mediation/monitoring/" + country + "/" + lobName + "/" + flowName);
  }

  renderEvents() {
    if (this.state.events == null) {
      return <p></p>
    }
    let rows = [];
    for (let event of this.state.events) {
      let row = <tr style={{cursor: 'pointer'}}
                    onClick={() => this.goToFlowDetail(event.country, event.lobName, event.flowName)}>
        <td><img src={Util.countryToFlagPath(event.country)} style={{height: 15 + 'px'}}/></td>
        <td>{event.lobName}</td>
        <td>{event.flowName}</td>
        <td>{event.message}</td>
        <td>{Util.formatIsoDateStrToDateTimeStr(event.time)}&nbsp;
          ({Util.timeAgo(Util.parseIsoDateString(event.time))})
        </td>
        <td>{Util.formatIsoDateStrToDateTimeStr(event.ticTime)}</td>
        <td><h5><StatusBadge status={event.newStatus}/></h5></td>

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
                <th>Message</th>
                <th>Time</th>
                <th>Tic time</th>
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
            <i><img src={Util.countryToFlagPath("CZ")} alt="Czech Republic"/></i>Czech Republic
          </div>
          <div className="card-block">
            <h2>
              <StatusCounterBadge statuses={this.state.countries.CZ}/>
            </h2>
          </div>
        </div>
      </div>
      <div className="col-sm-3">
        <div className="card">
          <div className="card-header">
            <i><img src={Util.countryToFlagPath("DE")} alt="Germany"/></i>Germany
          </div>
          <div className="card-block">
            <h2>
              <StatusCounterBadge statuses={this.state.countries.DE}/>
            </h2>
          </div>
        </div>
      </div>
      <div className="col-sm-3">
        <div className="card">
          <div className="card-header">
            <i><img src={Util.countryToFlagPath("AT")} alt="Austria"/></i>Austria
          </div>
          <div className="card-block">
            <h2>
              <StatusCounterBadge statuses={this.state.countries.AT}/>
            </h2>
          </div>
        </div>
      </div>
      <div className="col-sm-3">
        <div className="card">
          <div className="card-header">
            <i><img src={Util.countryToFlagPath("NL")} alt="Netherlands"/></i>Netherlands
          </div>
          <div className="card-block">
            <h2>
              <StatusCounterBadge statuses={this.state.countries.NL}/>
            </h2>
          </div>
        </div>
      </div>

    </div>
  }
}

export default Dashboard;
