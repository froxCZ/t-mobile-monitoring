var ErrorStatus = class ErrorStatus extends Error{
  constructor(msg,statusCode){
    super(msg);
    this.statusCode = statusCode;
  }
};

module.exports = ErrorStatus;