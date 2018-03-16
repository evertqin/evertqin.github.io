---
title: Bring Together RequireJS and AngularJS
date: 10/08/2015
tags: 
- Technology
- RequireJS
- AngularJS
- Javascript
---
Recently, I accidentally poked into the frontend development code of some company. That website does not use too many frontend
frameworks except for jQuery and another one I am going to talk about today -- RequireJS.

<!--more-->

I would say when I first saw it during interview, the structure looked very familiar to me.

~~~~{.js}
define(['jquery', 'underscore'], function($, _) {
    ...
});
~~~~

I remember doing something similiar in AngularJS too.
~~~~{.js}
mainApp.controller('controller', ['$scope'], function($scope){});
~~~~
When we need to specify the dependencies, we put them
in an array and pass them as arguments to the function. Similar as they appear, bringing them together is not entirely easy. The difficult is because of how those frameworks work:

The concept of RequireJS is based on Asynchronous Module Loading (AMD). That is
modules are loaded in an async way by the order you specified but it is not guaranteed the order is still maintained due to asynchronous nature.[*](http://www.sitepoint.com/understanding-requirejs-for-effective-javascript-module-loading/). Some
a `shim` option is provided to manage the dependencies.

The concept of AngularJS:

Angular initializes automatically upon DOMContentLoaded event or when the angular.js script is evaluated if at that time document.readyState is set to 'complete'. At this point Angular looks for the ng-app directive which designates your application root. If the ng-app directive is found then Angular will:

* load the module associated with the directive.
* create the application injector
* compile the DOM treating the ng-app directive as the root of the compilation. This allows you to tell it to treat only a portion of the DOM as an Angular application.

If we use automatic initialization, our application will fail for some module not found error.
The conflict here is: RequireJS delays the loading of js after page is rendered but angular js needs define those directives before replacing portion of DOM as ng-app. So we have to use manual bootstrapping when document is ready.
~~~~
.
├── app
│   ├── blog
│   │   ├── angular
│   │   │   ├── blogApp.js
│   │   │   └── blogFilter.js
│   │   └── blog.main.js
│   ├── index
│   │   ├── angular
│   │   │   ├── mainApp.js
│   │   │   ├── randomFixedImage.js
│   │   │   └── randomImage.js
│   │   └── index.main.js
│   ├── photography
│   │   └── photography.main.js
│   └── post.main.js
├── blog.js
├── common.js
├── constants
│   └── constants.js
├── index.js
├── lib
│   ├── count.js
│   ├── header-scroll.js
│   ├── jquery.simplePagination.js
│   ├── require.js
│   ├── smoothscroll.js
│   └── utils.js
├── photography.js
├── post.js
~~~~

I put all the common libraries into lib folder. In my html page, first call `<script data-main="/build/js/index" async="" src="/build/js/lib/require.js"></script>`. This tells requirejs
to load itself first in async manner, then load the index.js file under the path we specified.

Our index js is merely like following:

~~~~{.js}
require(['./common'], function (common) {
    require(['/js/app/index/index.main.js']);
});
~~~~

common.js contains config for requirejs, because angular does not support AMD, we need to define it in `shim`:

~~~~{.js}
require.config({
    baseUrl: '/build/js/app',
    paths: {

        angular: "https://ajax.googleapis.com/ajax/libs/angularjs/1.4.7/angular",
    },
    // angular does not support AMD out of the box, put it in a shim
  shim: {
    'angular': {
      exports: 'angular'
    },
  },
});
~~~~

Following structure is a zoom in view of the structure for saving all the js related with index page. I break down angular module into small parts and make each of them a seperate requirejs module.
~~~~
.
├── angular
│   ├── mainApp.js
│   ├── randomFixedImage.js
│   └── randomImage.js
└── index.main.js
~~~~

Take mainApp.js as an example:

~~~~{.js}
define(['angular'], function(angular){
  'use strict';

  var mainApp = angular.module('mainApp', []);

  // bootstrap angular here, notice we need to apply directive before bootstraping
  mainApp.init = function() {
      angular.bootstrap(document, ['mainApp']);
  };

  mainApp.controller('backgroundController', ['$scope',function($scope){
  }])
  .factory('getImage', [function(imageUrls){
    function getImage(imageUrls){
      var selectedImageIdx = Math.floor(Math.random() * imageUrls.length);
      return imageUrls[selectedImageIdx];
    }

    return getImage;
  }]);

  return mainApp;
});
~~~~

We return mainApp as a require module. Then for randomFixedImage directive, we need to declare mainApp as a dependent), apply the directive to it and return.

~~~~{.js}
define(['./mainApp', 'constants'], function(mainApp, constants){
  'use strict';

  mainApp.directive('randomFixedImage', ['getImage', function(getImage){
    var link = function(scope, element, attrs){
      var url = getImage(constants.staticImageUrls);
      element.css({
        'background-image':'url(' + url + ')',
      });
    };
    return {
      restrict:'A',
      link: link
    };
  }]);

  return mainApp;
});
~~~~

Finally, we need to bootstrap this angular module in `index.main.js`. To make sure mainApp is initialized first, we put it as dependent in the beginning. Then we load two directives
and call app.init();

~~~~{.js}
require(["jquery","skrollr", "./index/angular/mainApp"], function($, skrollr, app) {
  "use strict";

  require(["./index/angular/randomFixedImage", "./index/angular/randomImage"], function(){
    app.init();
  });

  ....
});
~~~~
