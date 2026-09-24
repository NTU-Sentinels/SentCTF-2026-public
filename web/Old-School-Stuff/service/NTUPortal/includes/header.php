<?php
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}
?>

<!DOCTYPE html>
<html>

<head>

<title>NTU Legacy Staff Portal</title>

<link rel="stylesheet" href="assets/style.css">

</head>

<body>

<div id="wrapper">

<div id="header">

<h1>NTU Legacy Staff Portal</h1>

<p>Internal Staff Information System</p>

</div>

<div id="nav">

<?php if(isset($_SESSION['user'])) { ?>

<a href="dashboard.php">Dashboard</a>

<a href="employee_directory.php">Employee Directory</a>

<a href="announcements.php">Announcements</a>

<a href="documents.php">Documents</a>

<a href="logout.php" style="float:right;color:#990000;">Logout</a>

<?php } else { ?>

<a href="index.php">Home</a>

<a href="login.php">Login</a>

<a href="contact.php">Contact</a>

<a href="helpdesk.php">Helpdesk</a>

<?php } ?>

</div>

<?php if(isset($_SESSION['user'])) { ?>

<div style="background:#f2f2f2;padding:8px 15px;border-bottom:1px solid #aaa;">

Logged in as:
<strong><?php echo htmlspecialchars($_SESSION['user']); ?></strong>

</div>

<?php } ?>

<div id="content">
