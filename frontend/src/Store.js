import DevTools from './DevTools';
import {AuthReducer,AuthListener, AuthSagas} from './actions/Auth';
import {createStore, combineReducers, compose, applyMiddleware} from 'redux'
import createSagaMiddleware from "redux-saga";
export const AUTH = "auth";
export const Reducers = combineReducers(
  {[AUTH]: AuthReducer}
);
const initialState = {};
const sagaMiddleware = createSagaMiddleware();
const enhancer = compose(
  // Required! Enable Redux DevTools with the monitors you chose
  applyMiddleware(sagaMiddleware),
  DevTools.instrument()
);
export const Store = createStore(Reducers, initialState, enhancer);
sagaMiddleware.run(function*() {
  yield [
    ...AuthSagas
  ].map(s=> {
    return s();
  });
});

Store.subscribe(function () {
  AuthListener(state(AUTH));
});

export function state(key) {
  return Store.getState()[key];
}

