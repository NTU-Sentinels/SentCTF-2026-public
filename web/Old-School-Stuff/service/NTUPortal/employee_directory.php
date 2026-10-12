<?php

include("includes/auth.php");
include("includes/db.php");
include("includes/header.php");

$search = "";
$result = null;

if(isset($_GET['search']))
{
    $search = trim($_GET['search']);

    $stmt = "SELECT name, department, email FROM employees ";
    $stmt .= "WHERE name LIKE '%{$search}%'";

    // Uncomment while debugging
    // echo "<pre>" . htmlspecialchars($stmt) . "</pre>";

    $result = $conn->query($stmt);

    if(!$result){
        die("MySQL Error: " . $conn->error);
    }
}

?>

<h2>Employee Directory</h2>

<div class="notice">
Search for staff members by name.
</div>

<form method="GET">

<input type="text"
       name="search"
       placeholder="Enter employee name..."
       value="<?php echo htmlspecialchars($search); ?>">

<input type="submit" value="Search">

</form>

<br>

<?php
if(!isset($_GET['search']))
{
    echo "<p>Please enter an employee name to begin searching.</p>";
}
else
{
?>

<table>

<tr>
<th>Name</th>
<th>Department</th>
<th>Email</th>
</tr>

<?php while($row = $result->fetch_assoc()) { ?>

<tr>

<td><?php echo htmlspecialchars($row['name']); ?></td>
<td><?php echo htmlspecialchars($row['department']); ?></td>
<td><?php echo htmlspecialchars($row['email']); ?></td>

</tr>

<?php } ?>

</table>

<?php
}
?>

<?php
include("includes/footer.php");
?>
