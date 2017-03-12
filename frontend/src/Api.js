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

  updateLobConfig(lobName, updateObj) {
    var myInit = {
      method: 'POST',
      body: updateObj
    };
    return this.fetch("/mediation/config/" + lobName, myInit);
  }

  lobData(fromDate, toDate, lobName, neids, forwards, granularity) {
    var myInit = {
      method: 'POST',
      body: {
        "from": fromDate,
        "to": toDate,
        "lobNames": [lobName],
        "neids": neids,
        "forwards": forwards,
        "granularity": granularity || 0
      }
    };
    return this.fetch("/mediation/data_query/flows", myInit);
  }

  fetch(url, myInit) {
    let myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    myInit.headers = myHeaders;
    if (typeof myInit.body != 'string' || !myInit.body instanceof String) {
      myInit.body = JSON.stringify(myInit.body)
    }
    let request = new Request(url, myInit);
    Store.dispatch(showLoading());
    return fetch(request).then((response) => {
      if (response.status >= 200 && response.status < 300) {
        return response.json();
      } else {
        let error = new Error(response.status);
        error.status = response.status
        error.json = response.json()
        return Promise.reject(error)
      }
    })
      .then(x => {
        return x
      }).finally(x => {
        Store.dispatch(hideLoading())
      });
  }
}

export default Api = new Api();