import {showLoading, hideLoading} from "react-redux-loading-bar";
import {Store} from "./Store";
function delayPromise(duration) {
  return function (...args) {
    return new Promise(function (resolve, reject) {
      setTimeout(function () {
        resolve(...args);
      }, duration)
    });
  };
}
class Api {

  lobInputs(fromDate, toDate, lobName, neid, granularity) {
    var myInit = {
      method: 'POST',
      body: {
        "from": fromDate,
        "to": toDate,
        "lobNames": [lobName],
        "neid": neid,
        "granularity": granularity || 0
      }
    };
    return this.fetch("/data_query/v2", myInit);
  }

  fetch(url, myInit) {
    let myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    myInit.headers = myHeaders;
    myInit.body = JSON.stringify(myInit.body)
    let request = new Request(url, myInit);
    Store.dispatch(showLoading());
    return fetch(request).then((response) => response.json())
      .then(x => {
        return x
      }).finally(x => {
        Store.dispatch(hideLoading())
      });
  }
}

export default Api = new Api();