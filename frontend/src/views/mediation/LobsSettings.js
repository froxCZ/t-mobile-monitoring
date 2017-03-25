import React, {Component} from "react";
import Api from "../../Api";
import Util from "../../Util";
import CountrySettings from "../../components/CountrySettings";
import classnames from "classnames";
import {TabContent, TabPane, Nav, NavItem, NavLink} from "reactstrap";
import "react-datepicker/dist/react-datepicker.css";
const COUNTRIES = ["CZ", "AT", "DE", "NL"]
class LobsSettings extends Component {
  constructor() {
    super();
    this.state = {countries: null, activeTab: "CZ"}
  }

  componentDidMount() {
    this.loadSettings();
  }

  loadSettings() {
    Api.fetch("/mediation/config/countries", {method: 'GET'}).then(response => {
      this.setState({countries: response});
    })
  }

  saveSettings() {
    let req = {
      method: 'PUT',
      body: this.state.countries
    };
    Api.fetch("/mediation/config/countries", req).then(response => {
      console.log(response)
      this.setState({countries: response});
    })
  }

  toggle(tab) {
    if (this.state.activeTab !== tab) {
      this.setState({
        activeTab: tab
      });
    }
  }

  render() {
    if (!this.state.countries) {
      return <p></p>
    }
    let navs = []
    for (let c of COUNTRIES) {
      navs.push(<NavItem>
        <NavLink
          className={classnames({active: this.state.activeTab === c})}
          onClick={() => {
            this.toggle(c);
          }}
        >
          {c}
        </NavLink>
      </NavItem>)
    }
    let tabs = []
    for (let c of COUNTRIES) {
      tabs.push(<TabPane tabId={c}>
        <div className="row">
          <div className="col-lg-12">
            <div className="card-block">
              <CountrySettings
                country={this.state.countries[c]}
                onSave={this.saveSettings.bind(this)}
                editable={Util.isRoot(this.props.user)}
              />
            </div>
          </div>

        </div>
      </TabPane>)
    }
    return (<div className="row">
      <div className="col-lg-12">
        <Nav tabs>
          {navs}
        </Nav>
        <TabContent activeTab={this.state.activeTab}>
          {tabs}
        </TabContent>
      </div>
    </div>);

  }
}
export default Util.injectUserProp(LobsSettings)