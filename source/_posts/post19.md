---
title: AngularJS Study Note -- ngView and ngRoute(3)
date: 08/26/2015
tags: 
- Technology
- AngularJS
- Javascript
---

Tried a little big ngView and ngRoute, the basic concept is not so difficult to grasp. It is like regular V and C in MVC.
The function of this ngApp is to display different images when click on different links. Traditionally, using jQuery, we can just update the src of the image. 
This ngApp is just for demo, i don't think it has more advantage than just using jQuery. But it does quite fun to think of this in a VC way.

<!--more-->

~~~~{.html}
<html ng-app="imageSelector">
  <head>
    <script src="http://ajax.googleapis.com/ajax/libs/angularjs/1.3.14/angular.js"></script>
    <script type='text/javascript' src="https://ajax.googleapis.com/ajax/libs/angularjs/1.4.3/angular-route.min.js"></script>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
    <link rel="stylesheet" href="main.css"/>
    <script type="text/javascript" src="main.js"></script>
  </head>
  <body>
    <h3>This is a test</h3>
    <a href="/images/image0">image0</a>
    <a href="/images/small/image1">image1</a>
    <div class="image-select" ng-controller="mainController as main">
      <div ng-view></div>
    </div>
  </body>
</html>
~~~~

we need to include angularjs route module in the head.

~~~~{.js}
(function() {
    var imageSelector = angular.module('imageSelector', ['ngRoute']);
    imageSelector.config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider){
        $routeProvider.when('/images/:imageId',{
            template: "<div>This is a image {{bigImage.params.imageId}} and size is {{bigImage.size}}<img src='/images/image_0.jpg'/></div>",
            controller:'BigImageController',
            controllerAs:'bigImage'
        }).when('/images/small/:imageId', {
            template: "<div>This is a image '{{smallImage.params.imageId}}' and size is very very {{smallImage.size}}<image src='/images/IMG_1822.jpg' /></div>",
            controller:'SmallImageController',
            controllerAs:'smallImage'
        });
        $locationProvider.html5Mode({
            enabled:true,
            requireBase:false
        });
    }]).controller('mainController',
                   ['$route', '$routeParams', '$location', function($route, $routeParams, $location){
                       this.$route = $route;
                       this.$routeParams = $routeParams;
                       this.$location = $location;
                   }]).controller('BigImageController', ['$routeParams', function($routeParams){
                       this.size = 'Big';
                       this.params = $routeParams;
                   }]).controller('SmallImageController', ['$routeParams', function($routeParms){
                       this.size = 'Small';
                       this.params = $routeParms;
                   }]);
    
})();
~~~~
We need first config `$routeProvide` and `$locationProvide`. The first configs the route params, like we do in express.js. Following the tutorial, created two routes and provide two inline templates. Also need to specify which controller
to use for given route.

Then we need to implement controllers. The first `mainController` needs to be implement like we do for other angular apps. I am not sure about this yet, will update when I figure out. Then we implement two other controllers used by
two routes. They are not different from other controllers. However, instead of use `$scope` to pass data, here we use `this`. 










