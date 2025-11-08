<?php
// Start the session to carry data between pages
session_start();

// If form was submitted, store data in session
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $_SESSION['archeryFormData'] = [
        "fullName" => $_POST['fullName'] ?? '',
        "age"      => $_POST['age'] ?? '',
        "club"     => $_POST['club'] ?? '',
        "date"     => $_POST['date'] ?? '',
        "round"    => $_POST['round'] ?? '',
        "distance" => $_POST['distance'] ?? '',
        "target"   => $_POST['target'] ?? '',
        "category" => $_POST['category'] ?? '',
        "division" => $_POST['division'] ?? ''
    ];
}

// Retrieve session data
$data = $_SESSION['archeryFormData'] ?? null;
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Review Information</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <div class="container">
    <h1>Review Your Information</h1>
    <div id="review">
      <?php if ($data): ?>
        <p><strong>Name:</strong> <?= htmlspecialchars($data['fullName']) ?></p>
        <p><strong>Age:</strong> <?= htmlspecialchars($data['age']) ?></p>
        <p><strong>Club:</strong> <?= htmlspecialchars($data['club']) ?></p>
        <p><strong>Date:</strong> <?= htmlspecialchars($data['date']) ?></p>
        <p><strong>Round:</strong> <?= htmlspecialchars($data['round']) ?></p>
        <p><strong>Distance:</strong> <?= htmlspecialchars($data['distance']) ?> m</p>
        <p><strong>Target Face:</strong> <?= htmlspecialchars($data['target']) ?> cm</p>
        <p><strong>Category:</strong> <?= htmlspecialchars($data['category']) ?></p>
        <p><strong>Division:</strong> <?= htmlspecialchars($data['division']) ?></p>
      <?php else: ?>
        <p>No data found. Please fill the form first.</p>
      <?php endif; ?>
    </div>

    <form action="form.php" method="post" style="display:inline;">
      <button type="submit">Back to Edit</button>
    </form>

    <form action="save.php" method="post" style="display:inline;">
      <button type="submit">Confirm</button>
    </form>
  </div>
</body>
</html>
