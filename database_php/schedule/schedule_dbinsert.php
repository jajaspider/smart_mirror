<?php
    $p_date = $_POST["p_date"] . ":00";
    $p_subject = $_POST["p_subject"];

    $p_date = str_replace("T", " ", $p_date);

    //database :: smartmirror
    //table :: schedule(_id[int], schedule_time[datetime], subject[varchar(200)] )
    $connect = mysqli_connect("localhost:3306","root","flvmfptl1","smartmirror");
    mysqli_set_charset($connect, "utf8");

    $insertSQL = "insert into schedule values(NULL, '$p_date', '$p_subject')";
    echo $insertSQL;
    $insertQuery = mysqli_query($connect, $insertSQL);

    if($insertQuery)
        echo "데이터 입력 성공";
    else
        echo "데이터 입력 실패";

    mysqli_close($connect);
?>
