---
title: Setup Jersey Restful service in Intellij
date: 02/01/2016
tags: 
- Technology
- Java
- Jersey
---

Having played with Nodejs for a while, I decided to try some other web framwwork for a change, having used Tomcat a little bit, I decide to try a simple java based restful service with Jersey + Tomcat. Most of the online tutorials are based on eclipse or based on maven. Here I am using Intellij with gradle. I used [this article](https://github.com/jasonray/jersey-starterkit/wiki/Create-a-"Hello-World"-jersey-project) as reference.

<!--more-->


1. Start a new project and select gradle as project type. Also choose the Web as this may come handy in the future
![Choose gradle](http://i.imgur.com/YAGZPPj.png)
2. Enter the GroupId and ArtifactId, then in the next screen, choose gradle version and JVM version (I use gradle 2.10 and JDK 1.8u72). Pick a project name then click "Finish"
3. To enable the build, we need to first declare some dependencies, here I am using maven repositories to get required dependencies

    ~~~
group 'com.sample.gradle_sample'
version '1.0-SNAPSHOT'

apply plugin: 'java'
apply plugin: 'war'

sourceCompatibility = 1.5

repositories {
    mavenCentral()
}

dependencies {
    compile 'javax.ws.rs:javax.ws.rs-api:2.0.1'
    compile 'com.sun.jersey:jersey-server:1.8'
    testCompile group: 'junit', name: 'junit', version: '4.11'
}
    ~~~
    
    We include two dependencies for now, [javax.ws.rs](https://jax-rs-spec.java.net) will enable restful endpoints by using annotation in the code. Jersey is the required library for building restful service.

4. create src/main/java/{groupId}/test.java file, replace {groupId} with the one you specified when you setup the project.

    ~~~{.java}
package com.tripplan.dev_tracker.service;

import jdk.nashorn.internal.objects.annotations.Getter;

import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

@Path("myresource")
public class MyResource {

    /**
     * Method handling HTTP GET requests. The returned object will be sent
     * to the client as "text/plain" media type.
     *
     * @return String that will be returned as a text/plain response.
     */
    @GET
    @Produces(MediaType.TEXT_PLAIN)
    public String getIt() {
        return "Got it!";
    }
}
    ~~~

5. Create src/main/webapp/WEB-INF folder, then create a file web.xml, copy the following code

    ~~~{.xml}
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://java.sun.com/xml/ns/javaee" xmlns:web="http://java.sun.com/xml/ns/javaee/web-app_2_5.xsd" xsi:schemaLocation="http://java.sun.com/xml/ns/javaee http://java.sun.com/xml/ns/javaee/web-app_2_5.xsd" id="WebApp_ID" version="2.5">
    <display-name>jersey sample</display-name>
    <servlet>
        <servlet-name>Jersey</servlet-name>
        <servlet-class>com.sun.jersey.spi.container.servlet.ServletContainer</servlet-class>
        <init-param>
            <param-name>com.sun.jersey.config.property.packages</param-name>
            <param-value>com.sample.gradle_sample.service</param-value>
        </init-param>

        <!-- the following is only needed if you want to use the built-in support
        for mapping pojo objects to json. -->
        <init-param>
            <param-name>com.sun.jersey.api.json.POJOMappingFeature</param-name>
            <param-value>true</param-value>
        </init-param>
        <load-on-startup>1</load-on-startup>
    </servlet>
    <servlet-mapping>
        <servlet-name>Jersey</servlet-name>
        <url-pattern>/rest/*</url-pattern>
    </servlet-mapping>
</web-app>
    ~~~

    To enable Jersey support, we need to tell the server some information.

    - Under `<servlet>`, we need to tell jersey where to find the packages specifying the endpoints, here the package is `com.sample.gradle_sample.service` which should match what you used for your java source file
    
    - The url-pattern is also important, in this example it is `/rest/*`, so the final endpoint will be like `{server}/rest/myresource`. 

6. Open `Gradle projects` tool window by going to View -> Tool Windows -> Gradles, click the blue "Refresh" button if there are any unresolved dependencies. Once everything is fine, excute `./gradlew war` in your project directory. This will generate a war file under ./build/libs.

    ![refresh](http://i.imgur.com/6o37hyg.png)
7. Make sure your Tomcat server is running, for setting up Tomcat, it is very straightforward, you can follow this [tutorial](http://www.vogella.com/tutorials/ApacheTomcat/article.html), or there are tons of others over Google. Copy the war file from the previous step to the {Tomcat folder}/webapp, wait a bit till Tomcat pick up the war file.
8. Now you can test it by going to `http://localhost:8080/gradle_sample-1.0-SNAPSHOT/rest/myresource`. This is ugly but you can change the name of the war file before dropping it to the Tomcat folder.

    