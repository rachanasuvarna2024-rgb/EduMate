# ============================================================
# TEACHER MODULE
# ============================================================

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from session_utils import role_required
from db import get_db_connection


# ============================================================
# TEACHER BLUEPRINT
# ============================================================

teacher_bp = Blueprint(
    "teacher",
    __name__,
    url_prefix="/teacher"
)


# ============================================================
# TEACHER DASHBOARD
# ============================================================

@teacher_bp.route("/")
@role_required("Teacher")
def teacher_home():

    return render_template(
        "teacher/teacher_home.html"
    )

# ============================================================
# ============================================================
# QUESTION BANK
# ============================================================
# ===========================================================

# ============================================================
# ADD QUESTION
# ============================================================

@teacher_bp.route("/add_question", methods=["GET", "POST"])
@role_required("Teacher")
def add_question():

    teacher_id = session.get("user_id")

    if not teacher_id:
        flash("Teacher session not found.", "error")
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # -------------------------------------------------
    # GET TEACHER'S INSTITUTION TYPE
    # -------------------------------------------------

    cursor.execute("""
        SELECT
            i.institution_id,
            i.institution_type,
            i.institution_category
        FROM teacher t
        JOIN institution i
            ON i.institution_id = t.institution_id
        WHERE t.teacher_id = %s
    """, (teacher_id,))

    teacher_institution = cursor.fetchone()

    if not teacher_institution:
        cursor.close()
        conn.close()

        flash("Teacher institution details not found.", "error")
        return redirect(url_for("auth.login"))

    institution_type = teacher_institution["institution_type"]


    # -------------------------------------------------
    # SUBJECTS ASSIGNED TO TEACHER
    # -------------------------------------------------

    cursor.execute("""
        SELECT
            s.subject_id,
            s.subject_name,
            st.standard_name
        FROM teacher_subject ts
        JOIN subject s
            ON s.subject_id = ts.subject_id
        LEFT JOIN standard st
            ON st.standard_id = s.standard_id
        WHERE ts.teacher_id = %s
          AND s.status = 'Active'
        ORDER BY st.standard_name, s.subject_name
    """, (teacher_id,))

    subjects = cursor.fetchall()


    # -------------------------------------------------
    # CHAPTERS
    # -------------------------------------------------

    cursor.execute("""
        SELECT
            c.chapter_id,
            c.subject_id,
            c.chapter_name,
            c.chapter_number
        FROM chapter c
        JOIN teacher_subject ts
            ON ts.subject_id = c.subject_id
        WHERE ts.teacher_id = %s
          AND c.status = 'Active'
        ORDER BY
            c.subject_id,
            c.chapter_number,
            c.chapter_name
    """, (teacher_id,))

    chapters = cursor.fetchall()


    # -------------------------------------------------
    # COURSE OUTCOMES
    # ONLY FETCH THEM FOR OBE INSTITUTIONS
    # -------------------------------------------------

    course_outcomes = []

    if institution_type == "OBE":

        cursor.execute("""
            SELECT
                co.co_id,
                co.subject_id,
                co.co_code,
                co.co_description
            FROM course_outcome co
            JOIN teacher_subject ts
                ON ts.subject_id = co.subject_id
            WHERE ts.teacher_id = %s
            ORDER BY
                co.subject_id,
                co.co_code
        """, (teacher_id,))

        course_outcomes = cursor.fetchall()


    # -------------------------------------------------
    # POST
    # -------------------------------------------------

    if request.method == "POST":

        subject_id = request.form.get("subject_id")
        chapter_id = request.form.get("chapter_id")

        # CO is accepted ONLY for OBE
        co_id = request.form.get("co_id") if institution_type == "OBE" else None

        question_text = request.form.get(
            "question_text",
            ""
        ).strip()

        option_a = request.form.get(
            "option_a",
            ""
        ).strip()

        option_b = request.form.get(
            "option_b",
            ""
        ).strip()

        option_c = request.form.get(
            "option_c",
            ""
        ).strip()

        option_d = request.form.get(
            "option_d",
            ""
        ).strip()

        correct_answer = request.form.get("correct_answer")

        difficulty = request.form.get(
            "difficulty",
            "Medium"
        )

        marks = request.form.get(
            "marks",
            "1"
        )

        is_pyq = True if request.form.get("is_pyq") == "1" else False


        # -------------------------------------------------
        # IMAGE
        # -------------------------------------------------

        question_image = request.files.get("question_image")

        image_filename = None

        if question_image and question_image.filename:

            allowed_extensions = {
                "png",
                "jpg",
                "jpeg",
                "gif",
                "webp"
            }

            original_filename = question_image.filename

            extension = original_filename.rsplit(
                ".",
                1
            )[-1].lower()

            if extension not in allowed_extensions:

                flash(
                    "Invalid image format. Please upload PNG, JPG, JPEG, GIF or WEBP.",
                    "error"
                )

                cursor.close()
                conn.close()

                return render_template(
                    "teacher/add_question.html",
                    subjects=subjects,
                    chapters=chapters,
                    course_outcomes=course_outcomes,
                    institution_type=institution_type
                )

            from werkzeug.utils import secure_filename
            import os
            import uuid

            safe_filename = secure_filename(
                original_filename
            )

            image_filename = (
                str(uuid.uuid4())
                + "_"
                + safe_filename
            )

            upload_folder = os.path.join(
                "static",
                "uploads",
                "questions"
            )

            os.makedirs(
                upload_folder,
                exist_ok=True
            )

            image_path = os.path.join(
                upload_folder,
                image_filename
            )

            question_image.save(image_path)


        # -------------------------------------------------
        # BASIC VALIDATION
        # -------------------------------------------------

        if not subject_id:

            flash(
                "Please select a subject.",
                "error"
            )

            cursor.close()
            conn.close()

            return render_template(
                "teacher/add_question.html",
                subjects=subjects,
                chapters=chapters,
                course_outcomes=course_outcomes,
                institution_type=institution_type
            )


        if not question_text:

            flash(
                "Please enter the question.",
                "error"
            )

            cursor.close()
            conn.close()

            return render_template(
                "teacher/add_question.html",
                subjects=subjects,
                chapters=chapters,
                course_outcomes=course_outcomes,
                institution_type=institution_type
            )


        # -------------------------------------------------
        # TEACHER SUBJECT VALIDATION
        # -------------------------------------------------

        cursor.execute("""
            SELECT subject_id
            FROM teacher_subject
            WHERE teacher_id = %s
              AND subject_id = %s
        """, (
            teacher_id,
            subject_id
        ))

        assigned_subject = cursor.fetchone()

        if not assigned_subject:

            flash(
                "You are not assigned to the selected subject.",
                "error"
            )

            cursor.close()
            conn.close()

            return render_template(
                "teacher/add_question.html",
                subjects=subjects,
                chapters=chapters,
                course_outcomes=course_outcomes,
                institution_type=institution_type
            )


        # -------------------------------------------------
        # CHAPTER VALIDATION
        # -------------------------------------------------

        if chapter_id:

            cursor.execute("""
                SELECT chapter_id
                FROM chapter
                WHERE chapter_id = %s
                  AND subject_id = %s
                  AND status = 'Active'
            """, (
                chapter_id,
                subject_id
            ))

            valid_chapter = cursor.fetchone()

            if not valid_chapter:

                flash(
                    "Invalid chapter selected.",
                    "error"
                )

                cursor.close()
                conn.close()

                return render_template(
                    "teacher/add_question.html",
                    subjects=subjects,
                    chapters=chapters,
                    course_outcomes=course_outcomes,
                    institution_type=institution_type
                )


        # -------------------------------------------------
        # CO VALIDATION
        # ONLY FOR OBE
        # -------------------------------------------------

        if institution_type == "OBE" and co_id:

            cursor.execute("""
                SELECT co_id
                FROM course_outcome
                WHERE co_id = %s
                  AND subject_id = %s
            """, (
                co_id,
                subject_id
            ))

            valid_co = cursor.fetchone()

            if not valid_co:

                flash(
                    "Invalid Course Outcome selected.",
                    "error"
                )

                cursor.close()
                conn.close()

                return render_template(
                    "teacher/add_question.html",
                    subjects=subjects,
                    chapters=chapters,
                    course_outcomes=course_outcomes,
                    institution_type=institution_type
                )


        # -------------------------------------------------
        # MCQ VALIDATION
        # -------------------------------------------------

        if not option_a or not option_b or not option_c or not option_d:

            flash(
                "Please enter all four options.",
                "error"
            )

            cursor.close()
            conn.close()

            return render_template(
                "teacher/add_question.html",
                subjects=subjects,
                chapters=chapters,
                course_outcomes=course_outcomes,
                institution_type=institution_type
            )


        if correct_answer not in ["A", "B", "C", "D"]:

            flash(
                "Please select the correct answer.",
                "error"
            )

            cursor.close()
            conn.close()

            return render_template(
                "teacher/add_question.html",
                subjects=subjects,
                chapters=chapters,
                course_outcomes=course_outcomes,
                institution_type=institution_type
            )


        # -------------------------------------------------
        # INSERT QUESTION
        # QUESTION TYPE IS ALWAYS MCQ FOR NOW
        # -------------------------------------------------

        cursor.execute("""
            INSERT INTO question
            (
                subject_id,
                chapter_id,
                co_id,
                question_text,
                question_image,
                option_a,
                option_b,
                option_c,
                option_d,
                correct_answer,
                difficulty,
                marks,
                question_type,
                is_pyq,
                status
            )
            VALUES
            (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, 'MCQ',
                %s, 'Active'
            )
        """, (
            subject_id,
            chapter_id if chapter_id else None,
            co_id,
            question_text,
            image_filename,
            option_a,
            option_b,
            option_c,
            option_d,
            correct_answer,
            difficulty,
            marks,
            is_pyq
        ))

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            "Question added successfully to the Question Bank.",
            "success"
        )

        return redirect(
            url_for("teacher.view_questions")
        )


    # -------------------------------------------------
    # GET
    # -------------------------------------------------

    cursor.close()
    conn.close()

    return render_template(
        "teacher/add_question.html",
        subjects=subjects,
        chapters=chapters,
        course_outcomes=course_outcomes,
        institution_type=institution_type
    )


