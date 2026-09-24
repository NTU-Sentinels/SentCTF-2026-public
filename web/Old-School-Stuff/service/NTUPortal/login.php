<?php

session_start();

if(isset($_SESSION['user']))
{
	header("Location: dashboard.php");
	exit();
}

include("includes/header.php");

if(isset($_GET['error']))
{
    echo "<p style='color:red;'>Invalid username or password.</p>";
}


?>

<h2>Staff Login</h2>

<form action="authenticate.php" method="post">

<table>

<tr>

<td width="180">

Username

</td>

<td>

<input type="text" name="username">

</td>

</tr>

<tr>

<td>

Password

</td>

<td>

<input type="password" name="password">

</td>

</tr>

<tr>

<td></td>

<td>

<input type="submit" value="Login">

</td>

</tr>

</table>

</form>

<?php
include("includes/footer.php");
?>
