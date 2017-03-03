import React from "react";
import {Router, Route, IndexRoute, IndexRedirect, hashHistory} from "react-router";
// Containers
import Full from "./containers/Full/";
import LobsMonitoring from "./views/lobs/LobsMonitoring";
import LobMonitoringDetail from "./views/lobs/LobMonitoringDetail";
import LobMonitoringDetailForward from "./views/lobs/LobMonitoringDetailForward";
import LobsSettings from "./views/lobs/LobsSettings";
import Incidents from "./views/incidents/Incidents";
import UsersList from "./views/settings/UsersList";
// import Simple from './containers/Simple/'
import Dashboard from "./views/Dashboard/";

export default (
  <Router history={hashHistory}>
    <Route path="/" name="Home" component={Full}>
      <IndexRoute component={Dashboard}/>
      <Route path="dashboard" name="Dashboard" component={Dashboard}/>
      <Route path="lobs" name="Lobs">
        <IndexRedirect to="monitoring" />
        <Route path="monitoring" name="Monitoring">
          <IndexRoute component={LobsMonitoring}/>
          <Route path=":lobName" name="Lob">
            <IndexRoute component={LobMonitoringDetail}/>
            <Route path=":forwardDetail" name="Forward" component={LobMonitoringDetailForward}/>
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
