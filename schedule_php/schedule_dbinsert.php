<?php
    $p_date = $_POST["p_date"];
    $p_subject = $_POST["p_subject"];

    //database :: smartmirror
    //table :: schedule(_id[int], schedule_time[datetime], subject[varchar(200)] )
    $connect = mysqli_connect("localhost:3306","smartmirror","root","flvmfptl1");
    mysqli_set_charset($connect, "utf8");

    $insertSQL = "insert into schedule values(NULL, '$p_date', '$p_subject')";
    $insertQuery = mysqli_query($connect, $insertSQL);

    if($insertQuery)
        echo "데이터 입력 완료";
    else
        echo "데이터 입력 실패";

    mysqli_close($connect);
?>
