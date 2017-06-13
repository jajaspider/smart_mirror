<?php
    $min_temp = $_POST["min_temp"];
    $max_temp = $_POST["max_temp"];

    //database :: smartmirror
    //table :: temperature(_id[int], min_temp[int], max_temp[int] )
    $connect = mysqli_connect("localhost:3306","root","flvmfptl1","smartmirror");
    mysqli_set_charset($connect, "utf8");

    $selectSQL = "select * from temperature";
    $selectQuery = mysqli_query($connect, $selectSQL);

    $selectRowCount = mysqli_num_rows($selectQuery);

    if($selectRowCount == 0) {
        $insertSQL = "insert into temperature values(NULL, '$min_temp', '$max_temp')";
        $insertQuery = mysqli_query($connect, $insertSQL);

        if($insertQuery)
            echo "온도 설정 성공";
        else
            echo "온도 설정 실패";
    } else {
        $updateSQL = "update temperature set min_temp='$min_temp', max_temp='$max_temp' where _id = 1";
        $updateQuery = mysqli_query($connect, $updateSQL);

        if($updateQuery)
            echo "온도 변경 성공";
        else
            echo "온도 변경 실패";
    }

    mysqli_close($connect);
?>