# ============================================================
# VIEW QUESTIONS
# ============================================================

@teacher_bp.route("/view_questions")
@role_required("Teacher")
def view_questions():

    teacher_id = session.get("user_id")

    if not teacher_id:
        flash("Teacher session not found.", "error")
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            q.question_id,
            q.question_text,
            q.question_image,
            q.option_a,
            q.option_b,
            q.option_c,
            q.option_d,
            q.correct_answer,
            q.difficulty,
            q.marks,
            q.question_type,
            q.is_pyq,
            q.status,

            s.subject_name,

            st.standard_name,

            c.chapter_name,
            c.chapter_number,

            co.co_code

        FROM question q

        JOIN subject s
            ON s.subject_id = q.subject_id

        JOIN teacher_subject ts
            ON ts.subject_id = q.subject_id

        LEFT JOIN standard st
            ON st.standard_id = s.standard_id

        LEFT JOIN chapter c
            ON c.chapter_id = q.chapter_id

        LEFT JOIN course_outcome co
            ON co.co_id = q.co_id

        WHERE ts.teacher_id = %s

        ORDER BY q.question_id DESC
    """, (teacher_id,))

    questions = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "teacher/view_questions.html",
        questions=questions
    )


# ============================================================
# EDIT QUESTION
# ============================================================

@teacher_bp.route(
    "/edit_question/<int:question_id>",
    methods=["GET", "POST"]
)
@role_required("Teacher")
def edit_question(question_id):

    teacher_id = session.get("user_id")

    if not teacher_id:
        flash("Teacher session not found.", "error")
        return redirect(url_for("auth.login"))


    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)


    try:

        # ====================================================
        # GET TEACHER'S INSTITUTION TYPE
        # ====================================================

        cursor.execute("""
            SELECT
                i.institution_type
            FROM teacher t
            JOIN institution i
                ON i.institution_id = t.institution_id
            WHERE t.teacher_id = %s
        """, (teacher_id,))

        teacher_info = cursor.fetchone()


        if not teacher_info:

            flash("Teacher information not found.", "error")

            cursor.close()
            conn.close()

            return redirect(
                url_for("teacher.view_questions")
            )


        institution_type = teacher_info["institution_type"]


        # ====================================================
        # GET QUESTION
        # ====================================================

        cursor.execute("""
            SELECT
                q.question_id,
                q.subject_id,
                q.chapter_id,
                q.co_id,
                q.question_text,
                q.question_image,
                q.option_a,
                q.option_b,
                q.option_c,
                q.option_d,
                q.correct_answer,
                q.difficulty,
                q.marks,
                q.question_type,
                q.is_pyq,
                q.status

            FROM question q

            JOIN teacher_subject ts
                ON ts.subject_id = q.subject_id

            WHERE q.question_id = %s
              AND ts.teacher_id = %s
        """, (
            question_id,
            teacher_id
        ))

        question = cursor.fetchone()


        if not question:

            flash(
                "Question not found or you do not have permission to edit it.",
                "error"
            )

            cursor.close()
            conn.close()

            return redirect(
                url_for("teacher.view_questions")
            )


        # ====================================================
        # GET ASSIGNED SUBJECTS
        # ====================================================

        cursor.execute("""
            SELECT
                s.subject_id,
                s.subject_name,
                st.standard_name
            FROM teacher_subject ts
            JOIN subject s
                ON s.subject_id = ts.subject_id
            LEFT JOIN standard st
                ON st.standard_id = s.standard_id
            WHERE ts.teacher_id = %s
              AND s.status = 'Active'
            ORDER BY st.standard_name, s.subject_name
        """, (teacher_id,))

        subjects = cursor.fetchall()


        # ====================================================
        # GET CHAPTERS
        # ====================================================

        cursor.execute("""
            SELECT
                c.chapter_id,
                c.subject_id,
                c.chapter_name,
                c.chapter_number
            FROM chapter c
            JOIN teacher_subject ts
                ON ts.subject_id = c.subject_id
            WHERE ts.teacher_id = %s
              AND c.status = 'Active'
            ORDER BY
                c.subject_id,
                c.chapter_number
        """, (teacher_id,))

        chapters = cursor.fetchall()


        # ====================================================
        # GET COURSE OUTCOMES - OBE ONLY
        # ====================================================

        course_outcomes = []

        if institution_type == "OBE":

            cursor.execute("""
                SELECT
                    co.co_id,
                    co.subject_id,
                    co.co_code,
                    co.co_description
                FROM course_outcome co
                JOIN teacher_subject ts
                    ON ts.subject_id = co.subject_id
                WHERE ts.teacher_id = %s
                ORDER BY co.subject_id, co.co_code
            """, (teacher_id,))

            course_outcomes = cursor.fetchall()


        # ====================================================
        # UPDATE QUESTION
        # ====================================================

        if request.method == "POST":

            subject_id = request.form.get("subject_id")

            chapter_id = request.form.get("chapter_id")

            question_text = request.form.get(
                "question_text"
            )

            option_a = request.form.get("option_a")

            option_b = request.form.get("option_b")

            option_c = request.form.get("option_c")

            option_d = request.form.get("option_d")

            correct_answer = request.form.get(
                "correct_answer"
            )

            difficulty = request.form.get("difficulty")

            marks = request.form.get("marks")

            is_pyq = 1 if request.form.get("is_pyq") else 0


            # =================================================
            # CO
            # =================================================

            if institution_type == "OBE":

                co_id = request.form.get("co_id") or None

            else:

                co_id = None


            # =================================================
            # VALIDATION
            # =================================================

            if not subject_id:

                return render_template(
                    "teacher/edit_question.html",
                    question=question,
                    subjects=subjects,
                    chapters=chapters,
                    course_outcomes=course_outcomes,
                    institution_type=institution_type,
                    error="Please select a subject."
                )


            if not chapter_id:

                return render_template(
                    "teacher/edit_question.html",
                    question=question,
                    subjects=subjects,
                    chapters=chapters,
                    course_outcomes=course_outcomes,
                    institution_type=institution_type,
                    error="Please select a chapter."
                )


            if not question_text:

                return render_template(
                    "teacher/edit_question.html",
                    question=question,
                    subjects=subjects,
                    chapters=chapters,
                    course_outcomes=course_outcomes,
                    institution_type=institution_type,
                    error="Please enter the question."
                )


            if not option_a or not option_b or not option_c or not option_d:

                return render_template(
                    "teacher/edit_question.html",
                    question=question,
                    subjects=subjects,
                    chapters=chapters,
                    course_outcomes=course_outcomes,
                    institution_type=institution_type,
                    error="All four options are required."
                )


            if correct_answer not in ["A", "B", "C", "D"]:

                return render_template(
                    "teacher/edit_question.html",
                    question=question,
                    subjects=subjects,
                    chapters=chapters,
                    course_outcomes=course_outcomes,
                    institution_type=institution_type,
                    error="Please select a valid correct answer."
                )


            # =================================================
            # CHECK SUBJECT BELONGS TO TEACHER
            # =================================================

            cursor.execute("""
                SELECT subject_id
                FROM teacher_subject
                WHERE teacher_id = %s
                  AND subject_id = %s
            """, (
                teacher_id,
                subject_id
            ))

            assigned_subject = cursor.fetchone()


            if not assigned_subject:

                return render_template(
                    "teacher/edit_question.html",
                    question=question,
                    subjects=subjects,
                    chapters=chapters,
                    course_outcomes=course_outcomes,
                    institution_type=institution_type,
                    error="You are not assigned to the selected subject."
                )


            # =================================================
            # CHECK CHAPTER BELONGS TO SUBJECT
            # =================================================

            cursor.execute("""
                SELECT chapter_id
                FROM chapter
                WHERE chapter_id = %s
                  AND subject_id = %s
                  AND status = 'Active'
            """, (
                chapter_id,
                subject_id
            ))

            valid_chapter = cursor.fetchone()


            if not valid_chapter:

                return render_template(
                    "teacher/edit_question.html",
                    question=question,
                    subjects=subjects,
                    chapters=chapters,
                    course_outcomes=course_outcomes,
                    institution_type=institution_type,
                    error="Invalid chapter selected."
                )


            # =================================================
            # CHECK CO FOR OBE
            # =================================================

            if institution_type == "OBE" and co_id:

                cursor.execute("""
                    SELECT co_id
                    FROM course_outcome
                    WHERE co_id = %s
                      AND subject_id = %s
                """, (
                    co_id,
                    subject_id
                ))

                valid_co = cursor.fetchone()


                if not valid_co:

                    return render_template(
                        "teacher/edit_question.html",
                        question=question,
                        subjects=subjects,
                        chapters=chapters,
                        course_outcomes=course_outcomes,
                        institution_type=institution_type,
                        error="Invalid Course Outcome selected."
                    )


            # =================================================
            # IMAGE HANDLING
            # =================================================

            image_filename = question["question_image"]

            remove_image = request.form.get("remove_image")

            question_image = request.files.get(
                "question_image"
            )


            # =================================================
            # REPLACE / ADD IMAGE
            # =================================================

            if question_image and question_image.filename:

                from werkzeug.utils import secure_filename
                import os
                import uuid


                allowed_extensions = {
                    "png",
                    "jpg",
                    "jpeg",
                    "gif",
                    "webp"
                }


                original_filename = secure_filename(
                    question_image.filename
                )


                extension = (
                    original_filename
                    .rsplit(".", 1)[1].lower()
                    if "." in original_filename
                    else ""
                )


                if extension not in allowed_extensions:

                    return render_template(
                        "teacher/edit_question.html",
                        question=question,
                        subjects=subjects,
                        chapters=chapters,
                        course_outcomes=course_outcomes,
                        institution_type=institution_type,
                        error="Invalid image format. Use PNG, JPG, JPEG, GIF or WEBP."
                    )


                upload_folder = os.path.join(
                    "static",
                    "uploads",
                    "questions"
                )

                os.makedirs(
                    upload_folder,
                    exist_ok=True
                )


                new_filename = (
                    uuid.uuid4().hex
                    + "."
                    + extension
                )


                question_image.save(
                    os.path.join(
                        upload_folder,
                        new_filename
                    )
                )


                # Delete old image if it exists

                if image_filename:

                    old_path = os.path.join(
                        upload_folder,
                        image_filename
                    )

                    if os.path.exists(old_path):

                        os.remove(old_path)


                image_filename = new_filename


            # =================================================
            # REMOVE EXISTING IMAGE
            # =================================================

            elif remove_image:

                if image_filename:

                    import os

                    old_path = os.path.join(
                        "static",
                        "uploads",
                        "questions",
                        image_filename
                    )

                    if os.path.exists(old_path):

                        os.remove(old_path)


                image_filename = None


            # =================================================
            # UPDATE DATABASE
            # =================================================

            cursor.execute("""
                UPDATE question
                SET
                    subject_id = %s,
                    chapter_id = %s,
                    co_id = %s,
                    question_text = %s,
                    question_image = %s,
                    option_a = %s,
                    option_b = %s,
                    option_c = %s,
                    option_d = %s,
                    correct_answer = %s,
                    difficulty = %s,
                    marks = %s,
                    question_type = 'MCQ',
                    is_pyq = %s
                WHERE question_id = %s
            """, (
                subject_id,
                chapter_id,
                co_id,
                question_text,
                image_filename,
                option_a,
                option_b,
                option_c,
                option_d,
                correct_answer,
                difficulty,
                marks,
                is_pyq,
                question_id
            ))


            conn.commit()


            cursor.close()
            conn.close()


            flash(
                "Question updated successfully.",
                "success"
            )

            return redirect(
                url_for("teacher.view_questions")
            )


        # ====================================================
        # DISPLAY EDIT PAGE
        # ====================================================

        cursor.close()
        conn.close()

        return render_template(
            "teacher/edit_question.html",
            question=question,
            subjects=subjects,
            chapters=chapters,
            course_outcomes=course_outcomes,
            institution_type=institution_type
        )


    except Exception as e:

        conn.rollback()

        cursor.close()
        conn.close()

        flash(
            "Unable to update question: " + str(e),
            "error"
        )

        return redirect(
            url_for("teacher.view_questions")
        )


# ============================================================
# DELETE QUESTION
# ============================================================

@teacher_bp.route(
    "/delete_question/<int:question_id>",
    methods=["POST"]
)
@role_required("Teacher")
def delete_question(question_id):

    teacher_id = session.get("user_id")

    if not teacher_id:
        flash("Teacher session not found.", "error")
        return redirect(url_for("auth.login"))


    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)


    try:

        # ====================================================
        # CHECK QUESTION BELONGS TO TEACHER
        # ====================================================

        cursor.execute("""
            SELECT
                q.question_id,
                q.question_image
            FROM question q

            JOIN teacher_subject ts
                ON ts.subject_id = q.subject_id

            WHERE q.question_id = %s
              AND ts.teacher_id = %s
        """, (
            question_id,
            teacher_id
        ))

        question = cursor.fetchone()


        if not question:

            flash(
                "Question not found or you do not have permission to delete it.",
                "error"
            )

            cursor.close()
            conn.close()

            return redirect(
                url_for("teacher.view_questions")
            )


        # ====================================================
        # CHECK IF QUESTION IS USED IN A TEST
        # ====================================================

        cursor.execute("""
            SELECT
                test_question_id
            FROM test_question
            WHERE question_id = %s
            LIMIT 1
        """, (
            question_id,
        ))

        used_in_test = cursor.fetchone()


        if used_in_test:

            flash(
                "This question cannot be deleted because it is already used in a test.",
                "error"
            )

            cursor.close()
            conn.close()

            return redirect(
                url_for("teacher.view_questions")
            )


        # ====================================================
        # DELETE QUESTION
        # ====================================================

        cursor.execute("""
            DELETE FROM question
            WHERE question_id = %s
        """, (
            question_id,
        ))


        # ====================================================
        # DELETE IMAGE FILE
        # ====================================================

        if question["question_image"]:

            import os

            image_path = os.path.join(
                "static",
                "uploads",
                "questions",
                question["question_image"]
            )


            if os.path.exists(image_path):

                os.remove(image_path)


        # ====================================================
        # COMMIT
        # ====================================================

        conn.commit()


        cursor.close()
        conn.close()


        flash(
            "Question deleted successfully.",
            "success"
        )


        return redirect(
            url_for("teacher.view_questions")
        )


    except Exception as e:

        conn.rollback()

        cursor.close()
        conn.close()

        flash(
            "Unable to delete question: " + str(e),
            "error"
        )

        return redirect(
            url_for("teacher.view_questions")
        )


# ============================================================
# CREATE TEST
# ============================================================

@teacher_bp.route("/create_test", methods=["GET", "POST"])
@role_required("Teacher")
def create_test():

    teacher_id = session.get("user_id")

    if not teacher_id:
        flash(
            "Teacher session not found.",
            "error"
        )

        return redirect(
            url_for("auth.login")
        )

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # --------------------------------------------------------
    # GET SUBJECTS ASSIGNED TO LOGGED-IN TEACHER
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT
            s.subject_id,
            s.subject_name,
            st.standard_name

        FROM teacher_subject ts

        JOIN subject s
            ON s.subject_id = ts.subject_id

        LEFT JOIN standard st
            ON st.standard_id = s.standard_id

        WHERE ts.teacher_id = %s
          AND s.status = 'Active'

        ORDER BY
            st.standard_name,
            s.subject_name
        """,
        (teacher_id,)
    )

    subjects = cursor.fetchall()


    # ========================================================
    # POST - CREATE TEST
    # ========================================================

    if request.method == "POST":

        subject_id = request.form.get("subject_id")
        test_name = request.form.get("test_name")
        description = request.form.get("description")

        total_marks = request.form.get("total_marks")
        duration_minutes = request.form.get("duration_minutes")

        start_datetime = request.form.get("start_datetime")
        end_datetime = request.form.get("end_datetime")


        # ----------------------------------------------------
        # BASIC VALIDATION
        # ----------------------------------------------------

        if not subject_id:
            flash(
                "Please select a subject.",
                "error"
            )

            cursor.close()
            conn.close()

            return render_template(
                "teacher/create_test.html",
                subjects=subjects
            )


        if not test_name:
            flash(
                "Please enter a test name.",
                "error"
            )

            cursor.close()
            conn.close()

            return render_template(
                "teacher/create_test.html",
                subjects=subjects
            )


        if not total_marks:
            flash(
                "Please enter total marks.",
                "error"
            )

            cursor.close()
            conn.close()

            return render_template(
                "teacher/create_test.html",
                subjects=subjects
            )


        if not duration_minutes:
            flash(
                "Please enter test duration.",
                "error"
            )

            cursor.close()
            conn.close()

            return render_template(
                "teacher/create_test.html",
                subjects=subjects
            )


        # ----------------------------------------------------
        # VERIFY SUBJECT BELONGS TO TEACHER
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT subject_id
            FROM teacher_subject
            WHERE teacher_id = %s
              AND subject_id = %s
            """,
            (
                teacher_id,
                subject_id
            )
        )

        assigned_subject = cursor.fetchone()

        if not assigned_subject:

            flash(
                "You are not assigned to the selected subject.",
                "error"
            )

            cursor.close()
            conn.close()

            return render_template(
                "teacher/create_test.html",
                subjects=subjects
            )


        # ----------------------------------------------------
        # INSERT TEST
        # ----------------------------------------------------

        cursor.execute(
            """
            INSERT INTO test
            (
                teacher_id,
                subject_id,
                test_name,
                description,
                total_marks,
                duration_minutes,
                start_datetime,
                end_datetime,
                status
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                'Draft'
            )
            """,
            (
                teacher_id,
                subject_id,
                test_name,
                description,
                total_marks,
                duration_minutes,
                start_datetime if start_datetime else None,
                end_datetime if end_datetime else None
            )
        )

        conn.commit()

        test_id = cursor.lastrowid

        cursor.close()
        conn.close()


        # ----------------------------------------------------
        # AFTER CREATION
        # ----------------------------------------------------

        flash(
            "Test created successfully. You can now add questions.",
            "success"
        )

        return redirect(
            url_for(
                "teacher.view_tests"
            )
        )


    # ========================================================
    # GET
    # ========================================================

    cursor.close()
    conn.close()

    return render_template(
        "teacher/create_test.html",
        subjects=subjects
    )

# ============================================================
# VIEW / MANAGE TESTS
# ============================================================

@teacher_bp.route("/view_tests")
@role_required("Teacher")
def view_tests():

    teacher_id = session.get("user_id")

    if not teacher_id:
        flash(
            "Teacher session not found.",
            "error"
        )

        return redirect(
            url_for("auth.login")
        )

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # --------------------------------------------------------
    # GET TESTS CREATED BY LOGGED-IN TEACHER
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT
            t.test_id,
            t.test_name,
            t.description,
            t.total_marks,
            t.duration_minutes,
            t.start_datetime,
            t.end_datetime,
            t.status,

            s.subject_name,
            st.standard_name

        FROM test t

        JOIN subject s
            ON s.subject_id = t.subject_id

        LEFT JOIN standard st
            ON st.standard_id = s.standard_id

        WHERE t.teacher_id = %s

        ORDER BY t.test_id DESC
        """,
        (teacher_id,)
    )

    tests = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "teacher/view_tests.html",
        tests=tests
    )

