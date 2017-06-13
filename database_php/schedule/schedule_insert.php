<html>
	<head>
		<title>Schedule Insert Page</title>
	</head>

	<body>
		<h2>스케줄 등록</h2>
		<hr>
		<form method="post" action="schedule_dbinsert.php">
			날짜 : <input type="datetime-local" name="p_date" /> <br/>
			제목 : <input type="text" name="p_subject" /> <br/>
			<input type="submit" value="확인">
			<input type="reset" value="초기화">
		</form>
	</body>
</html>
