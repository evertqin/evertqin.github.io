---
title: Custom log4net appender for broadcasting log events
date: 07/08/2015
tags: 
- Technology
- Programming
- CSharp
---

Recently, I was assigned a task to create a module that other modules can subscribe to and get updates when message is logged. Naturally, one would think of using C# event to broadcast a message and client modules can subscribe to the event. Here I am leveraging the powerful log4net's custom appender to broadcast event whenever an info level message is logged.

To construct the whole process, we need at least 3 classes:

<!--more-->

* BroadcastEventArgs

This is a class holding most of the data we wish to broadcast to clients. I could just reuse the LoggingEvent class provided by log4net, but since we might need more customization, creating a new class might be a better choice.

~~~~{.csharp}
using System;

namespace log4netEventBroadcast
{
	public class BroadcastEventArgs : EventArgs
	{
		public DateTime DataTime { get; set; }
		public string Level { get; set; }
		public string LoggerName { get; set; }
		public string ThreadName { get; set; }
		public string Message { get; set; }
	}
}
~~~~

* BroadcastEventService

This is a singleton class for event broadcasting and handling. Our broadcasters can call the functions (such as Start(), Broadcast(), etc) to signal some events. Clients can subscribe to several provided events provided by this class.

~~~~{.csharp}
using System;

namespace log4netEventBroadcast
{
	public delegate void BroadcastEventHandler(object sender, BroadcastEventArgs e);

	public class BroadcastEventService
	{
		private static volatile BroadcastEventService _instance;
		private static object _mutex = new object();

		public event BroadcastEventHandler BroadcastStart;
		public event BroadcastEventHandler BroadcastEvent;
		public event BroadcastEventHandler BroadcastDone;
		#region constructor

		private BroadcastEventService()
		{
		}

		#endregion

		public static BroadcastEventService Instance
		{
			get
			{
				if (_instance == null)
				{
					lock (_mutex)
					{
						if (_instance == null)
						{
							_instance = new BroadcastEventService();
						}
					}
				}
				return _instance;
			}
		}



		public void Start()
		{
			if (BroadcastStart != null)
			{
				BroadcastStart (this, null);
			}
		}

		public void Broadcast(BroadcastEventArgs e)
		{
			if (BroadcastEvent != null)
			{
				BroadcastEvent(this, e);
			}
		}

		public void Finished()
		{
			if (BroadcastDone != null)
			{
				BroadcastDone(this, null);
			}
		}
	}
}
~~~~

* EventAppender
This class implements AppenderSkeleton. It is used for log4net. We need to override the Append member function to broadcast events by calling functions provided by BroadcastEventService.

~~~~{.csharp}
using System;
using log4net;
using log4net.Core;
using log4net.Appender;

namespace log4netEventBroadcast
{
	class EventAppender : AppenderSkeleton
	{
		protected override void Append(LoggingEvent loggingEvent)
		{
			// we are coupling the info with the status indication, maybe we can consider using other levels, such as Notice to indicate progress
			if (loggingEvent.Level == Level.Info)
			{
				BroadcastEventService.Instance.Broadcast(new BroadcastEventArgs
					{
						DataTime = loggingEvent.TimeStamp,
						Level = loggingEvent.Level.ToString(),
						LoggerName = loggingEvent.LoggerName,
						ThreadName = loggingEvent.ThreadName,
						Message = loggingEvent.MessageObject.ToString(),
					});
			}

		}
	}
}
~~~~

Create a folder "Configs" and add this log4net_config.xml to the folder

~~~~{.xml}
<?xml version="1.0" encoding="utf-8" ?>
<log4net>
  <!-- A1 is set to be a ConsoleAppender -->
  <appender name="A1" type="log4net.Appender.ConsoleAppender">
    <!-- A1 uses PatternLayout -->
    <layout type="log4net.Layout.PatternLayout">
      <conversionPattern value="%date [%thread] %-5level %logger - %message%newline" />
    </layout>
  </appender>
  <appender name="logFile" type="log4net.Appender.RollingFileAppender">
    <param name="File" value="c:\\log_"/>
    <param name="RollingStyle" value="Date"/>
    <param name="DatePattern" value="yyyy-MM-dd.\tx\t" />
    <param name="StaticLogFileName" value="false"/>
    <layout type="log4net.Layout.PatternLayout">
      <conversionPattern value="%date [%thread] %-5level %logger - %message%newline" />
    </layout>
    <threshold value="Info" />
  </appender>
  <!-- Specify the full path to the appender class, followed by comman, then the assembly name-->
  <appender name="EventAppender" type="LogBroadcaster.Broadcast.EventAppender, LogBroadcaster">
    <layout type="log4net.Layout.PatternLayout">
      <conversionPattern value="%d [%thread] %-5level %logger [%ndc] - %message%newline%exception" />
    </layout>
  </appender>
  <!-- Set root logger level to DEBUG and its only appender to A1 -->
  <root>
    <level value="INFO" />
    <appender-ref ref="logFile">
    </appender-ref>
    <appender-ref ref="A1">
    </appender-ref>
    <appender-ref ref="EventAppender" />
  </root>
</log4net>
~~~~

finally, add the folling line to "Properties->AssemblyInfo.cs"` [assembly: XmlConfigurator(ConfigFile = @"Configs\log4net_config.xml", Watch = true)]`. You may need to add `using log4net.Config;`

The complete project can be found on github: [https://github.com/evertqin/log4netEventBroadcast](https://github.com/evertqin/log4netEventBroadcast).