# ============================================================
# EDIT TEST
# ============================================================

@teacher_bp.route("/edit_test/<int:test_id>", methods=["GET", "POST"])
@role_required("Teacher")
def edit_test(test_id):

    teacher_id = session.get("user_id")

    if not teacher_id:
        flash(
            "Teacher session not found.",
            "error"
        )

        return redirect(
            url_for("auth.login")
        )

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:

        # ----------------------------------------------------
        # GET TEST DETAILS
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT
                t.test_id,
                t.teacher_id,
                t.subject_id,
                t.test_name,
                t.description,
                t.total_marks,
                t.duration_minutes,
                t.start_datetime,
                t.end_datetime,
                t.status,

                s.subject_name,
                s.standard_id,

                st.standard_name

            FROM test t

            JOIN subject s
                ON s.subject_id = t.subject_id

            LEFT JOIN standard st
                ON st.standard_id = s.standard_id

            WHERE t.test_id = %s
              AND t.teacher_id = %s
            """,
            (
                test_id,
                teacher_id
            )
        )

        test = cursor.fetchone()

        if not test:

            flash(
                "Test not found or you are not authorized to edit it.",
                "error"
            )

            cursor.close()
            conn.close()

            return redirect(
                url_for("teacher.view_tests")
            )


        # ----------------------------------------------------
        # ONLY DRAFT TESTS CAN BE EDITED
        # ----------------------------------------------------

        if test["status"] != "Draft":

            flash(
                "Only draft tests can be edited.",
                "error"
            )

            cursor.close()
            conn.close()

            return redirect(
                url_for("teacher.view_tests")
            )


        # ----------------------------------------------------
        # GET SUBJECTS ASSIGNED TO TEACHER
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT
                s.subject_id,
                s.subject_name,
                st.standard_name

            FROM teacher_subject ts

            JOIN subject s
                ON s.subject_id = ts.subject_id

            LEFT JOIN standard st
                ON st.standard_id = s.standard_id

            WHERE ts.teacher_id = %s
              AND s.status = 'Active'

            ORDER BY
                st.standard_name,
                s.subject_name
            """,
            (
                teacher_id,
            )
        )

        subjects = cursor.fetchall()


        # ====================================================
        # POST - UPDATE TEST
        # ====================================================

        if request.method == "POST":

            subject_id = request.form.get("subject_id")
            test_name = request.form.get("test_name", "").strip()
            description = request.form.get("description", "").strip()

            total_marks = request.form.get("total_marks")
            duration_minutes = request.form.get("duration_minutes")

            start_datetime = request.form.get("start_datetime")
            end_datetime = request.form.get("end_datetime")


            # ------------------------------------------------
            # BASIC VALIDATION
            # ------------------------------------------------

            if not subject_id:

                flash(
                    "Please select a subject.",
                    "error"
                )

                return render_template(
                    "teacher/edit_test.html",
                    test=test,
                    subjects=subjects
                )


            if not test_name:

                flash(
                    "Please enter a test name.",
                    "error"
                )

                return render_template(
                    "teacher/edit_test.html",
                    test=test,
                    subjects=subjects
                )


            if not total_marks:

                flash(
                    "Please enter total marks.",
                    "error"
                )

                return render_template(
                    "teacher/edit_test.html",
                    test=test,
                    subjects=subjects
                )


            if not duration_minutes:

                flash(
                    "Please enter test duration.",
                    "error"
                )

                return render_template(
                    "teacher/edit_test.html",
                    test=test,
                    subjects=subjects
                )


            # ------------------------------------------------
            # VERIFY SUBJECT IS ASSIGNED TO TEACHER
            # ------------------------------------------------

            cursor.execute(
                """
                SELECT subject_id
                FROM teacher_subject
                WHERE teacher_id = %s
                  AND subject_id = %s
                """,
                (
                    teacher_id,
                    subject_id
                )
            )

            assigned_subject = cursor.fetchone()

            if not assigned_subject:

                flash(
                    "You are not assigned to the selected subject.",
                    "error"
                )

                return render_template(
                    "teacher/edit_test.html",
                    test=test,
                    subjects=subjects
                )


            # ------------------------------------------------
            # VALIDATE START / END DATE
            # ------------------------------------------------

            if start_datetime and end_datetime:

                if start_datetime >= end_datetime:

                    flash(
                        "End date and time must be after the start date and time.",
                        "error"
                    )

                    return render_template(
                        "teacher/edit_test.html",
                        test=test,
                        subjects=subjects
                    )


            # ------------------------------------------------
            # CHECK IF SUBJECT HAS CHANGED
            # ------------------------------------------------

            old_subject_id = test["subject_id"]

            subject_changed = (
                int(subject_id) != int(old_subject_id)
            )


            # ------------------------------------------------
            # IF SUBJECT CHANGED:
            #
            # REMOVE QUESTIONS CURRENTLY ATTACHED TO TEST
            #
            # Because those questions belong to the old subject.
            # ------------------------------------------------

            if subject_changed:

                cursor.execute(
                    """
                    DELETE FROM test_question
                    WHERE test_id = %s
                    """,
                    (
                        test_id,
                    )
                )


            # ------------------------------------------------
            # UPDATE TEST
            # ------------------------------------------------

            cursor.execute(
                """
                UPDATE test

                SET
                    subject_id = %s,
                    test_name = %s,
                    description = %s,
                    total_marks = %s,
                    duration_minutes = %s,
                    start_datetime = %s,
                    end_datetime = %s

                WHERE test_id = %s
                  AND teacher_id = %s
                  AND status = 'Draft'
                """,
                (
                    subject_id,
                    test_name,
                    description if description else None,
                    total_marks,
                    duration_minutes,
                    start_datetime if start_datetime else None,
                    end_datetime if end_datetime else None,
                    test_id,
                    teacher_id
                )
            )


            conn.commit()


            # ------------------------------------------------
            # SUCCESS MESSAGE
            # ------------------------------------------------

            if subject_changed:

                flash(
                    "Test updated successfully. The subject was changed, so the previously added questions were removed. You can add questions again.",
                    "success"
                )

            else:

                flash(
                    "Test updated successfully.",
                    "success"
                )


            cursor.close()
            conn.close()

            return redirect(
                url_for(
                    "teacher.view_tests"
                )
            )


        # ====================================================
        # GET
        # ====================================================

        cursor.close()
        conn.close()

        return render_template(
            "teacher/edit_test.html",
            test=test,
            subjects=subjects
        )


    except Exception as e:

        try:
            conn.rollback()
        except Exception:
            pass

        try:
            cursor.close()
        except Exception:
            pass

        try:
            conn.close()
        except Exception:
            pass

        flash(
            f"Database error: {str(e)}",
            "error"
        )

        return redirect(
            url_for("teacher.view_tests")
        )


