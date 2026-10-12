<?php

$host = "127.0.0.1";
$user = "portaluser";
$pass = "portalpass";
$dbname = "legacy_portal";

$conn = new mysqli($host, $user, $pass, $dbname);

if ($conn->connect_error) {
    die("Database connection failed: " . $conn->connect_error);
}
?>
