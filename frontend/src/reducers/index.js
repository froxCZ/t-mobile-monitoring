import {combineReducers} from 'redux'
import user from './user'

const apps = (state = {}, action) => {
  console.log(action);
  switch (action.type) {
    case 'LOGIN':
      return {...state, b: "x"};
    default:
      return state;
  }
}

const myApp = combineReducers({
  user,
  apps
})

export default myApp