<html>
	<head>
		<title>Temperature Setting Page</title>
	</head>

	<body>
		<h2>온도 설정</h2>
		<hr>
		<form method="post" action="temp_dbsetting.php">
			최저 온도 : <input type="number" name="min_temp" /> <br/>
			최대 온도 : <input type="number" name="max_temp" /> <br/>
			<input type="submit" value="확인">
			<input type="reset" value="초기화">
		</form>
	</body>
</html>
