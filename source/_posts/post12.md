---
title: Combine WCF, ASP.NET, SignalR for event broadcasting (1)
date: 07/29/2015
tags: 
- Technology
- C#
---

Previously, I introduced a way to broadcast logging events from log4net. Today I'm taking it a step forward by enabling event broadcasting on website.

<!--more-->

In traditional desktop applications, such as WinForms, events handling is quite a breeze -- For built in events like Timer.Elaspsed,  the only thing we need to do is to subscribe a delegate. However, when it comes to the web word, events handling is not that simple anymore. The reason is browser does not actively run and wait for events after the page is rendered, so there is no way to change the DOM except for by using frontend javascript. Also, regular ways to send data between frontend and backend, regardless whether it is a synchronized call or AJAX requires a series of actions, including open the socket, sending the request, process the request, send back response, close the socket. The whole process needs to open and close socket each time so it is not very efficient so it is ideal if we need real-time data.

Luckily, there is a great technology called [SignalR](http://www.asp.net/signalr) that makes the real-time communication between ASP.NET frontend and backend much easier. What I am going to show here contains three components:

#### Create dummy business logic

1. An assembly that mimic logging event generation from business logic.

2. A WCF service running in either interactive mode or as windows service. This is the backend service.

3. An ASP.NET website that calls the WCF service reference and receive logging events broadcasting all the way from the business logic.

Let's start by creating the dummy business logic.

* Create an empty console application (we will change it to class library later but let's make it console application first for easier debugging)

  ![Create a Console Application](http://i.imgur.com/xFa0Sbc.png)

* Add log4net through NuGet

* Create EventAppender, BroadcastEventArgs and BroadcastEvetnService as introduced in my previous blog post[http://blog.tripplan.info/blog/post/item/4](http://blog.tripplan.info/blog/post/item/4).

* Make a new folder called "Configs" and add log4net_config.xml to that folder, make sure for the line `<appender name="EventAppender" type="LogBroadcaster.Broadcast.EventAppender, LogBroadcaster">`, you use the correct classes. For the type attribute, the field before comma should be the full reference path to the EventAppender, the field after comma should be the assembly name containing the EventAppender.

* Add a new folder called "Test" and add a new class "TestRunner"

~~~~{.cs}
public class TestRunner
{
    private static readonly ILog _log = LogManager.GetLogger(typeof (TestRunner));

    private Timer timer;

    public TestRunner()
    {
        timer = new Timer();
    }

    public void GeneratingRandomLog()
    {
        Random rand = new Random();
        double interval = rand.NextDouble()*10000;

        timer.Interval = interval;
        timer.Elapsed +=
            (sender, eventArgs) =>
            {
                _log.Warn(string.Format("This is a test. Now timer is {0}", eventArgs.SignalTime));
            };
        timer.Start();
    }
}
~~~~

* Add the following code snippet to Main function:

~~~~{.cs}
TestRunner testRunner = new TestRunner();
testRunner.GeneratingRandomLog();

Console.ReadKey();
~~~~

Now run the project, and you should see some dummy log messages scrolling in the console

* Change the project property to dll by changing Application -> Output type to "Class Library". Compile the dll.

#### Create WCF Service and enabling asynchronous callback

Conventional client server modal is： client sends a request to server and wait for a response, after server processed the request, client get the response then unblock. This is one directional. A Duplex service is a pattern that both endpoints can send and receive messages to the other independently.

* Start by creating a console application(We could have started with WCF class library, but still, a console application is easier to debug during development)

* Add a WCF service to the project (New Item... -> WCF Service). Here I named my service "MyWcfService". Visual Studio will automatically create IMyWcfService Interface and MyWcfService implementation.

* To make the project more interesting, I am adding another interface "IMyWcfServiceAsync" to the project. The idea behind this is that I want to put all my asynchronous functions under a separate interface so I can add different ServiceContract Attributes to them. The project will look like the following figure.

  ![Create WCF console application](http://i.imgur.com/rEVKRS4.png)

* Add the dll generated from last solution as reference..

* Add ServiceContracts and OperationContracts to the interfaces and classes.

  * IMyWcfService

~~~~{.cs}
[ServiceContract]
public interface IMyWcfService
{
    [OperationContract]
    void DoWork();
}
~~~~

  * IMyWcfServiceAsync

~~~~{.cs}
[ServiceContract(Namespace = "mynamspace", SessionMode = SessionMode.Required)]
public interface IClientCallback
{
    [OperationContract]
    void NotifyClient(string message);
}

[ServiceContract(Namespace = "mynamspace", SessionMode = SessionMode.Required,
    CallbackContract = typeof (IClientCallback))]
public interface IMyWcfServiceAsync
{
    [OperationContract(IsOneWay = true)]
    void ListenToEvents();
}
~~~~

  The most importand part is `[ServiceContract(Namespace = "mynamspace", SessionMode = SessionMode.Required,
      CallbackContract = typeof (IClientCallback))]` attribute. This tells that this ServiceContract is a asynchronous callback contract and the client to provide a implementation of IClientCallback interface.

  * MyWcfService

~~~~{.cs}
using System.ServiceModel;
using LogBroadcaster.Broadcast;
using LogBroadcaster.Test;

namespace MyWcfServiceHost
{
    public class MyWcfService : IMyWcfService, IMyWcfServiceAsync
    {
        public void DoWork()
        {
            TestRunner testRunner = new TestRunner();
            testRunner.GeneratingRandomLog();
        }

        public void ListenToEvents()
        {
            // this call back is only valid in the context of this function
            var callback = OperationContext.Current.GetCallbackChannel<IClientCallback>();

            BroadcastEventService.Instance.BroadcastEvent +=
                (sender, eventArgs) => { callback.NotifyClient(eventArgs.Message); };
        }
    }
}
~~~~

5. Make a new folder called "Configs" and add log4net_config.xml to that forlder by copying from previous solution.

6. Rename `Program.cs` to "WcfServiceHost" (or a name of your choice) and replace its content with following code:

~~~~{.cs}

namespace MyWcfServiceHost
{
    internal class WcfServiceHost : ServiceBase
    {
        private static readonly Dictionary<string, ServiceHost> _ServiceHosts = new Dictionary<string, ServiceHost>();

        public static ServiceHost GetService(string sSrvName)
        {
            if (_ServiceHosts.ContainsKey(sSrvName)) return _ServiceHosts[sSrvName];
            return null;
        }

        public WcfServiceHost()
        {
            this.ServiceName = "MyWcfService";
            Directory.SetCurrentDirectory(AppDomain.CurrentDomain.BaseDirectory);
        }

        private static void RunInteractive(ServiceBase[] servicesToRun)
        {
            Console.WriteLine("Services running in interactive mode.");
            Console.WriteLine();

            MethodInfo onStartMethod = typeof (ServiceBase).GetMethod("OnStart",
                BindingFlags.Instance | BindingFlags.NonPublic);
            foreach (ServiceBase service in servicesToRun)
            {
                Console.Write("Starting {0}...", service.ServiceName);
                ((WcfServiceHost) service).OnStart(new string[] {});
                //onStartMethod.Invoke(service, new object[] { new string[] { } });
                Console.Write("Started");
            }

            Console.WriteLine();
            Console.WriteLine();
            Console.WriteLine(
                "Press any key to stop the services and end the process...");
            Console.ReadKey();
            Console.WriteLine();

            MethodInfo onStopMethod = typeof (ServiceBase).GetMethod("OnStop",
                BindingFlags.Instance | BindingFlags.NonPublic);
            foreach (ServiceBase service in servicesToRun)
            {
                Console.Write("Stopping {0}...", service.ServiceName);
                //onStopMethod.Invoke(service, null);
                ((WcfServiceHost) service).OnStop();
                Console.WriteLine("Stopped");
            }

            Console.WriteLine("All services stopped.");
            // Keep the console alive for a second to allow the user to see the message.
            Thread.Sleep(1000);
        }

        protected int OpenAll()
        {
            OpenHost<MyWcfService>();
            return _ServiceHosts.Count();
        }

        protected int CloseAll()
        {
            foreach (ServiceHost serviceHost in _ServiceHosts.Values)
            {
                try
                {
                    serviceHost.Close(new TimeSpan(0, 0, 10));
                }
                catch (Exception ex)
                {
                    serviceHost.Abort();
                }
            }
            _ServiceHosts.Clear();
            return 0;
        }

        protected void OpenHost<T>()
        {
            Type type = typeof (T);
            ServiceHost serviceHost = new ServiceHost(type);
            serviceHost.Open();
            _ServiceHosts[type.ToString()] = serviceHost;
        }

        protected override void OnStart(string[] args)
        {
            // eventlog.WriteEntry("AnalysisWindowsService started.");
            this.CloseAll();
            this.OpenAll();
        }

        protected override void OnStop()
        {
            this.CloseAll();
        }

        private static void Main(string[] args)
        {
            ServiceBase[] servicesToRun;
            servicesToRun = new ServiceBase[]
            {
                new WcfServiceHost()
            };
            if (Environment.UserInteractive)
            {
                RunInteractive(servicesToRun);
            }
            else
            {
                Run(servicesToRun);
            }
        }
    }
}

~~~~

* Update the app.config

~~~~{.xml}
<?xml version="1.0" encoding="utf-8"?>

<configuration>
  <system.serviceModel>
    <behaviors>
      <serviceBehaviors>
        <behavior name="">
          <serviceMetadata httpGetEnabled="false" />
          <serviceDebug includeExceptionDetailInFaults="false" />
        </behavior>
      </serviceBehaviors>
      <endpointBehaviors>
        <behavior name="MyEndpointBehavior">
          <dataContractSerializer maxItemsInObjectGraph="2147483646" />
        </behavior>
      </endpointBehaviors>
    </behaviors>

    <bindings>
      <netTcpBinding>
        <binding name="BufferedNetTcpBindingConf" receiveTimeout="16:10:00" sendTimeout="16:10:00"
                 transferMode="Buffered" maxBufferPoolSize="2147483647" maxBufferSize="2147483647"
                 maxReceivedMessageSize="2147483647">
          <readerQuotas maxArrayLength="2147483647" />
          <security mode="None" />
        </binding>
      </netTcpBinding>
    </bindings>
    <services>
      <service name="MyWcfServiceHost.MyWcfService">
        <endpoint address="" behaviorConfiguration="MyEndpointBehavior" binding="netTcpBinding"  bindingConfiguration="BufferedNetTcpBindingConf" contract="MyWcfServiceHost.IMyWcfService">
          <identity>
            <dns value="localhost" />
          </identity>
        </endpoint>
        <endpoint address="" behaviorConfiguration="MyEndpointBehavior" binding="netTcpBinding" bindingConfiguration="BufferedNetTcpBindingConf" contract="MyWcfServiceHost.IMyWcfServiceAsync">
          <identity>
            <dns value="localhost" />
          </identity>
        </endpoint>
        <endpoint address="mex" binding="mexTcpBinding" name="MexTcpBindingEndpoint" contract="IMetadataExchange" />
        <host>
          <baseAddresses>
            <add baseAddress="net.tcp://localhost:8733/MyWcfService/" />
          </baseAddresses>
        </host>
      </service>
    </services>
  </system.serviceModel>
  <startup>
    <supportedRuntime version="v4.0" sku=".NETFramework,Version=v4.5" />
  </startup>
</configuration>

~~~~

  I am creating two endpoints for two of my interfaces. Also, I am setting "maxReceivedMessageSize" to max, although it is not necessary in this application. Also I am using net+tcp here. You can also use dualHttp binding, check the article here [Duplex Service](https://msdn.microsoft.com/en-us/library/ms731064(v=vs.110).aspx)

  The above code will enable this wcf to run either under interactive mode or run as windows service. Hit F5 and you should be able to see the following screen.

  ![WCF service successfully run under interactive mode](http://i.imgur.com/rPUtRF3.png)
