import {showLoading, hideLoading} from "react-redux-loading-bar";
import {Store} from "./Store";
function delayPromise(duration) {
  return function(...args){
    return new Promise(function(resolve, reject){
      setTimeout(function(){
        resolve(...args);
      }, duration)
    });
  };
}
class Api {
  fetch(url, myInit) {
    let myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    myInit.headers = myHeaders;
    myInit.body = JSON.stringify(myInit.body)
    let request = new Request(url, myInit);
    Store.dispatch(showLoading());
    return fetch(request).then((response) => response.json())
      .then(x => {
      Store.dispatch(hideLoading())
      return x
    })
  }
}

export default Api;