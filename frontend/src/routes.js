import React from "react";
import {Router, Route, IndexRoute, IndexRedirect, browserHistory} from "react-router";
// Containers
import Full from "./containers/Full/";
import Simple from "./containers/Simple/";
import LobsMonitoring from "./views/mediation/LobsMonitoring";
import LobMonitoringDetail from "./views/mediation/LobMonitoringDetail";
import LobMonitoringDetailForward from "./views/mediation/LobMonitoringDetailForward";
import LobsSettings from "./views/mediation/LobsSettings";
import Incidents from "./views/incidents/Incidents";
import UsersList from "./views/settings/UsersList";
// import Simple from './containers/Simple/'
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
        <Route path="monitoring/:country" name="Monitoring">
          <IndexRoute component={LobsMonitoring}/>
          <Route path=":lobName" name="Lob">
            <IndexRoute component={LobMonitoringDetail}/>
            <Route path=":flowName" name="Input" component={LobMonitoringDetailForward}/>
          </Route>
        </Route>

        <Route path="settings" name="Settings" component={LobsSettings}/>
      </Route>
      <Route path="incidents/" name="Incidents">
        <IndexRoute component={Incidents}/>
        <Route path="active" name="Active" component={Incidents}/>
        <Route path="archive" name="Archive" component={Incidents}/>
      </Route>
      <Route path="settings/" name="Incidents">
        <Route path="users" name="Users" component={UsersList}/>
      </Route>
    </Route>
  </Router>
);
