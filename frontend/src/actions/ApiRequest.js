export function* performFetch(request) {
  return yield fetch(request)
    .then((response) => response.json())
}