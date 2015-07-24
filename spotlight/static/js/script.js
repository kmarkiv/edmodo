/**
 * Created by vikram on 22/7/15.
 */
// script.js

// create the module and name it scotchApp
// also include ngRoute for all our routing needs
var scotchApp = angular.module('myNoteApp', ['ngRoute', "checklist-model"]);

scotchApp.run(function ($rootScope) {

    $rootScope.loading = true;
    $rootScope.apps = [];
    $rootScope.item = {};

    $rootScope.setItem = function (item) {
        $rootScope.item = item;
        $('#myModal').modal('show');
    };


});

// configure our routes
scotchApp.config(function ($routeProvider) {
    $routeProvider

        // route for the home page
        .when('/', {
            templateUrl: '/static/pages/home.html',
            controller: 'mainController'
        })

        // route for the about page
        .when('/apps/users/:user_id', {
            templateUrl: '/static/pages/home.html',
            controller: 'aboutController'
        })

        // route for the contact page
        .when('/flags', {
            templateUrl: '/static/pages/flags.html',
            controller: 'flagsController'
        });
});

// create the controller and inject Angular's $scope
scotchApp.controller('mainController', function ($scope, $rootScope, $http) {
    // create a message to display in our view


    $scope.sayHello = function () {
        $http.get('/api/apps').
            success(function (data, status, headers, config) {
                // this callback will be called asynchronously
                // when the response is available
                $rootScope.apps = data.response.apps;
                $rootScope.loading = false;
            }).
            error(function (data, status, headers, config) {
                // called asynchronously if an error occurs
                // or server returns response with an error status.
            });
    };

    $scope.message = 'Everyone come and see how good I look!';
    $rootScope.loading = true;
    $scope.sayHello();


});

scotchApp.controller('aboutController', function ($scope, $rootScope, $http, $routeParams) {
    $scope.sayHello = function () {
        $http.get('/api/apps/users/' + $routeParams.user_id).
            success(function (data, status, headers, config) {
                // this callback will be called asynchronously
                // when the response is available
                $rootScope.apps = data.response.apps;
                $rootScope.loading = false;
            }).
            error(function (data, status, headers, config) {
                // called asynchronously if an error occurs
                // or server returns response with an error status.
            });
    };

    $scope.message = 'Everyone come and see how good I look!';
    $rootScope.loading = true;
    $scope.sayHello();
});

scotchApp.controller('contactController', function ($scope, $rootScope, $http) {

    $rootScope.loading = true;
    $scope.submit = function () {
        $http({
            url: '/api/apps/search',
            method: "GET",
            params: {term: $scope.term}
        }).success(function (data, status, headers, config) {
            $rootScope.apps = data.response.apps;
            $rootScope.loading = false;
        }).
            error(function (data, status, headers, config) {

            });
    };


});

scotchApp.controller('flagsController', function ($scope, $rootScope, $http) {

    $rootScope.loading = true;
    $scope.init = function () {
        $http({
            url: '/api/flags',
            method: "GET",
            params: {term: $scope.term}
        }).success(function (data, status, headers, config) {
            $rootScope.flags = data.response.flags;
            $rootScope.loading = false;
        }).
            error(function (data, status, headers, config) {

            });
    };

    $scope.init();


});

scotchApp.controller('modalController', function ($scope, $rootScope, $http) {
    $scope.flags = [
        {id: 1, text: 'Inappropriate'},
        {id: 2, text: 'Not helpful'},
        {id: 3, text: 'Wrong tags'},
        {id: 4, text: 'Spam'}
    ];
    $scope.app_flags = {
        flags: []
    };
    $scope.checkAll = function () {
        $scope.app_flags.flags = $scope.flags.map(function (item) {
            return item.id;
        });
    };
    $scope.uncheckAll = function () {
        $scope.app_flags.roles = [];
    };

    $scope.submit = function (app_id) {
        console.log($scope.app_flags);
        $http({
            url: '/api/flags',
            method: "POST",
            data: $.param({'flags[]': $scope.app_flags.flags, app_id: app_id}),
            headers: {'Content-Type': 'application/x-www-form-urlencoded'}
        }).success(function (data, status, headers, config) {
            //  $('#myModal').modal('close');

        }).
            error(function (data, status, headers, config) {

            });
    };

});


scotchApp.directive('starRating', function () {
    return {
        restrict: 'A',
        template: '<i  ng-repeat="star in stars" ng-class="{true:\'fa fa-star\', false:\'fa fa-star-o\'}[star.filled]" ></i>',
        scope: {
            ratingValue: '=',
            max: '='
        },
        link: function (scope, elem, attrs) {

            scope.stars = [];
            for (var i = 0; i < 5; i++) {
                scope.stars.push({
                    filled: i < scope.ratingValue,
                });
            }
        }
    }
});