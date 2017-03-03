import {createStore, combineReducers, compose, applyMiddleware} from "redux";
import {loadingBarReducer} from "react-redux-loading-bar";
export const AUTH = "auth";
export const Reducers = combineReducers(
  {
    loadingBar: loadingBarReducer
  }
);
const initialState = {};

export const Store = createStore(Reducers, initialState);


export function state(key) {
  return Store.getState()[key];
}

