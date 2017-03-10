export function* performFetch(url, myInit) {
  var myHeaders = new Headers();
  myInit.headers = myHeaders;
  myHeaders.append("Content-Type", "application/json");
  var request = new Request(url, myInit);
  return yield fetch(request)
    .then((response) => response.json())
}

export function performFetchPromise(url, myInit) {
  var myHeaders = new Headers();
  myInit.headers = myHeaders;
  myHeaders.append("Content-Type", "application/json");
  myInit.body = JSON.stringify(myInit.body)
  var request = new Request(url, myInit);
  return fetch(request).then((response) => response.json())
}