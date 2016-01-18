USE [Twitter]
GO
/****** Object:  StoredProcedure [dbo].[sp_IQ_dell_pricetracker]    Script Date: 1/16/2016 8:13:09 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[sp_predict]
	@l1 AS NVARCHAR(20),
	@l2 AS NVARCHAR(20),
	@l3 AS NVARCHAR(20),
	@f2 AS INT,
	@f3 AS INT,
	@f4 AS INT
AS

SELECT TOP 10
	l4, Freq, ngram
FROM
	twitter_grouped
WHERE
	(l3 = @l3 AND ngram = 2 AND Freq >= @f2) OR
	(l2 = @l2 AND l3 = @l3 AND ngram = 3 AND Freq >= @f3) OR
	(l1 = @l1 AND l2 = @l2 AND l3 = @l3 AND ngram = 4 AND Freq >= @f4)
ORDER BY ngram DESC, Freq DESC

--EXEC sp_predict @l1='best', @l2='times', @l3='worst', @f2=10, @f3=1, @f4=1