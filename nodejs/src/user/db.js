var exports = {}
class User {
  constructor(data) {
    Object.assign(this, data);
  }
}
exports.findById = function (id) {
  return db.collection('users').find({_id: id}).limit(1).toArray().then(users=> {
    var user = users[0];
    return new User(user);
  })
}
module.exports = exports;
