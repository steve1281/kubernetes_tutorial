'use strict';

var utils = require('../utils/writer.js');
var Default = require('../service/DefaultService');

module.exports.employeesGET = function employeesGET (req, res, next, bodyLimit, pageLimit) {
  Default.employeesGET(bodyLimit, pageLimit)
    .then(function (response) {
      utils.writeJson(res, response);
    })
    .catch(function (response) {
      utils.writeJson(res, response);
    });
};

module.exports.employeesIdGET = function employeesIdGET (req, res, next, id) {
  Default.employeesIdGET(id)
    .then(function (response) {
      utils.writeJson(res, response);
    })
    .catch(function (response) {
      utils.writeJson(res, response);
    });
};

module.exports.employeesPOST = function employeesPOST (req, res, next, body) {
  Default.employeesPOST(body)
    .then(function (response) {
      utils.writeJson(res, response);
    })
    .catch(function (response) {
      utils.writeJson(res, response);
    });
};
