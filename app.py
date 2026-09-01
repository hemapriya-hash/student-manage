import streamlit as st

from database import (
    create_tables,
    add_student,
    get_students,
    update_student,
    delete_students,
    add_marks,
    get_marks,
    delete_marks
)

from calculations import (
    get_grade,
    get_grade_point,
    calculate_sgpa
)


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Student Management System",
    page_icon="🎓",
    layout="wide"
)


# ---------------------------------------------------------
# CREATE DATABASE TABLES
# ---------------------------------------------------------

create_tables()


# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------

st.title("🎓 Student Management System")
st.write("Manage students, subjects, marks and calculate SGPA.")


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

st.sidebar.title("📚 Navigation")

menu = st.sidebar.radio(
    "Select an option",
    [
        "🏠 Dashboard",
        "➕ Add Student",
        "👨‍🎓 View Students",
        "✏️ Update Student",
        "🗑️ Delete Student",
        "📊 Marks & SGPA"
    ]
)


# =========================================================
# DASHBOARD
# =========================================================

if menu == "🏠 Dashboard":

    st.header("🏠 Dashboard")

    students = get_students()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "👨‍🎓 Total Students",
            len(students)
        )

    total_subjects = 0

    for student in students:
        student_id = student[0]
        marks_data = get_marks(student_id)
        total_subjects += len(marks_data)

    with col2:
        st.metric(
            "📚 Total Subjects",
            total_subjects
        )

    with col3:
        if len(students) > 0:
            st.metric(
                "📈 Average Students",
                len(students)
            )
        else:
            st.metric(
                "📈 Average Students",
                0
            )

    st.divider()

    st.subheader("Welcome 👋")

    st.write(
        """
        This Student Management System allows you to:

        - ➕ Add students
        - 👨‍🎓 View student details
        - ✏️ Update student information
        - 🗑️ Delete students
        - 📝 Add subject marks
        - ❌ Delete subjects
        - 📊 Calculate SGPA
        - 🏆 Display grades and grade points
        """
    )


# =========================================================
# ADD STUDENT
# =========================================================

elif menu == "➕ Add Student":

    st.header("➕ Add Student")

    with st.form("add_student_form"):

        name = st.text_input(
            "Student Name"
        )

        email = st.text_input(
            "Email"
        )

        course = st.text_input(
            "Course"
        )

        semester = st.text_input(
            "Semester"
        )

        roll_number = st.text_input(
            "Roll Number"
        )

        submitted = st.form_submit_button(
            "Add Student"
        )

        if submitted:

            if name == "":
                st.error("Please enter student name.")

            elif roll_number == "":
                st.error("Please enter roll number.")

            else:

                try:

                    add_student(
                        name,
                        email,
                        course,
                        semester,
                        roll_number
                    )

                    st.success(
                        "Student added successfully! 🎉"
                    )

                except Exception as e:

                    st.error(
                        f"Error: {e}"
                    )


# =========================================================
# VIEW STUDENTS
# =========================================================

elif menu == "👨‍🎓 View Students":

    st.header("👨‍🎓 Student Details")

    students = get_students()

    if not students:

        st.info(
            "No students found. Please add a student first."
        )

    else:

        for student in students:

            student_id = student[0]
            name = student[1]
            email = student[2]
            course = student[3]
            semester = student[4]
            roll_number = student[5]

            with st.expander(
                f"🎓 {name} - {roll_number}"
            ):

                col1, col2 = st.columns(2)

                with col1:

                    st.write(
                        f"**Student ID:** {student_id}"
                    )

                    st.write(
                        f"**Name:** {name}"
                    )

                    st.write(
                        f"**Email:** {email}"
                    )

                with col2:

                    st.write(
                        f"**Course:** {course}"
                    )

                    st.write(
                        f"**Semester:** {semester}"
                    )

                    st.write(
                        f"**Roll Number:** {roll_number}"
                    )

                st.divider()

                marks_data = get_marks(student_id)

                if marks_data:

                    st.write("### 📚 Subjects")

                    for mark in marks_data:

                        mark_id = mark[0]
                        subject = mark[1]
                        marks = mark[2]
                        credits = mark[3]

                        grade = get_grade(marks)
                        grade_point = get_grade_point(marks)

                        st.write(
                            f"**{subject}** | "
                            f"Marks: {marks} | "
                            f"Credits: {credits} | "
                            f"Grade: {grade} | "
                            f"Grade Point: {grade_point}"
                        )

                    sgpa = calculate_sgpa(
                        marks_data
                    )

                    st.success(
                        f"📊 SGPA: {sgpa}"
                    )

                else:

                    st.info(
                        "No marks added for this student."
                    )


# =========================================================
# UPDATE STUDENT
# =========================================================

