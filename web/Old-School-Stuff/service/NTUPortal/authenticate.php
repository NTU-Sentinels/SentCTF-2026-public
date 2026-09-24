<?php

session_start();
include("includes/db.php");

$username = $_POST['username'] ?? "";
$password = $_POST['password'] ?? "";

$stmt = $conn->prepare("SELECT username FROM users WHERE username=? AND password=?");
$stmt->bind_param("ss",$username,$password);

$stmt->execute();

$result = $stmt->get_result();

if($result->num_rows == 1){

    $_SESSION['user']=$username;

    header("Location: dashboard.php");

}else{

    header("Location: login.php?error=1");

}
