import React from "react";
import ReactDOM from "react-dom";
import {Router, hashHistory} from "react-router";
import routes from "./routes";
import {Store} from "./Store";
import {Provider} from "react-redux";
ReactDOM.render(
  <Provider store={Store}>
    <div id="container">
      <Router routes={routes} history={hashHistory}/></div>
  </Provider>, document.getElementById('root')
);
