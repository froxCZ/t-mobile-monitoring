import {take, put, fork} from "redux-saga/effects";
import {performFetch} from './ApiRequest'
export const LOGIN = 'LOGIN';
export const LOGGED_IN = 'LOGGED_IN';
export const LOGOUT = 'LOGOUT';

export function login(username, password) {
  return {
    type: LOGIN,
    username: username,
    password: password
  }
}
export function loggedIn(response) {
  return {
    type: LOGGED_IN,
    ...response
  }
}
export function logout() {

  return {
    type: LOGOUT
  }
}

export function UserReducer(state = null, action) {
  console.log(action);
  switch (action.type) {
    case LOGGED_IN:
      return {...action};
    case LOGOUT:
      return null;
    default:
      return state;
  }
}

export function* LoginSaga() {
  while (true) {
    const action = yield take(LOGIN)
    var myInit = {
      method: 'POST',
      body: {
        username: action.username,
        password: action.password,
      }
    }
    var request = new Request('/login', myInit);
    var response = yield performFetch(request)
    yield put(loggedIn(response))
  }
}

export const UserSagas = [
  LoginSaga,
];


export function* root() {
  console.log("asd");
  yield take(LOGIN)
  console.log("asd");
}

export const Actions = {
  login: login,
  logout: logout
};
