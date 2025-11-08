import streamlit as st
import mysql.connector
from datetime import date

# --------------------
# MySQL Connection
# --------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",   # XAMPP root password
        database="archery_db"
    )

# --------------------
# Page Layout
# --------------------
st.title("🏹 Archery Club Score System")

menu = ["Home", "Add Score", "Recorder Approval", "Leaderboard"]
choice = st.sidebar.selectbox("Menu", menu)

# --------------------
# Home Page
# --------------------
if choice == "Home":
    st.subheader("Welcome to Archery Club Score System")
    st.write("Use the sidebar to navigate: Add Score, Approve Scores, or view Leaderboard.")

# --------------------
# Add Score Page
# --------------------
elif choice == "Add Score":
    st.subheader("🎯 Enter Your Score")

    with st.form(key='score_form'):
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        dob = st.date_input("Date of Birth", date.today())
        gender = st.selectbox("Gender", ["F", "M"])
        equipment_name = st.selectbox("Equipment", ["Recurve", "Compound", "Recurve Barebow", "Compound Barebow", "Longbow"])
        category_name = st.selectbox("Category", ["Female Open","Male Open","50+ Female","50+ Male",
                                                  "60+ Female","60+ Male","70+ Female","70+ Male",
                                                  "Under 21 Female","Under 21 Male","Under 18 Female","Under 18 Male",
                                                  "Under 16 Female","Under 16 Male","Under 14 Female","Under 14 Male"])
        round_name = st.text_input("Round Name")
        division_name = st.selectbox("Division", ["Recurve","Compound","Recurve Barebow","Compound Barebow","Longbow"])
        total_score = st.number_input("Total Score", min_value=0)
        submit = st.form_submit_button("Submit Score")

    if submit:
        conn = get_connection()
        cursor = conn.cursor()

        # --------------------
        # Get or insert Archer
        # --------------------
        cursor.execute("SELECT archer_id FROM Archer WHERE first_name=%s AND last_name=%s AND date_of_birth=%s",
                       (first_name, last_name, dob))
        result = cursor.fetchone()
        if result:
            archer_id = result[0]
        else:
            # Map equipment_id
            cursor.execute("SELECT equipment_id FROM Equipment WHERE name=%s", (equipment_name,))
            eq_result = cursor.fetchone()
            equipment_id = eq_result[0] if eq_result else None

            # Map category_id
            cursor.execute("SELECT category_id FROM Category WHERE name=%s", (category_name,))
            cat_result = cursor.fetchone()
            category_id = cat_result[0] if cat_result else None

            cursor.execute("""
                INSERT INTO Archer (first_name, last_name, date_of_birth, gender, default_equipment_id, category_id)
                VALUES (%s,%s,%s,%s,%s,%s)
            """, (first_name, last_name, dob, gender, equipment_id, category_id))
            archer_id = cursor.lastrowid

        # --------------------
        # Get or insert Round
        # --------------------
        cursor.execute("SELECT round_id FROM Round WHERE name=%s", (round_name,))
        r = cursor.fetchone()
        if r:
            round_id = r[0]
        else:
            cursor.execute("INSERT INTO Round (name, total_ranges) VALUES (%s,%s)", (round_name, 1))
            round_id = cursor.lastrowid

        # --------------------
        # Get or insert Division
        # --------------------
        cursor.execute("SELECT division_id FROM Division WHERE name=%s", (division_name,))
        d = cursor.fetchone()
        if d:
            division_id = d[0]
        else:
            cursor.execute("""
                INSERT INTO Division (name, category_id, equipment_id)
                VALUES (%s, %s, %s)
            """, (division_name, category_id if category_id else 1, equipment_id if equipment_id else 1))
            division_id = cursor.lastrowid

        # --------------------
        # Insert Score
        # --------------------
        cursor.execute("""
            INSERT INTO Score (archer_id, round_id, division_id, total_score, date_recorded, approved)
            VALUES (%s,%s,%s,%s,NOW(),FALSE)
        """, (archer_id, round_id, division_id, total_score))

        conn.commit()
        cursor.close()
        conn.close()
        st.success("✅ Score recorded successfully! Awaiting recorder approval.")

# --------------------
# Recorder Approval Page
# --------------------
elif choice == "Recorder Approval":
    st.subheader("🧾 Recorder Approval")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.score_id, a.first_name, a.last_name, s.total_score 
        FROM Score s
        JOIN Archer a ON s.archer_id = a.archer_id
        WHERE s.approved=FALSE
    """)
    rows = cursor.fetchall()

    for row in rows:
        approve = st.checkbox(f"{row[1]} {row[2]} - {row[3]} points", key=row[0])
        if approve:
            cursor.execute("UPDATE Score SET approved=TRUE WHERE score_id=%s", (row[0],))
            conn.commit()
            st.success(f"{row[1]} {row[2]} approved!")

    cursor.close()
    conn.close()

# --------------------
# Leaderboard Page
# --------------------
elif choice == "Leaderboard":
    st.subheader("🏆 Detailed Leaderboard")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            a.first_name,
            a.last_name,
            a.gender,
            TIMESTAMPDIFF(YEAR, a.date_of_birth, CURDATE()) AS age,
            s.total_score,
            r.name AS round_name,
            d.name AS division_name,
            e.name AS equipment_name,
            s.date_recorded
        FROM Score s
        JOIN Archer a ON s.archer_id = a.archer_id
        JOIN Division d ON s.division_id = d.division_id
        JOIN Equipment e ON d.equipment_id = e.equipment_id
        JOIN Round r ON s.round_id = r.round_id
        WHERE s.approved=TRUE
        ORDER BY s.total_score DESC
    """)

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # Prepare data for display
    leaderboard_data = []
    for i, row in enumerate(rows, start=1):
        full_name = f"{row[0]} {row[1]}"
        leaderboard_data.append({
            "Rank": i,
            "Name": full_name,
            "Gender": row[2],
            "Age": row[3],
            "Score": row[4],
            "Round": row[5],
            "Division": row[6],
            "Equipment": row[7],
            "Date": row[8].strftime("%Y-%m-%d")
        })

    # Display using Streamlit dataframe with wider view
    st.dataframe(leaderboard_data, width=1200)
