var router = require('express').Router()
var User = require('./user');

function login(req, res) {
  User.findById(req.body.login).then(user=> {
    if (user == null || user.password != req.body.password) {
      res.sendStatus(401);
    } else {
      res.send(user);
    }
  });
}

function createUser(req, res, next) {
  var user = req.body;
  var requiredAttributes = ["login", "password"];
  Promise.resolve(user)
    .then(user => {
      for (let attribute of requiredAttributes) {
        if (user[attribute] == null) {
          var error = new Error('missing ' + attribute + ' attribute');
          error.statusCode = 400;
          throw error;
        }
      }
      return user;
    })
    .then(user => {
      user._id = user.login;
      delete user.login;
      user.apiKey = Math.random().toString(36).replace(/[^a-z0-9]+/g, '');
      return user;
    })
    .then(user => User.findById(user._id))
    .then(user => {
      if (user) {
        throw new Error("user already exists");
      }
    })
    .then(()=>User.create(user))
    .then(result=>res.send({_id: result}))
    .catch(err=> next(err));
}
function getUser(req, res) {
  User.find({}, {apiKey: false, password: false}).then(result=> {
    res.send(result);
  })
}

router.get("/user", getUser);
router.post("/user", createUser);
router.post('/user/login', login);


router.delete("/user/:id");
router.get("/user/:userId", function (req, res) {
  var userId = req.params.userId;
  User.delete(userId).then(result=>res.send(result.result));
})


module.exports = router;