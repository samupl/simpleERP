/// <reference path="typings/angularjs/angular.d.ts" />
/// <reference path="typings/angularjs/angular-resource.d.ts" />
var SimpleERP;
(function (SimpleERP) {
    var Module = (function () {
        function Module() {
        }
        Module.module = angular.module('SimpleERP', []);
        return Module;
    })();
    SimpleERP.Module = Module;
    var ExampleController = (function () {
        function ExampleController($scope) {
            this.scope = $scope;
            this.scope.test = 'Test';
        }/*<auto_generate>*/ExampleController.$inject = ['$scope']; ExampleController.$componentName = 'ExampleController'/*</auto_generate>*/
        return ExampleController;
    })();
    SimpleERP.ExampleController = ExampleController;
    SimpleERP.Module.module.controller('ExampleController', function ($scope) { return new ExampleController($scope); });
})(SimpleERP || (SimpleERP = {}));
