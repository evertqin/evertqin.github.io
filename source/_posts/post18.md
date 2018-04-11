---
title: AngularJS Study Note (2)
date: 08/25/2015
tags: 
- Technology
- AngularJS
- Javascript
---

Other Random notes about angularjs, I will add more to this.     
     
<!--more-->

1. Customize directives
    
    Let's continue the html from yesterday by adding a new controller. In this controller, I tried to use directives.




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
    <div ng-controller="firstController">
      <p ng-bind="whereIsMyDataFrom"></p>
      <ul>
        <li ng-repeat="person in personList |orderBy: '-name'">{{person.name}}</li>
      </ul>
      <p>{{ whereIsMyDataFrom }}</p>
      <p>Simple Calculation: {{ 1 + 1 + 2}}</p>
      <h4>{{ currentTime }}</h4>
    </div>
    <div ng-controller="secondController">
      <my-customized-directive></my-customized-directive>
    </div>
  </body>
</html>
    ~~~~
    
    Notice I added `secondController` and a new html tag `<my-customized-directive>`. Here comes the js file
    
    ~~~~{.js}
firstDivApp.controller('secondController', ['$scope', function($scope){
        $scope.sampleData = "Sample Data";
    }])
    .directive('myCustomizedDirective', function() {
        return {
            restrict:'E',
            template: 'SampleData goes here:  {{ sampleData }}',
        };
    });
    ~~~~
    
    Here I added the new controller and declaresa new directive `myCustomizedDirective`.
    I am restricting it usage to element only (or I can also make it attribute only by specifying `restrict:'A'`).
    I'm also declaring a template. I can also use `templateUrl` and specify the path to a html file. And replace with ` templateUrl: 'template.html'`
    
2. Isolating the scope

    For previous implementation, if you want to use the directive for two people, you need to create two controllers because within a single controller, the customized 
directive can only be used once. To solve this problem, we can isolate the scope of our directives.

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
    <!-- NEW STUFF BELOW -->
    <div ng-controller="firstController">
      <p ng-bind="whereIsMyDataFrom"></p>
      <ul>
        <li ng-repeat="person in personList |orderBy: '-name'">{{person.name}}</li>
      </ul>
      <p>{{ whereIsMyDataFrom }}</p>
      <p>Simple Calculation: {{ 1 + 1 + 2}}</p>
      <h4>{{ currentTime }}</h4>
    </div>
    <div ng-controller="secondController">
      <my-customized-directive info='people1'></my-customized-directive>
      <hr/>
      <my-customized-directive info='people2'></my-customized-directive>
    </div>
  </body>
</html>
    ~~~~
    
    Make modification to the js file:
    
    ~~~~{.js}
firstDivApp.controller('secondController', ['$scope', function($scope){
        $scope.sampleData = "Sample Data";
        $scope.people1 = {name: 'Tom', address:'yyy street'};
        $scope.people2 = {name: 'Dio', address:'ydsdsdsdy stredet'};
    }])
    .directive('myCustomizedDirective', function() {
        return {
            restrict:'E',
            scope:{
            peopleInfo:"=info"
        },
            templateUrl: 'template.html'
        };
    });
    ~~~~
    
    Here, the `people1` binds to attribute `info='people1'`, `people2` binds to attribute `info='people2'`.
    By doing this, we are 
    and update the `template.html`. 
    
    ~~~~{.html}
SampleData goes here:  {{ sampleData }}
People info: name {{peopleInfo.name}}, address: {{peopleInfo.address}}
    ~~~~
    
3. Manipulate DOM object
    
    The key here is to return an object with link function. And current DOM
can be manipulated by using the element varialbe.

    Let's add the following lines to the html
    
    ~~~~{.html}
<div ng-controller="thirdController">
    <my-time-update format="'M/d/yy h:mm:ss a'"></my-time-update>
    <hr/>
    <my-time-update format="'MM/d/yy h:mm:ss a'"></my-time-update>
</div>
    ~~~~
    
    We then create a third controller:
    
    ~~~~{.js}
firstDivApp.controller('thirdController', ['$scope', function($scope){}])
.directive('myTimeUpdate', ['$interval', 'dateFilter', function($interval, dateFilter) {
    var link = function(scope, element, attrs){
        var format;
        var timeoutId;
         function updateTime(){
            console.log(format);
            element.text(dateFilter(new Date(), format));
        };

        scope.$watch(attrs.format, function(value){
            format = value;
            updateTime();
        });
        timeoutId = $interval(function() {
            updateTime();
        },1000);
    };

    return {
        link:link
    };
}]);
    ~~~~
    
    We create a link function which takes `scope, element, attrs` as arguments. scope is the scope of current directive.
    The above function update the element text of the scope every second.

4. Directive that wraps other contents
    
    
    