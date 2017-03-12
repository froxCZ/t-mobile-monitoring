import {createStore, combineReducers, compose, applyMiddleware} from "redux";
import {loadingBarReducer} from "react-redux-loading-bar";
export const AUTH = "auth";
const AUTH_LOCAL_STORAGE_KEY = 'AUTH_LOCAL_STORAGE_KEY';
export const LOGGED_IN = 'LOGGED_IN';
export const LOGOUT = 'LOGOUT';
const authInitialState = JSON.parse(localStorage.getItem(AUTH_LOCAL_STORAGE_KEY) || '{}');

function loggedIn(user) {
  return {
    type: LOGGED_IN,
    user: user
  }
}
function logout() {

  return {
    type: LOGOUT
  }
}
export function AuthReducer(state = authInitialState, action) {
  switch (action.type) {
    case LOGGED_IN:
      let newState = {...state, user: action.user}
      localStorage.setItem(AUTH_LOCAL_STORAGE_KEY, JSON.stringify(newState));
      return newState;
    case LOGOUT:
      localStorage.setItem(AUTH_LOCAL_STORAGE_KEY, JSON.stringify({}));
      return {};
    default:
      return state;
  }
}
export const Reducers = combineReducers(
  {
    loadingBar: loadingBarReducer,
    [AUTH]: AuthReducer,
  }
);
const initialState = {};

export const Store = createStore(Reducers, initialState);


export function state(key) {
  return Store.getState()[key];
}

export const Actions = {
  loggedIn: loggedIn,
  logout: logout
};



