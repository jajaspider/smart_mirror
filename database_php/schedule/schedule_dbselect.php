<?php
    $connect = mysqli_connect("localhost:3306", "root", "flvmfptl1", "smartmirror");
    mysqli_set_charset($connect, "utf8");

    $selectSQL = "select * from schedule where date(schedule_time) = date(now())";
    $selectResult = mysqli_query($connect, $selectSQL);

    $selectRowCount = mysqli_num_rows($selectResult);

    if($selectRowCount == 0) {
        echo "검색 결과가 없음";
    }else if($selectRowCount >= 1) {
        //검색된 행 존재 -> 결과 표시
        while($row = mysqli_fetch_row($selectResult)) {
            echo "Schedule_Time : $row[1] ";
            echo "Subject : $row[2] ";
            echo "<br />";
        }
    }
    mysqli_close($connect);
?>
