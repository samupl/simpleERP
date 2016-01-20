/// <reference path="typings/angularjs/angular.d.ts" />
/// <reference path="typings/angularjs/angular-resource.d.ts" />

module SimpleERP {
    export class Module {
        static module = angular.module('SimpleERP', []);

        constructor() {
        }
    }

    export class ExampleController {
        private scope: any;

        constructor($scope: ng.IScope) {
            this.scope = $scope;
            this.scope.test = 'Test';
        }
    }

    SimpleERP.Module.module.controller('ExampleController', ($scope) => new ExampleController($scope));
}
