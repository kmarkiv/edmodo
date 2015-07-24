/**
 * Created by vikram on 22/7/15.
 */
// script.js

// create the module and name it spotApp
// also include ngRoute for all our routing needs
var spotApp = angular.module('myNoteApp', ['ngRoute', "checklist-model"]);

spotApp.run(function ($rootScope) {

    $rootScope.loading = true;
    $rootScope.apps = [];
    $rootScope.app = {};

    $rootScope.setItem = function (item) {
        $rootScope.app = item;
        $('#myModal').modal('show');
    };


});

// configure our routes
spotApp.config(function ($routeProvider) {
    $routeProvider

        // route for the home page
        .when('/', {
            templateUrl: '/static/pages/home.html',
            controller: 'mainController'
        })

        // route for the app page
        .when('/apps/users/:user_id', {
            templateUrl: '/static/pages/home.html',
            controller: 'appController'
        })

        // route for the flags page
        .when('/flags', {
            templateUrl: '/static/pages/flags.html',
            controller: 'flagsController'
        });
});

// create the controller and inject Angular's $scope
spotApp.controller('mainController', function ($scope, $rootScope, $http) {
    // create a message to display in our view

    $scope.init = function () {
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

    $rootScope.loading = true;
    $scope.init();


});

spotApp.controller('appController', function ($scope, $rootScope, $http, $routeParams) {
    $scope.init = function () {
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

    $rootScope.loading = true;
    $scope.init();
});

spotApp.controller('searchController', function ($scope, $rootScope, $http) {


    $scope.submit = function () {
        $rootScope.loading = true;
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

spotApp.controller('flagsController', function ($scope, $rootScope, $http) {

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

spotApp.controller('modalController', function ($scope, $rootScope, $http) {
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
        $scope.app_flags.flags = [];
    };

    $scope.submit = function (app_id) {
        console.log($scope.app_flags);
        $http({
            url: '/api/flags',
            method: "POST",
            data: $.param({'flags[]': $scope.app_flags.flags, app_id: app_id}),
            headers: {'Content-Type': 'application/x-www-form-urlencoded'}
        }).success(function (data, status, headers, config) {
            $('#myModal').modal('hide');
            $scope.uncheckAll();

        }).
            error(function (data, status, headers, config) {

            });
    };

});


spotApp.directive('starRating', function () {
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