# ============================================================
# MANAGE QUESTIONS IN TEST
# ============================================================

@teacher_bp.route("/manage_questions/<int:test_id>", methods=["GET", "POST"])
@role_required("Teacher")
def manage_questions(test_id):

    teacher_id = session.get("user_id")

    if not teacher_id:
        flash("Teacher session not found.", "error")
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:

        # -------------------------------------------------
        # GET TEST DETAILS
        # -------------------------------------------------

        cursor.execute("""
            SELECT
                t.test_id,
                t.test_name,
                t.description,
                t.total_marks,
                t.duration_minutes,
                t.status,
                t.subject_id,
                s.subject_name,
                s.standard_id,
                st.standard_name
            FROM test t
            JOIN subject s
                ON s.subject_id = t.subject_id
            LEFT JOIN standard st
                ON st.standard_id = s.standard_id
            WHERE t.test_id = %s
              AND t.teacher_id = %s
        """, (test_id, teacher_id))

        test = cursor.fetchone()

        if not test:
            flash(
                "Test not found or you are not authorized to manage it.",
                "error"
            )
            cursor.close()
            conn.close()
            return redirect(url_for("teacher.view_tests"))

        # -------------------------------------------------
        # ADD SELECTED QUESTIONS TO TEST
        # -------------------------------------------------

        if request.method == "POST":

            question_ids = request.form.getlist("question_ids")

            if not question_ids:
                flash("Please select at least one question.", "error")
                cursor.close()
                conn.close()
                return redirect(
                    url_for("teacher.manage_questions", test_id=test_id)
                )

            # Get current last question order
            cursor.execute("""
                SELECT COALESCE(MAX(question_order), 0) AS max_order
                FROM test_question
                WHERE test_id = %s
            """, (test_id,))

            max_order = cursor.fetchone()["max_order"]

            for question_id in question_ids:

                # -------------------------------------------------
                # VERIFY QUESTION MATCHES TEST STANDARD + SUBJECT
                # -------------------------------------------------

                cursor.execute("""
                    SELECT
                        q.question_id
                    FROM question q
                    JOIN subject s
                        ON s.subject_id = q.subject_id
                    WHERE q.question_id = %s
                      AND q.subject_id = %s
                      AND s.standard_id = %s
                      AND q.status = 'Active'
                """, (
                    question_id,
                    test["subject_id"],
                    test["standard_id"]
                ))

                valid_question = cursor.fetchone()

                if not valid_question:
                    continue

                # -------------------------------------------------
                # CHECK IF ALREADY ADDED
                # -------------------------------------------------

                cursor.execute("""
                    SELECT test_question_id
                    FROM test_question
                    WHERE test_id = %s
                      AND question_id = %s
                """, (test_id, question_id))

                already_added = cursor.fetchone()

                if already_added:
                    continue

                # -------------------------------------------------
                # ADD QUESTION
                # -------------------------------------------------

                max_order += 1

                cursor.execute("""
                    INSERT INTO test_question
                    (
                        test_id,
                        question_id,
                        question_order
                    )
                    VALUES (%s, %s, %s)
                """, (
                    test_id,
                    question_id,
                    max_order
                ))

            conn.commit()

            flash(
                "Selected questions added to the test successfully.",
                "success"
            )

            cursor.close()
            conn.close()

            return redirect(
                url_for("teacher.manage_questions", test_id=test_id)
            )

        # -------------------------------------------------
        # QUESTIONS ALREADY ADDED TO TEST
        # -------------------------------------------------

        cursor.execute("""
            SELECT
                tq.test_question_id,
                tq.question_order,
                q.question_id,
                q.question_text,
                q.question_image,
                q.option_a,
                q.option_b,
                q.option_c,
                q.option_d,
                q.correct_answer,
                q.difficulty,
                q.marks,
                q.question_type,
                q.is_pyq
            FROM test_question tq
            JOIN question q
                ON q.question_id = tq.question_id
            WHERE tq.test_id = %s
            ORDER BY tq.question_order
        """, (test_id,))

        selected_questions = cursor.fetchall()

        # -------------------------------------------------
        # AVAILABLE QUESTIONS FROM QUESTION BANK
        #
        # ONLY:
        # SAME STANDARD
        # SAME SUBJECT
        # ACTIVE QUESTIONS
        # NOT ALREADY IN TEST
        # -------------------------------------------------

        cursor.execute("""
            SELECT
                q.question_id,
                q.question_text,
                q.question_image,
                q.option_a,
                q.option_b,
                q.option_c,
                q.option_d,
                q.correct_answer,
                q.difficulty,
                q.marks,
                q.question_type,
                q.is_pyq
            FROM question q
            JOIN subject s
                ON s.subject_id = q.subject_id
            JOIN standard st
                ON st.standard_id = s.standard_id
            WHERE q.status = 'Active'
              AND q.subject_id = %s
              AND s.standard_id = %s
              AND q.question_id NOT IN
              (
                  SELECT question_id
                  FROM test_question
                  WHERE test_id = %s
              )
            ORDER BY
                CASE q.difficulty
                    WHEN 'Easy' THEN 1
                    WHEN 'Medium' THEN 2
                    WHEN 'Hard' THEN 3
                    ELSE 4
                END,
                q.question_id
        """, (
            test["subject_id"],
            test["standard_id"],
            test_id
        ))

        available_questions = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template(
            "teacher/manage_questions.html",
            test=test,
            selected_questions=selected_questions,
            available_questions=available_questions
        )

    except Exception as e:

        try:
            conn.rollback()
        except Exception:
            pass

        try:
            cursor.close()
        except Exception:
            pass

        try:
            conn.close()
        except Exception:
            pass

        flash(f"Database error: {str(e)}", "error")

        return redirect(
            url_for("teacher.view_tests")
        )

