angular.module('myApp').factory('AuthService',
  ['$q', '$timeout', '$http',
  function ($q, $timeout, $http) {

    // create user variable
    var user = null;

    // return available functions for use in controllers
    return ({
      isLoggedIn: isLoggedIn,
      login: login,
      logout: logout,
      register: register
    });

  function isLoggedIn() {
    if(user) {
      return true;
    } else {
      return false;
    }
  }



  function login(username, password) {

    // create a new instance of deferred
    var deferred = $q.defer();

    // send a post request to the server
    $http.post('/api/login', {username: username, password: password})
      // handle success
      .success(function (data, status) {
        if(status === 200 && data.status === true){
          user = true;
          # Store Token to LocalStorage
          localStorage['token']=data.token;
          localStorage['uid']=data.userId;
          deferred.resolve();
        } else {
          user = false;
          deferred.reject();
        }
      })
      // handle error
      .error(function (data) {
        user = false;
        deferred.reject();
      });

    // return promise object
    return deferred.promise;

  }

  function logout() {

    // create a new instance of deferred
    var deferred = $q.defer();
    localStorage.removeItem('token');
    localStorage.removeItem('uid');
    // send a get request to the server
    $http.get('/api/logout')
      // handle success
      .success(function (data) {
        user = false;
        deferred.resolve();
      })
      // handle error
      .error(function (data) {
        user = false;
        deferred.reject();
      });

    // return promise object
    return deferred.promise;

  }

  function register(username, password) {

    // create a new instance of deferred
    var deferred = $q.defer();

    // send a post request to the server
    $http.post('/api/register', {username: username, password: password})
      // handle success
      .success(function (data, status) {
        if(status === 200 && data.result){
          deferred.resolve();
        } else {
          deferred.reject();
        }
      })
      // handle error
      .error(function (data) {
        deferred.reject();
      });

    // return promise object
    return deferred.promise;

  }

}]);