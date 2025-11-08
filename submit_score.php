<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
  // 1️⃣ Connect to your MySQL database
  $conn = new mysqli("localhost", "root", "", "archery_club");
  if ($conn->connect_error) {
    die("❌ Connection failed: " . $conn->connect_error);
  }

  // 2️⃣ Collect form data
  $firstName  = $_POST['firstName'];
  $middleName = $_POST['middleName'];
  $lastName   = $_POST['lastName'];
  $age        = $_POST['age'];
  $gender     = $_POST['gender'];
  $club       = $_POST['club'];
  $date       = $_POST['date'];
  $roundName  = $_POST['round'];
  $distance   = $_POST['distance'];
  $target     = $_POST['target'];
  $category   = $_POST['category'];
  $division   = $_POST['division'];

  // 3️⃣ Prepare and run an insert statement
  $stmt = $conn->prepare(
    "INSERT INTO archery_scores
     (firstName, middleName, lastName, age, gender, club, date, roundName, distance, target, category, division)
     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
  );
  $stmt->bind_param(
    "sssisssiisss",
    $firstName, $middleName, $lastName, $age, $gender, $club,
    $date, $roundName, $distance, $target, $category, $division
  );

  if ($stmt->execute()) {
    echo "<h2 style='text-align:center;color:#f4c542;font-family:Poppins;'>✅ Score recorded successfully!</h2>";
    echo "<div style='text-align:center;margin-top:20px;'>
            <a href='archery-score-recording.html' style='color:#f4c542;text-decoration:none;font-weight:600;'>⬅️ Back to form</a>
          </div>";
  } else {
    echo "Error: " . $stmt->error;
  }

  $stmt->close();
  $conn->close();
} else {
  echo "No data submitted.";
}
?>
