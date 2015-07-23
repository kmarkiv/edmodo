/**
 * Created by vikram on 22/7/15.
 */
// script.js

// create the module and name it scotchApp
// also include ngRoute for all our routing needs
var scotchApp = angular.module('myNoteApp', ['ngRoute']);

scotchApp.run(function ($rootScope) {

    $rootScope.loading = true;
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
        .when('/about', {
            templateUrl: '/static/pages/about.html',
            controller: 'aboutController'
        })

        // route for the contact page
        .when('/contact', {
            templateUrl: '/static/pages/contact.html',
            controller: 'contactController'
        });
});

// create the controller and inject Angular's $scope
scotchApp.controller('mainController', function ($scope, $rootScope) {
    // create a message to display in our view
    $scope.message = 'Everyone come and see how good I look!';
    $rootScope.loading = false;
});

scotchApp.controller('aboutController', function ($scope, $rootScope) {
    $scope.message = 'Look! I am an about page.';
    $rootScope.loading = true;
});

scotchApp.controller('contactController', function ($scope, $rootScope) {
    $scope.message = 'Contact us! JK. This is just a demo.';
    $rootScope.loading = false;
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