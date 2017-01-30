var _ = require("underscore");


 setTimeout(function () {
 // UsersCollection = db.collection("users");
 // User.save("avojxta", {x: "eeee", _id: "newId"}).then(result=>console.log(result));
 }, 1000)

var User = class User {

  constructor(data) {
    this.tmp = {};
    Object.assign(this, data);
  }

  dto() {
    return _.omit(this, "tmp");
  }

  static findById(id) {
    return db.collection("users").findOne({_id: id})
      .then(user => {
        if (!user)return user;
        return new User(user);
      });
  }

  static save(id, newData) {
    return this.findById(id)
      .then(user => _.extend(user.dto(), newData, {_id: id}))
      .then(updateUser => db.collection("users").save(updateUser))
      .then(result => result.result);
  }

  static create(data){
    return db.collection("users").insertOne(data).then(result =>result.insertedId);
  }

  static delete(userId) {
    return db.collection("users").deleteOne({_id: userId});
  }
};


module.exports = User;