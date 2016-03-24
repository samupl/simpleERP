simpleERPApp.config(function($routeProvider, $locationProvider){
    $locationProvider.html5Mode(true);

    $routeProvider
        .when('/', { controller: 'MainPageCtrl', templateUrl: 'views/main.html'})
        .when('/example', { controller: 'ExampleCtrl', templateUrl: 'views/example.html'});
});