elif menu == "✏️ Update Student":

    st.header("✏️ Update Student")

    students = get_students()

    if not students:

        st.info(
            "No students available to update."
        )

    else:

        student_options = {
            f"{student[1]} - {student[5]}": student
            for student in students
        }

        selected_student = st.selectbox(
            "Select Student",
            list(student_options.keys())
        )

        student = student_options[
            selected_student
        ]

        student_id = student[0]

        st.divider()

        with st.form("update_student_form"):

            name = st.text_input(
                "Student Name",
                value=student[1]
            )

            email = st.text_input(
                "Email",
                value=student[2] or ""
            )

            course = st.text_input(
                "Course",
                value=student[3] or ""
            )

            semester = st.text_input(
                "Semester",
                value=student[4] or ""
            )

            roll_number = st.text_input(
                "Roll Number",
                value=student[5]
            )

            update_button = st.form_submit_button(
                "Update Student"
            )

            if update_button:

                if name == "":
                    st.error(
                        "Student name cannot be empty."
                    )

                elif roll_number == "":
                    st.error(
                        "Roll number cannot be empty."
                    )

                else:

                    try:

                        update_student(
                            student_id,
                            name,
                            email,
                            course,
                            semester,
                            roll_number
                        )

                        st.success(
                            "Student updated successfully! ✅"
                        )

                        st.rerun()

                    except Exception as e:

                        st.error(
                            f"Error: {e}"
                        )


# =========================================================
# DELETE STUDENT
# =========================================================

elif menu == "🗑️ Delete Student":

    st.header("🗑️ Delete Student")

    students = get_students()

    if not students:

        st.info(
            "No students available to delete."
        )

    else:

        student_options = {
            f"{student[1]} - {student[5]}": student[0]
            for student in students
        }

        selected_student = st.selectbox(
            "Select Student",
            list(student_options.keys())
        )

        student_id = student_options[
            selected_student
        ]

        st.warning(
            "⚠️ Deleting a student will also delete "
            "all marks associated with that student."
        )

        if st.button(
            "Delete Student",
            type="primary"
        ):

            try:

                delete_students(
                    student_id
                )

                st.success(
                    "Student deleted successfully! 🗑️"
                )

                st.rerun()

            except Exception as e:

                st.error(
                    f"Error: {e}"
                )


# =========================================================
# MARKS & SGPA
# =========================================================

elif menu == "📊 Marks & SGPA":

    st.header("📊 Marks & SGPA")

    students = get_students()

    if not students:

        st.info(
            "Please add a student first."
        )

    else:

        student_options = {
            f"{student[1]} - {student[5]}": student[0]
            for student in students
        }

        selected_student = st.selectbox(
            "Select Student",
            list(student_options.keys())
        )

        student_id = student_options[
            selected_student
        ]

        st.divider()

        # -------------------------------------------------
        # ADD MARKS
        # -------------------------------------------------

        st.subheader("➕ Add Subject Marks")

        with st.form("add_marks_form"):

            subject = st.text_input(
                "Subject Name"
            )

            marks = st.number_input(
                "Marks",
                min_value=0,
                max_value=100,
                value=0,
                step=1
            )

            credits = st.number_input(
                "Credits",
                min_value=1,
                max_value=10,
                value=1,
                step=1
            )

            add_marks_button = st.form_submit_button(
                "Add Marks"
            )

            if add_marks_button:

                if subject == "":
                    st.error(
                        "Please enter subject name."
                    )

                else:

                    try:

                        add_marks(
                            student_id,
                            subject,
                            marks,
                            credits
                        )

                        st.success(
                            "Marks added successfully! ✅"
                        )

                        st.rerun()

                    except Exception as e:

                        st.error(
                            f"Error: {e}"
                        )

        st.divider()

        # -------------------------------------------------
        # DISPLAY MARKS
        # -------------------------------------------------

        marks_data = get_marks(
            student_id
        )

        if marks_data:

            st.subheader("📚 Subject Details")

            for mark in marks_data:

                mark_id = mark[0]
                subject = mark[1]
                marks = mark[2]
                credits = mark[3]

                grade = get_grade(
                    marks
                )

                grade_point = get_grade_point(
                    marks
                )

                col1, col2, col3, col4, col5 = st.columns(5)

                with col1:
                    st.write(
                        f"**Subject:** {subject}"
                    )

                with col2:
                    st.write(
                        f"**Marks:** {marks}"
                    )

                with col3:
                    st.write(
                        f"**Credits:** {credits}"
                    )

                with col4:
                    st.write(
                        f"**Grade:** {grade}"
                    )

                with col5:
                    st.write(
                        f"**Grade Point:** {grade_point}"
                    )

            st.divider()

            # -------------------------------------------------
            # SGPA
            # -------------------------------------------------

            sgpa = calculate_sgpa(
                marks_data
            )

            st.subheader("📈 SGPA")

            st.metric(
                "Current SGPA",
                sgpa
            )

        else:

            st.info(
                "No marks added for this student."
            )

        st.divider()

        # -------------------------------------------------
        # DELETE SUBJECT
        # -------------------------------------------------

        if marks_data:

            st.subheader("🗑️ Delete Subject")

            mark_options = {
                f"{mark[1]} - {mark[2]} marks":
                mark[0]
                for mark in marks_data
            }

            selected_mark = st.selectbox(
                "Select Subject",
                list(mark_options.keys())
            )

            mark_id = mark_options[
                selected_mark
            ]

            if st.button(
                "Delete Subject"
            ):

                try:

                    delete_marks(
                        mark_id
                    )

                    st.success(
                        "Subject deleted successfully. ✅"
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"Error: {e}"
                    )

        else:

            st.info(
                "No marks added for this student."
            )