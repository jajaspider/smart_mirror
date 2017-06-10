<?php
    $current_time = date("Y-m-j H:i:s");
    $connect = mysql_connect("localhost:3306", "smartmirror", "root", "flvmfptl1");
    mysql_set_charset($connect, "utf8");

    $selectSQL = "select * from schedule where schedule_time >= '$current_time'";
    $selectResult = mysql_query($connect, $selectSQL);

    $selectRowCount = mysql_num_rows($selectResult);

    echo "rowCount : ";
    echo $selectRowCount;

    if($selectRowCount == 0) {
        echo "검색 결과가 없음";
    }else if($selectRowCount >= 1) {
        //검색된 행 존재 -> 결과 표시
        while($row = mysql_fetch_row($selectResult)) {
            echo "Schedule_Time : $row[1] ";
            echo "Subject : $row[2] ";
            echo "<br />";
        }
    }
    mysql_close($connect);
?>
