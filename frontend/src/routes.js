import React from "react";
import {Router, Route, IndexRoute, IndexRedirect, browserHistory} from "react-router";
import Full from "./containers/Full/";
import Simple from "./containers/Simple/";
import CountryMonitoring from "./views/mediation/CountryMonitoring";
import LobMonitoring from "./views/mediation/LobMonitoring";
import FlowMonitoring from "./views/mediation/FlowMonitoring";
import CountrySettingsView from "./views/mediation/CountrySettingsView";
import Zookeeper from "./views/zookeeper/Zookeeper";
import UsersList from "./views/system/UsersList";
import SystemStatus from "./views/system/SystemStatus";
import Dashboard from "./views/Dashboard/";
import Login from "./views/Login";


export default (
  <Router>
    <Route path="/public" component={Simple}>
      <Route path="login" name="Login" component={Login}/>
    </Route>
    <Route path="/" name="Home" component={Full}>
      <IndexRoute component={Dashboard}/>
      <Route path="dashboard" name="Dashboard" component={Dashboard}/>
      <Route path="mediation" name="Mediation">
        <IndexRedirect to="monitoring/CZ"/>
        <Route path="monitoring/:country" name="Country">
          <IndexRoute component={CountryMonitoring}/>
          <Route path=":lobName" name="Lob">
            <IndexRoute component={LobMonitoring}/>
            <Route path=":flowName" name="Flow" component={FlowMonitoring}/>
          </Route>
        </Route>

        <Route path="settings" name="Settings" component={CountrySettingsView}/>
      </Route>
      <Route path="zookeeper" name="Zookeeper">
        <IndexRoute component={Zookeeper}/>
      </Route>
      <Route path="system/" name="System">
        <Route path="users" name="Users" component={UsersList}/>
        <Route path="status" name="Status" component={SystemStatus}/>
      </Route>
    </Route>
  </Router>
);
