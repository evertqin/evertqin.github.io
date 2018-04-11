---
title: Brief summary of .call .apply and .bind in JavaScript
date: 11/08/2015
tags: 
- Technology
- Javascript
---

John Resig's book 'Secretes of the JavaScript Ninja' is really a fun and inspiring masterpiece to read. I believe it is one of the JavaScript book you should keep on your desk for study and reference. I am going to write something to summarize some important and interesting usages of .call(), .apply() and .bind() for my reference.

<!--more-->

All of them are used to change the context of the calling function, a.k.a, the meaning of `this`. For top level function, it is always the `window` because everything is in the global scope. Often times, we want to change the meaning of this (for example, when we use ReactJS, oftentimes we need to attach function to properties such as `CompoentWillMount` and some data are retrieved through `this.state`, you have to use bind to bind this of the parent object to the attached function).

1. `call` and `apply`

      In most of the cases, they can be used interchangeably, they only difference is that `call` accepts the object you want `this` to refer to as the first argument, followed by an arbitrary number of arguments as the arguments of the original function. Whereas `apply`, besides taking same first argument, expects an array of arguments as the second argument.

2. `bind`

      Bind is very useful in binding the context of this to a specific object without worrying about the context. We know that when a function is called as a method of an object, its this is set to the object the method is called on. The code snippet demonstrate how to fix the context of inner object to the outer object.
      ~~~~{.javascript}
    var something = {
      doSomething: function(){
        console.log("I am something");
      },
      doNothing:function(){
        var obj = {
          doSomething: function(){
            console.log("I am something in obj");
          },
          sample0: function(){
            this.doSomething();
          },

          sample1: function(){
            this.doSomething();
          }.bind(this)
        };

        obj.sample0();
        obj.sample1();
      }

      ~~~~

      Notice above program, if you remove the `.bind(this)`, you will see the print out `I am something in obj`. It is also useful in creating partial function.

      ~~~~{.javascript}
    function add(a, b){
      return a + b;
    }

    console.log(add(5, 6));

    var addTwo = add.bind(null, 2);
    console.log(addTwo(6));

    // same result can be achieved as bellow, this is more of a non-functional approach,
    // bind seems to create a new function object but this approach still uses the
    // original function reference
    var anotherAddTwo = function(a){
      return add(a, 2);
    };

    console.log(anotherAddTwo(6));

    var noArgs = add.bind(null, 2, 5);
    console.log(noArgs());
      ~~~~
