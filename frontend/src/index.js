import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import {Store} from "./Store";
import {Provider} from "react-redux";
import Routes from "./Routes";


// Don't do this! You’re bringing DevTools into the production bundle.


ReactDOM.render(
  <Provider store={Store}>
    <div id="container">
      <Routes/>
      {/*<DevTools />*/}
    </div>
  </Provider>,
  document.getElementById('root')
);
