(function(){
    simpleERPApp.controller('MainPageCtrl', function ($scope, $rootScope) {
        $rootScope.activeTab = 'main';
    });

    simpleERPApp.controller('ExampleCtrl', function ($scope, $rootScope) {
        $rootScope.activeTab = 'example';
    });
})();