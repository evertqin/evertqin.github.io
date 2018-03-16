---
title: sp_executesql in Transact-SQL 
date: 02/03/2016
tags: 
- Technology
- SQL
---

# Why we want to use sp_executesql
One use case for this stored procedure is when we need to do parameterized linked query using `OPENQUERY`. I could have constructed a string with the parameter decorated by some special characters such as `{{Parameter}}` (This resembles the handlebar a lot, or AngularJS) and use `EXEC` to execute the query. However, a fundamental flaw with that approach is that I will not be able to return a value since the query cannot be parameterized. With the help of sp_executesql, we are able to provide input and output parameters

<!--more-->

# How to use
Please take a look at the following query
```sql
DECLARE @LinkedServer NVARCHAR(100) = 'v2',
        @id = 1

DECLARE @InputQuery NVARCHAR(2000),
        @ParmDefinition NVARCHAR(2000),
        @TotalCount INT

SET @ValInputQuery = N'SELECT @TotalCountOut = COUNT FROM OPENQUERY(' 
                     + @LinkedServer + ',''SELECT COUNT(1) from myTable  WHERE id={id}'')' 
SET @ValInputQuery = Replace(@InputQuery, '{id}', @id) 
SET @ParmDefinition = N'@TotalCountOut int OUTPUT' 

EXECUTE sp_executesql 
  @ValInputQuery, 
  @ParmDefinition, 
  @TotalCountOut = @TotalCount output 
```

According to the [Official Document](), the query has the following format

```
sp_executesql [ @stmt = ] statement
[ 
  { , [ @params = ] N'@parameter_name data_type [ OUT | OUTPUT ][ ,...n ]' } 
     { , [ @param1 = ] 'value1' [ ,...n ] }
]
```

Simply speaking, it looks like

```sql
 EXECUTE sp_executesql 
  @InputQuery, 
  @ParmDefinition, 
  @Parameter1, @Parameter2...
```

In the code sample, we have one output parameter `@TotalCountOut`, after return, we can check the value of `@TotalCountOut`