# ============================================================
# REMOVE QUESTION FROM TEST
# ============================================================

@teacher_bp.route(
    "/remove_question_from_test/<int:test_id>/<int:test_question_id>",
    methods=["POST"]
)
@role_required("Teacher")
def remove_question_from_test(test_id, test_question_id):

    teacher_id = session.get("user_id")

    if not teacher_id:
        flash("Teacher session not found.", "error")
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:

        # -------------------------------------------------
        # VERIFY TEST BELONGS TO LOGGED-IN TEACHER
        # -------------------------------------------------

        cursor.execute("""
            SELECT test_id
            FROM test
            WHERE test_id = %s
              AND teacher_id = %s
        """, (test_id, teacher_id))

        test = cursor.fetchone()

        if not test:
            flash(
                "Test not found or you are not authorized to manage it.",
                "error"
            )

            cursor.close()
            conn.close()

            return redirect(url_for("teacher.view_tests"))

        # -------------------------------------------------
        # VERIFY QUESTION EXISTS IN THIS TEST
        # -------------------------------------------------

        cursor.execute("""
            SELECT test_question_id
            FROM test_question
            WHERE test_question_id = %s
              AND test_id = %s
        """, (test_question_id, test_id))

        test_question = cursor.fetchone()

        if not test_question:
            flash(
                "Question not found in this test.",
                "error"
            )

            cursor.close()
            conn.close()

            return redirect(
                url_for(
                    "teacher.manage_questions",
                    test_id=test_id
                )
            )

        # -------------------------------------------------
        # REMOVE QUESTION
        # -------------------------------------------------

        cursor.execute("""
            DELETE FROM test_question
            WHERE test_question_id = %s
              AND test_id = %s
        """, (test_question_id, test_id))

        conn.commit()

        flash(
            "Question removed from the test successfully.",
            "success"
        )

        cursor.close()
        conn.close()

        return redirect(
            url_for(
                "teacher.manage_questions",
                test_id=test_id
            )
        )

    except Exception as e:

        try:
            conn.rollback()
        except Exception:
            pass

        try:
            cursor.close()
        except Exception:
            pass

        try:
            conn.close()
        except Exception:
            pass

        flash(
            f"Database error: {str(e)}",
            "error"
        )

        return redirect(
            url_for(
                "teacher.manage_questions",
                test_id=test_id
            )
        )

