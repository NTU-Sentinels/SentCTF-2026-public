<?php
session_start();

if(!isset($_SESSION['user']))
{
    header("Location: login.php");
    exit();
}

include("includes/header.php");
?>

<h2>Welcome,
<?php echo $_SESSION['user']; ?>
</h2>

<div class="panel">

<div class="panel-header">

Staff Services

</div>

<div class="panel-body">

<ul>

<li><a href="employee_directory.php">Employee Directory</a></li>

<li><a href="payroll.php">Payroll</a></li>

<li><a href="leave.php">Leave Management</a></li>

<li><a href="documents.php">Documents</a></li>

<li><a href="announcements.php">Announcements</a></li>

</ul>

</div>

</div>

<?php
include("includes/footer.php");
?>
