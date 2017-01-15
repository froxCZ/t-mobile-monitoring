import {combineReducers} from 'redux'

const apps = (state = {}, action) => {
  console.log(action);
  switch (action.type) {
    case 'LOGIN':
      return {...state, b: "x"};
    default:
      return state;
  }
}
const debugReducer = (state = {}, action) => {
  console.log(action);

  return state;
}
const myApp = combineReducers({
  apps,
  debugReducer
})

export default myApp