# ============================================================
# PUBLISH TEST
# ============================================================

@teacher_bp.route("/publish_test/<int:test_id>", methods=["POST"])
@role_required("Teacher")
def publish_test(test_id):

    teacher_id = session.get("user_id")

    if not teacher_id:
        flash(
            "Teacher session not found.",
            "error"
        )
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:

        # -------------------------------------------------
        # CHECK TEST BELONGS TO TEACHER
        # -------------------------------------------------

        cursor.execute("""
            SELECT
                test_id,
                test_name,
                status
            FROM test
            WHERE test_id = %s
              AND teacher_id = %s
        """, (test_id, teacher_id))

        test = cursor.fetchone()

        if not test:

            flash(
                "Test not found or you are not authorized to publish it.",
                "error"
            )

            cursor.close()
            conn.close()

            return redirect(
                url_for("teacher.view_tests")
            )

        # -------------------------------------------------
        # CHECK CURRENT STATUS
        # -------------------------------------------------

        if test["status"] != "Draft":

            flash(
                "Only draft tests can be published.",
                "error"
            )

            cursor.close()
            conn.close()

            return redirect(
                url_for("teacher.view_tests")
            )

        # -------------------------------------------------
        # CHECK WHETHER QUESTIONS HAVE BEEN ADDED
        # -------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS question_count
            FROM test_question
            WHERE test_id = %s
        """, (test_id,))

        result = cursor.fetchone()

        question_count = result["question_count"]

        if question_count == 0:

            flash(
                "Cannot publish the test because no questions have been added.",
                "error"
            )

            cursor.close()
            conn.close()

            return redirect(
                url_for(
                    "teacher.manage_questions",
                    test_id=test_id
                )
            )

        # -------------------------------------------------
        # PUBLISH TEST
        # -------------------------------------------------

        cursor.execute("""
            UPDATE test
            SET status = 'Published'
            WHERE test_id = %s
              AND teacher_id = %s
        """, (test_id, teacher_id))

        conn.commit()

        flash(
            f"Test '{test['test_name']}' published successfully.",
            "success"
        )

        cursor.close()
        conn.close()

        return redirect(
            url_for("teacher.view_tests")
        )

    except Exception as e:

        try:
            conn.rollback()
        except Exception:
            pass

        try:
            cursor.close()
        except Exception:
            pass

        try:
            conn.close()
        except Exception:
            pass

        flash(
            f"Database error: {str(e)}",
            "error"
        )

        return redirect(
            url_for("teacher.view_tests")
        )
# ============================================================
# STUDENT RESULTS
# ============================================================

# ---------------------------------
# STUDENT RESULTS
# ---------------------------------
@teacher_bp.route("/student_results")
@role_required("Teacher")
def student_results():

    teacher_id = session.get("user_id")

    if not teacher_id:
        flash("Teacher session not found.", "error")
        return redirect(url_for("auth.login_page"))

    # Get selected test from URL
    selected_test_id = request.args.get("test_id", type=int)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:

        # -----------------------------------------
        # 1. GET TEACHER'S TESTS
        # -----------------------------------------
        cursor.execute("""
            SELECT
                t.test_id,
                t.test_name,
                t.total_marks,
                sub.subject_name

            FROM test t

            JOIN subject sub
                ON sub.subject_id = t.subject_id

            WHERE t.teacher_id = %s

            ORDER BY t.test_id DESC
        """, (teacher_id,))

        tests = cursor.fetchall()

        selected_test = None
        results = []

        # -----------------------------------------
        # 2. GET SELECTED TEST DETAILS
        # -----------------------------------------
        if selected_test_id:

            cursor.execute("""
                SELECT
                    t.test_id,
                    t.test_name,
                    t.total_marks,
                    sub.subject_name

                FROM test t

                JOIN subject sub
                    ON sub.subject_id = t.subject_id

                WHERE t.test_id = %s
                  AND t.teacher_id = %s
            """, (selected_test_id, teacher_id))

            selected_test = cursor.fetchone()

            # -----------------------------------------
            # 3. GET STUDENT RESULTS FOR SELECTED TEST
            # -----------------------------------------
            if selected_test:

                cursor.execute("""
                    SELECT
                        ta.attempt_id,

                        s.student_name,
                        s.email,

                        ta.score,

                        ROUND(
                            (
                                ta.score /
                                NULLIF(t.total_marks, 0)
                            ) * 100,
                            2
                        ) AS percentage,

                        ta.started_at,
                        ta.submitted_at,
                        ta.status

                    FROM test_attempt ta

                    JOIN student s
                        ON s.student_id = ta.student_id

                    JOIN test t
                        ON t.test_id = ta.test_id

                    WHERE t.test_id = %s
                      AND t.teacher_id = %s
                      AND ta.status = 'Submitted'

                    ORDER BY
                        ta.submitted_at DESC

                """, (selected_test_id, teacher_id))

                results = cursor.fetchall()

            else:

                flash(
                    "The selected test was not found.",
                    "error"
                )

                selected_test_id = None

        # -----------------------------------------
        # 4. RENDER PAGE
        # -----------------------------------------
        return render_template(
            "teacher/student_results.html",
            tests=tests,
            selected_test_id=selected_test_id,
            selected_test=selected_test,
            results=results
        )

    except Exception as e:

        flash(
            f"Database error: {str(e)}",
            "error"
        )

        return redirect(
            url_for("teacher.teacher_home")
        )

    finally:

        cursor.close()
        conn.close()

# ============================================================
# CLASS ANALYTICS
# ============================================================
# ---------------------------------
# CLASS ANALYTICS
# ---------------------------------
@teacher_bp.route("/class_analytics")
@role_required("Teacher")
def class_analytics():

    teacher_id = session.get("user_id")

    if not teacher_id:
        flash("Teacher session not found.", "error")
        return redirect(url_for("auth.login_page"))

    # Get selected test from URL
    selected_test_id = request.args.get("test_id", type=int)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:

        # ---------------------------------
        # 1. GET TEACHER'S TESTS
        # ---------------------------------
        cursor.execute("""
            SELECT
                t.test_id,
                t.test_name,
                t.total_marks,
                sub.subject_name
            FROM test t
            JOIN subject sub
                ON sub.subject_id = t.subject_id
            WHERE t.teacher_id = %s
            ORDER BY t.test_id DESC
        """, (teacher_id,))

        tests = cursor.fetchall()

        # ---------------------------------
        # DEFAULT VALUES
        # ---------------------------------
        overview = {
            "total_students": 0,
            "tests_completed": 0,
            "average_percentage": 0,
            "highest_percentage": 0
        }

        best_student = None
        worst_student = None
        student_performance = []
        weak_topics = []
        selected_test = None

        # ---------------------------------
        # 2. ANALYTICS FOR SELECTED TEST
        # ---------------------------------
        if selected_test_id:

            # ---------------------------------
            # CHECK THAT TEST BELONGS TO TEACHER
            # ---------------------------------
            cursor.execute("""
                SELECT
                    t.test_id,
                    t.test_name,
                    t.total_marks,
                    sub.subject_name
                FROM test t
                JOIN subject sub
                    ON sub.subject_id = t.subject_id
                WHERE t.test_id = %s
                  AND t.teacher_id = %s
            """, (selected_test_id, teacher_id))

            selected_test = cursor.fetchone()

            # ---------------------------------
            # INVALID TEST
            # ---------------------------------
            if not selected_test:

                flash(
                    "The selected test was not found.",
                    "error"
                )

                selected_test_id = None

            else:

                # ---------------------------------
                # 3. TEST OVERVIEW
                # ---------------------------------
                cursor.execute("""
                    SELECT
                        COUNT(DISTINCT ta.student_id)
                            AS total_students,

                        COUNT(DISTINCT ta.attempt_id)
                            AS tests_completed,

                        ROUND(
                            AVG(
                                (
                                    ta.score /
                                    NULLIF(t.total_marks, 0)
                                ) * 100
                            ),
                            2
                        ) AS average_percentage,

                        ROUND(
                            MAX(
                                (
                                    ta.score /
                                    NULLIF(t.total_marks, 0)
                                ) * 100
                            ),
                            2
                        ) AS highest_percentage

                    FROM test_attempt ta

                    JOIN test t
                        ON t.test_id = ta.test_id

                    WHERE t.test_id = %s
                      AND t.teacher_id = %s
                      AND ta.status = 'Submitted'
                """, (selected_test_id, teacher_id))

                overview = cursor.fetchone()

                # ---------------------------------
                # 4. STUDENT-WISE PERFORMANCE
                # ---------------------------------
                cursor.execute("""
                    SELECT
                        s.student_id,
                        s.student_name,
                        s.email,

                        ta.score,

                        t.total_marks,

                        ROUND(
                            (
                                ta.score /
                                NULLIF(t.total_marks, 0)
                            ) * 100,
                            2
                        ) AS average_percentage

                    FROM test_attempt ta

                    JOIN student s
                        ON s.student_id = ta.student_id

                    JOIN test t
                        ON t.test_id = ta.test_id

                    WHERE t.test_id = %s
                      AND t.teacher_id = %s
                      AND ta.status = 'Submitted'

                    ORDER BY average_percentage DESC
                """, (selected_test_id, teacher_id))

                student_performance = cursor.fetchall()

                # ---------------------------------
                # 5. HIGHEST-PERFORMING STUDENT
                # ---------------------------------
                if student_performance:
                    best_student = student_performance[0]

                # ---------------------------------
                # 6. LOWEST-PERFORMING STUDENT
                # ---------------------------------
                if student_performance:
                    worst_student = student_performance[-1]

                # ---------------------------------
                # 7. TOPICS NEEDING ATTENTION
                # ---------------------------------
                cursor.execute("""
                    SELECT
                        c.chapter_id,
                        c.chapter_name,

                        COUNT(DISTINCT ta.student_id)
                            AS students_weak,

                        COUNT(*)
                            AS incorrect_answers

                    FROM student_answer sa

                    JOIN test_attempt ta
                        ON ta.attempt_id = sa.attempt_id

                    JOIN test t
                        ON t.test_id = ta.test_id

                    JOIN question q
                        ON q.question_id = sa.question_id

                    JOIN chapter c
                        ON c.chapter_id = q.chapter_id

                    WHERE t.test_id = %s
                      AND t.teacher_id = %s
                      AND ta.status = 'Submitted'
                      AND sa.is_correct = 0

                    GROUP BY
                        c.chapter_id,
                        c.chapter_name

                    ORDER BY
                        students_weak DESC,
                        incorrect_answers DESC
                """, (selected_test_id, teacher_id))

                weak_topics = cursor.fetchall()

        # ---------------------------------
        # 8. RENDER PAGE
        # ---------------------------------
        return render_template(
            "teacher/class_analytics.html",
            tests=tests,
            selected_test_id=selected_test_id,
            selected_test=selected_test,
            overview=overview,
            best_student=best_student,
            worst_student=worst_student,
            student_performance=student_performance,
            weak_topics=weak_topics
        )

    except Exception as e:

        flash(
            f"Database error: {str(e)}",
            "error"
        )

        return redirect(
            url_for("teacher.teacher_home")
        )

    finally:

        cursor.close()
        conn.close()

# ============================================================
# PROFILE
# ============================================================

@teacher_bp.route("/teacher_profile")
@role_required("Teacher")
def teacher_profile():

    return "Teacher Profile Page"

