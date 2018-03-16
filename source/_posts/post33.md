---
title: Convert table to delimited string
date: 02/04/2016
tags: 
- Technology
- SQL
---

Something we need to convert a table into delimited string for, say, log or exception message, there are three ways to do it in TSQL

<!--more-->

#### Aggregate with variable

```
DECLARE @Result NVARCHAR(2000) = N'' /*Important! Assign empty string to the return variable*/

SELECT @Result = @Result + CONVERT(NVARCHAR(100), ID) + N',' 
    FROM @Table
SET @Result = SUBSTRING(@Result, 0, LEN(@Result)) /* Need to remove trailing delimiter*/
```

#### Use XML PATH

```
DECLARE @Result NVARCHAR(2000) /* Initial assignment is optional */

SELECT @Result = STUFF((SELECT ',' + CONVERT(NVARCHAR(100), ID) + ',' + Description FROM @Result FOR XML PATH('')), 1, 1, '' )
```

#### Use COALESCE
  
```
DECLARE @result NVARCHAR(1000) = N''

SELECT @result = COALESCE(@result + ',', '') + description FROM targetingservice
```