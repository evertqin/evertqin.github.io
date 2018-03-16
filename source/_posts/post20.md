---
title: React.js Study Note (1)
date: 09/24/2015
tags: 
- Technology
- ReactJS
- Javascript
---

I am doing a new project recently so I am trying to follow the react.js tutorial and make use of this new technology in my project. It is claimed that the concept of react.js is fondamentally different from AngularJS. For example AngularJS is a full MVC framework but ReactJS is only the View of the MVC. The following figure demonstrated the whole concept.

<!--more-->

![Compare AngularJS with ReactJS](http://i1-news.softpedia-static.com/images/news2/Basic-Differences-Between-AngularJS-and-React-484781-2.jpg)

I will add other things from time to time

~~~~{.html}
<div id="content">
  <div id="pageTitle" class="container">
    <div class="row">
      <div class="col-md-3">
        <div id="leftlist"></div>
      </div>
    </div>
  </div>
</div>
~~~~


~~~~{.jsx}
(function ($) {
    var NamesList = React.createClass({
        render: function () {
            var namesList = this.props.names.map(function (name) {
                return (
                    <li>
                        <a>{name.YLabel}</a>
                    </li>
                    );
            });

            return (
                <ul className="namesList">
                    {namesList}
                </ul>
                );
        }
    });

    var LeftListBox = React.createClass({
        getInitialState: function () {
          return { names: [ {YLabel:"Test1"},
             {YLabel:"Test2"} ]};
        },
        componentDidMount: function () {
            $.ajax({
                url: this.props.url,
                dataType: 'json',
                cache: false,
                success: function (names) {
                    this.setState({ names: names });
                }.bind(this),
                error: function (xhr, status, err) {
                    console.error(this.props.url, status, err.toString());
                }.bind(this),
            });
        },
        render: function () {
            return (
                <div className="leftListBox">
                    <NamesList names={this.state.names}></NamesList>
                </div>
                );
        }

    });




    var url = 'Plot/AggregatedPlotHandler.ashx?name=all';
    React.render(
      <LeftListBox url={url}>Sample</LeftListBox>,
      document.getElementById('leftlist')
    );
})(jQuery);
~~~~

This is modified from tutorial. I am creating a list by making ajax request to a endpoint with querystring. The return is an array of objects. `getInitialState` helps us setup the default this.state value. `componentDidMount` , according to the official document:

*Invoked once, only on the client (not on the server), immediately after the initial rendering occurs. At this point in the lifecycle, the component has a DOM representation which you can access via React.findDOMNode(this). The componentDidMount() method of child components is invoked before that of parent components.*

*If you want to integrate with other JavaScript frameworks, set timers using setTimeout or setInterval, or send AJAX requests, perform those operations in this method.*

Data binding is somewhat similar to AngularJS, you bind by assigning curly bracket to variable directly. Whereas in angular, you can use ng-bind or directly use double curly bracket.
