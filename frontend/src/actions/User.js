import {take, put} from "redux-saga/effects";
export const LOGIN = 'LOGIN';
export const LOGOUT = 'LOGOUT';

export function login(username, password) {
  return {
    type: LOGIN,
    username: username,
    password: password
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
    case LOGIN:
      return {name: "asd"};
    case LOGOUT:
      return null;
    default:
      return state;
  }
}

export const Actions = {
  login: login,
  logout: logout
};
