import {take, put, fork} from "redux-saga/effects";
import {performFetch} from './ApiRequest'
export const LOGIN = 'LOGIN';
export const LOGGED_IN = 'LOGGED_IN';
export const LOGIN_FAILED = 'LOGIN_FAILED';
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
    user: response
  }
}
export function loginFailed() {
  return {
    type: LOGIN_FAILED,
  }
}
export function logout() {

  return {
    type: LOGOUT
  }
}

export function AuthReducer(state = {}, action) {
  console.log(action);
  switch (action.type) {
    case LOGIN:
      return {...state, isLoading: true};
    case LOGGED_IN:
      return {...action, isLoading: false};
    case LOGIN_FAILED:
      return {loginFailed: true, isLoading: false}
    case LOGOUT:
      return {};
    default:
      return state;
  }
}

export function* LoginSaga() {
  while (true) {
    try {
      const action = yield take(LOGIN)
      var myInit = {
        method: 'POST',
        body: JSON.stringify({
          username: action.username,
          password: action.password,
        })
      }
      var response = yield performFetch("/login", myInit)
      yield put(loggedIn(response))
    } catch (error) {
      yield put(loginFailed());
    }
  }
}

export const AuthSagas = [
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
