---
title: Transfering Data between ASP.NET Client and Server
date: 08/03/2015
tag: 
- Technology
- C#
---

Here I am going to summarize commonly used ways to pass data between server and client. There are traditional ways along with some ASP.NET specific ways.

<!--more-->

1. Ajax request, using jQuery Library, if you are using webforms, then:

    ~~~~{.js}
$.ajax({
  type: "POST",
  url: "Analysis.aspx/getStatus",
  data: {},
  contentType: "application/json; charset=utf-8",
  dataType: "json",
  success: function (message) {
    console.log(message);
  },
  error: function(xhr, status, error) {
    console.log(xhr);
  }
});
    ~~~~

    In your code behind (Analysis.aspx.cs), you should have a public static method:

    ~~~~{.cs}
using System.Web.Services;

[WebMethod]
public static string GetStatus()
{
  return this.message;
}
    ~~~~

    In MVC model, it is simpler because you only needs to provide your restful service endpoint to the url field.

    The advantage of using ajax is 1) it is excuted immediately after html is loaded and it is synchronized.

2. Using code block
    The above code behind can also be called be embedding the following line into your javascript part of the page:

    ~~~~{.cs}
var message = "<% GetStatus() %>";
    ~~~~

    Note that by default the evaluated return for a code behind function does not include quotes, so if it is a string type, you have to add quotes manually.
