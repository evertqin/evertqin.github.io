---
title: AngularJS Study Note (1)
date: 08/24/2015
tags: 
- Technology
- AngularJS
- Javascript
---

I have been learning AngularJS recently. Although people say Angular might be okay for small scale websites, it becomes very slow as the website grow larger. Many people turn to React.js for better performace. But I do think it 
is useful to learn the concept of Angular since it has been there for quite a while and there are a lot of cool concepts.

<!--more-->

1. Terminologies

    At a high level, directives are markers on a DOM element (such as an attribute, element name, comment or CSS class) that tell AngularJS's HTML compiler ($compile) to attach a specified behavior to that DOM element or even transform the DOM element and its children.([From Angular document](https://docs.angularjs.org/guide/directive))
    
    There are several important built-in angular directives (ngApp, npBind, ngController, etc). You will know ngApp and ng-app are basically same thing because angular always covert to camelcase.

1. Baby Step

    ~~~~{.html}
<html ng-app>
  <head>
    <script src="http://ajax.googleapis.com/ajax/libs/angularjs/1.3.14/angular.js"></script>
  </head>
  <body>
    <h3>This is my First app</h3>
    <input type="text" ng-model="happyInput" ng-init="happyInput='sample'"/>
    <p>input: {{ happyInput }}</p>
    <h3 ng-bind="happyInput"></h3>
  </body>
</html>
    ~~~~

    To serve this web page, open it directly in browser, but I prefer using python to server static page: navigate to the page containing the above page (index.html). run `python3.4 -m http.server`. Then you can navigate to `http://localhost:8000` to view the page.
    
    The above page is simple, it declares this is a angular app ("ng-app" directive only). It also declares ng-model for the input textbox. After this binding, we can use whatever data inside input by calling {{ happyInput }} or explicitly bind it to a html tag (h3 above). The ng-init directive is useful when you want to specify a initial value for your ng-model.
    
    An angular app cannot be simpler than above. In reality, most of them are pretty complicated.

3. we need javascript now
      ~~~~{.html}
<html ng-app="firstDiv">
  <head>
    <script src="http://ajax.googleapis.com/ajax/libs/angularjs/1.3.14/angular.js"></script>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
    <script type="text/javascript" src="main.js"></script>
  </head>
  <body>
    <h3>This is my First app</h3>
    <input type="text" ng-model="happyInput" ng-init="happyInput='sample'"/>
    <p>input: {{ happyInput }}</p>
    <h3 ng-bind="happyInput"></h3>
    <!-- !!!NEW STUFF BELOW!!! -->
    <div ng-controller="firstController">
      <ul>
        <li ng-repeat="person in personList |orderBy: '-name'">{{person.name}}</li>
      </ul>
      <p>{{ whereIsMyDataFrom }}</p>
    </div>
  </body>
</html>
      ~~~~
    What's new here:
    * Added a name for our ng-app;
    * Added a ng-controller="firstController" for a div;
    * Used the ng-bind "whereIsMyDataFrom", but where is the data?
    * Used ng-repeat

    Take a look at the js file included in the html
    main.js
    
      ~~~~{.js}
(function() {
  var firstDivApp = angular.module('firstDiv', []);
  firstDivApp.controller('firstController', function($scope){
      $scope.personList = [
          {
              name: "Zohn", address: "somewhere"
          },
          {
              name: "Tom", address: "somewhere else"
          }
      ];
      $scope.whereIsMyDataFrom = "My Data is from Here";
  });
})();
      ~~~~
    `$scope` is a special variable for passing date to and from html view and js controller. Here we see where our "whereIsMyDataFrom" is populated and where our personList come from. The orderBy is another concept called ng-filter, normally, it sorts data in ascending order by the field specified. Adding a minus sign `-` will sort data in descending order.
    (Note: I actually think it is better to write the controller logic in the following way because of it follows more closely to the dependence injection pattern.
   
      ~~~~{.js}
firstDivApp.controller('firstController', ['$scope', function($scope){
   $scope.personList = [
       {
           name: "Zohn", address: "somewhere"
       },
       {
           name: "Tom", address: "somewhere else"
       }
   ];
   $scope.whereIsMyDataFrom = "My Data is from Here";
}]);
      ~~~~
    
    The second argument of the `module.controller(...)` has two parts. First part is the objects to be injected, the last element of the list usually contains the previous list elements (quote removed) as arguments. Although you can get away without specifying the injected object names for built-in variables, I do think it is clearly to use them.

2. fun with dependence injection(DI)
    I think this one is very easy to get hands on, there are three steps:
    1. put the the name of dependence you want to inject in the controller dependence list as stated above;
    2. call the .factory on the controller, return a function
  
    Add `<h4>{{ currentTime }}</h4>` somewhere iside firstController.
  
    Modify main.js
    
      ~~~~{.js}
(function() {
var firstDivApp = angular.module('firstDiv', []);

firstDivApp.controller('firstController', ['$scope','getCurrentTime', function($scope, getCurrentTime){
    $scope.personList = [
        {
            name: "Zohn", address: "somewhere"
        },
        {
            name: "Tom", address: "somewhere else"
        }
    ];
    $scope.whereIsMyDataFrom = "My Data is from Here";
    $scope.currentTime = getCurrentTime('M/d/yy h:mm:ss a');
}])
    .factory('getCurrentTime', ['dateFilter', function(dateFilter, format){
        var date = new Date();

        return  function(format){
            return dateFilter(new Date(), format);
        };
    }]);
})();
      ~~~~
  
    Notice the factory part. Here we need a function getCurrentTime which takes a single paramenter "format". 