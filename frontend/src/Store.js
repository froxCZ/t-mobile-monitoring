import DevTools from './DevTools';
import {UserReducer, UserSagas, root, TestIt} from './actions/User';
import {createStore, combineReducers, compose, applyMiddleware} from 'redux'
import createSagaMiddleware from "redux-saga";
export const Reducers = combineReducers(
  {user: UserReducer}
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
    ...UserSagas
  ].map(s=> {
    return s();
  });
});


