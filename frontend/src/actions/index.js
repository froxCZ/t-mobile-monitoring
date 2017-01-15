let nextTodoId = 0
import {combineReducers} from 'redux';
import {UserReducer} from './User'

export const Reducers = combineReducers(
  {user: UserReducer}
);
