<?php
    $current_time = date("Y-m-j H:i:s");
    $connect = mysqli_connect("localhost:3306", "smartmirror", "root", "flvmfptl1");
    mysqli_set_charset($connect, "utf8");

    $selectSQL = "select * from schedule where schedule_time >= '$current_time'";
    $selectResult = mysqli_query($connect, $selectSQL);

    if(mysqli_num_rows($selectResult) == 0) {
        echo "검색 결과가 없음";
    }else(mysqli_num_rows($selectResult) >= 1) {
        //검색된 행 존재 -> 결과 표시
        while($row = mysqli_fetch_array($selectResult)) {
            echo "Schedule_Time : $row['schedule_time'] ";
            echo "Subject : $row['subject'] ";
            echo "<br />";
        }
    }
    mysqli_close($connect);
?>
