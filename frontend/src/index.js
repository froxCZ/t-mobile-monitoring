import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import {Store} from "./Store";
import {Provider} from "react-redux";
import Routes from "./Routes";


// Don't do this! You’re bringing DevTools into the production bundle.
Promise.prototype.finally = function(cb) {
  const res = () => this
  return this.then(value =>
      Promise.resolve(cb({state:"fulfilled", value})).then(res)
    , reason =>
      Promise.resolve(cb({state:"rejected", reason})).then(res)
  );
};

ReactDOM.render(
  <Provider store={Store}>
    <div id="container">
      <Routes/>
      {/*<DevTools />*/}
    </div>
  </Provider>,
  document.getElementById('root')
);
