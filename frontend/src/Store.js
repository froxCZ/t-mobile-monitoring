import DevTools from './DevTools';
import {AuthReducer, AuthSagas, root, TestIt} from './actions/Auth';
import {createStore, combineReducers, compose, applyMiddleware} from 'redux'
import createSagaMiddleware from "redux-saga";
export const Reducers = combineReducers(
  {auth: AuthReducer}
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


