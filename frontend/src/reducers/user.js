import * as ActionTypes from '../const/ActionTypes';
const user = (state = {}, action) => {
  switch (action.type) {
    case ActionTypes.LOGIN:
      return action.user;
    case 'LOGOUT':
      return {};
    default:
      return state;
  }
}

export default user;