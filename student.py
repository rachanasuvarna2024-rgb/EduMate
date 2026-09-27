from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from session_utils import role_required
from db import get_db_connection


# ---------------------------------
# STUDENT BLUEPRINT
# ---------------------------------
student_bp = Blueprint(
    "student",
    __name__,
    url_prefix="/student"
)

# ---------------------------------
# STUDENT DASHBOARD
# ---------------------------------
@student_bp.route("/")
@role_required("Student")
def student_home():

    student_id = session.get("user_id")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT student_name
        FROM student
        WHERE student_id = %s
    """, (student_id,))

    student = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        "student/student_home.html",
        student=student
    )

# ---------------------------------
# AVAILABLE TESTS
# ---------------------------------
@student_bp.route("/available_tests")
@role_required("Student")
def available_tests():

    student_id = session.get("user_id")

    conn = None
    cursor = None

    try:

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                t.test_id,
                t.test_name,
                t.description,
                t.total_marks,
                t.duration_minutes,

                sub.subject_name AS subject_name,

                st.standard_name AS standard_name,

                (
                    SELECT ta.status
                    FROM test_attempt ta
                    WHERE ta.test_id = t.test_id
                      AND ta.student_id = %s
                      AND ta.status = 'In Progress'
                    ORDER BY ta.attempt_id DESC
                    LIMIT 1
                ) AS attempt_status,

                (
                    SELECT ta.attempt_id
                    FROM test_attempt ta
                    WHERE ta.test_id = t.test_id
                      AND ta.student_id = %s
                      AND ta.status = 'In Progress'
                    ORDER BY ta.attempt_id DESC
                    LIMIT 1
                ) AS attempt_id

            FROM test t

            JOIN subject sub
                ON sub.subject_id = t.subject_id

            JOIN standard st
                ON st.standard_id = sub.standard_id

            JOIN student stu
                ON stu.standard_id = st.standard_id
               AND stu.institution_id = st.institution_id

            WHERE t.status = 'Published'

              AND stu.student_id = %s

              AND NOT EXISTS (
                    SELECT 1
                    FROM test_attempt ta2
                    WHERE ta2.test_id = t.test_id
                      AND ta2.student_id = %s
                      AND ta2.status = 'Submitted'
              )

            ORDER BY t.test_id DESC

        """, (
            student_id,
            student_id,
            student_id,
            student_id
        ))

        tests = cursor.fetchall()

        return render_template(
            "student/available_tests.html",
            tests=tests
        )

    except Exception as e:

        print("\n========== AVAILABLE TESTS ERROR ==========")
        print(e)
        print("===========================================\n")

        flash(
            "Unable to load available tests.",
            "error"
        )

        return redirect(
            url_for("student.student_home")
        )

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# ---------------------------------
# START / CONTINUE TEST
# ---------------------------------
@student_bp.route("/start_test/<int:test_id>")
@role_required("Student")
def start_test(test_id):

    student_id = session.get("user_id")

    conn = None
    cursor = None

    try:

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # ---------------------------------
        # GET TEST DETAILS
        #
        # IMPORTANT:
        # Test must belong to the student's
        # institution AND standard.
        # ---------------------------------
        cursor.execute("""
            SELECT
                t.test_id,
                t.test_name,
                t.description,
                t.total_marks,
                t.duration_minutes,

                sub.subject_name AS subject_name,

                st.standard_name AS standard_name

            FROM test t

            JOIN subject sub
                ON sub.subject_id = t.subject_id

            JOIN standard st
                ON st.standard_id = sub.standard_id

            JOIN student stu
                ON stu.standard_id = st.standard_id
               AND stu.institution_id = st.institution_id

            WHERE t.test_id = %s
              AND t.status = 'Published'
              AND stu.student_id = %s

        """, (
            test_id,
            student_id
        ))

        test = cursor.fetchone()

        if not test:

            flash(
                "Test not found or is not available for your class.",
                "error"
            )

            return redirect(
                url_for("student.available_tests")
            )

        # ---------------------------------
        # CHECK IF STUDENT ALREADY SUBMITTED
        # ---------------------------------
        cursor.execute("""
            SELECT
                attempt_id
            FROM test_attempt
            WHERE test_id = %s
              AND student_id = %s
              AND status = 'Submitted'
            ORDER BY attempt_id DESC
            LIMIT 1
        """, (
            test_id,
            student_id
        ))

        submitted_attempt = cursor.fetchone()

        if submitted_attempt:

            return redirect(
                url_for(
                    "student.test_result",
                    attempt_id=submitted_attempt["attempt_id"]
                )
            )

        # ---------------------------------
        # FIND EXISTING IN-PROGRESS ATTEMPT
        # ---------------------------------
        cursor.execute("""
            SELECT
                attempt_id,
                started_at
            FROM test_attempt
            WHERE test_id = %s
              AND student_id = %s
              AND status = 'In Progress'
            ORDER BY attempt_id DESC
            LIMIT 1
        """, (
            test_id,
            student_id
        ))

        attempt = cursor.fetchone()

        # ---------------------------------
        # CREATE NEW ATTEMPT IF NEEDED
        # ---------------------------------
        if not attempt:

            cursor.execute("""
                INSERT INTO test_attempt
                (
                    test_id,
                    student_id,
                    started_at,
                    status,
                    score
                )
                VALUES
                (
                    %s,
                    %s,
                    NOW(),
                    'In Progress',
                    0
                )
            """, (
                test_id,
                student_id
            ))

            conn.commit()

            attempt_id = cursor.lastrowid

        else:

            attempt_id = attempt["attempt_id"]

        # ---------------------------------
        # GET QUESTIONS
        # ---------------------------------
        cursor.execute("""
            SELECT
                q.question_id,
                q.question_text,
                q.question_image,
                q.option_a,
                q.option_b,
                q.option_c,
                q.option_d,
                q.marks,
                q.question_type

            FROM test_question tq

            JOIN question q
                ON q.question_id = tq.question_id

            WHERE tq.test_id = %s

            ORDER BY tq.question_order ASC
        """, (
            test_id,
        ))

        questions = cursor.fetchall()

        # ---------------------------------
        # GET SAVED ANSWERS
        # ---------------------------------
        cursor.execute("""
            SELECT
                question_id,
                selected_answer
            FROM student_answer
            WHERE attempt_id = %s
        """, (
            attempt_id,
        ))

        saved_answer_rows = cursor.fetchall()

        saved_answers = {}

        for row in saved_answer_rows:

            saved_answers[
                row["question_id"]
            ] = row["selected_answer"]

        return render_template(
            "student/start_test.html",
            test=test,
            questions=questions,
            attempt_id=attempt_id,
            saved_answers=saved_answers
        )

    except Exception as e:

        print("\n========== START TEST ERROR ==========")
        print(e)
        print("======================================\n")

        flash(
            "Unable to start the test.",
            "error"
        )

        return redirect(
            url_for("student.available_tests")
        )

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# ---------------------------------
# SAVE ANSWER
# ---------------------------------
@student_bp.route("/save_answer", methods=["POST"])
@role_required("Student")
def save_answer():

    student_id = session.get("user_id")

    conn = None
    cursor = None

    try:

        data = request.get_json()

        if not data:

            return jsonify({
                "success": False,
                "message": "Invalid request."
            }), 400

        attempt_id = data.get("attempt_id")
        question_id = data.get("question_id")
        selected_answer = data.get("selected_answer")

        if not attempt_id or not question_id or not selected_answer:

            return jsonify({
                "success": False,
                "message": "Missing answer information."
            }), 400

        selected_answer = selected_answer.upper()

        if selected_answer not in ["A", "B", "C", "D"]:

            return jsonify({
                "success": False,
                "message": "Invalid answer."
            }), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # ---------------------------------
        # VERIFY ATTEMPT
        # ---------------------------------
        cursor.execute("""
            SELECT
                attempt_id,
                test_id
            FROM test_attempt
            WHERE attempt_id = %s
              AND student_id = %s
              AND status = 'In Progress'
        """, (
            attempt_id,
            student_id
        ))

        attempt = cursor.fetchone()

        if not attempt:

            return jsonify({
                "success": False,
                "message": "Invalid or completed attempt."
            }), 403

        # ---------------------------------
        # VERIFY QUESTION
        # ---------------------------------
        cursor.execute("""
            SELECT
                tq.question_id
            FROM test_question tq
            WHERE tq.test_id = %s
              AND tq.question_id = %s
        """, (
            attempt["test_id"],
            question_id
        ))

        question = cursor.fetchone()

        if not question:

            return jsonify({
                "success": False,
                "message": "Question does not belong to this test."
            }), 400

        # ---------------------------------
        # CHECK EXISTING ANSWER
        # ---------------------------------
        cursor.execute("""
            SELECT
                answer_id
            FROM student_answer
            WHERE attempt_id = %s
              AND question_id = %s
            LIMIT 1
        """, (
            attempt_id,
            question_id
        ))

        existing_answer = cursor.fetchone()

        if existing_answer:

            cursor.execute("""
                UPDATE student_answer
                SET selected_answer = %s
                WHERE answer_id = %s
            """, (
                selected_answer,
                existing_answer["answer_id"]
            ))

        else:

            cursor.execute("""
                INSERT INTO student_answer
                (
                    attempt_id,
                    question_id,
                    selected_answer,
                    is_correct,
                    marks_obtained
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    NULL,
                    0
                )
            """, (
                attempt_id,
                question_id,
                selected_answer
            ))

        conn.commit()

        return jsonify({
            "success": True
        })

    except Exception as e:

        if conn:
            conn.rollback()

        print("\n========== SAVE ANSWER ERROR ==========")
        print(e)
        print("=======================================\n")

        return jsonify({
            "success": False,
            "message": "Unable to save answer."
        }), 500

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# ---------------------------------
# SUBMIT TEST
# ---------------------------------
@student_bp.route("/submit_test/<int:test_id>", methods=["POST"])
@role_required("Student")
def submit_test(test_id):

    student_id = session.get("user_id")

    conn = None
    cursor = None

    try:

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # ---------------------------------
        # VERIFY TEST IS AVAILABLE TO
        # THIS STUDENT
        # ---------------------------------
        cursor.execute("""
            SELECT
                t.test_id
            FROM test t

            JOIN subject sub
                ON sub.subject_id = t.subject_id

            JOIN standard st
                ON st.standard_id = sub.standard_id

            JOIN student stu
                ON stu.standard_id = st.standard_id
               AND stu.institution_id = st.institution_id

            WHERE t.test_id = %s
              AND t.status = 'Published'
              AND stu.student_id = %s

        """, (
            test_id,
            student_id
        ))

        valid_test = cursor.fetchone()

        if not valid_test:

            flash(
                "This test is not available for your class.",
                "error"
            )

            return redirect(
                url_for("student.available_tests")
            )

        # ---------------------------------
        # GET CURRENT ATTEMPT
        # ---------------------------------
        cursor.execute("""
            SELECT
                attempt_id
            FROM test_attempt
            WHERE test_id = %s
              AND student_id = %s
              AND status = 'In Progress'
            ORDER BY attempt_id DESC
            LIMIT 1
        """, (
            test_id,
            student_id
        ))

        attempt = cursor.fetchone()

        if not attempt:

            # ---------------------------------
            # ALREADY SUBMITTED?
            # ---------------------------------
            cursor.execute("""
                SELECT
                    attempt_id
                FROM test_attempt
                WHERE test_id = %s
                  AND student_id = %s
                  AND status = 'Submitted'
                ORDER BY attempt_id DESC
                LIMIT 1
            """, (
                test_id,
                student_id
            ))

            submitted_attempt = cursor.fetchone()

            if submitted_attempt:

                return redirect(
                    url_for(
                        "student.test_result",
                        attempt_id=submitted_attempt["attempt_id"]
                    )
                )

            flash(
                "No active test attempt found.",
                "error"
            )

            return redirect(
                url_for("student.available_tests")
            )

        attempt_id = attempt["attempt_id"]

        # ---------------------------------
        # GET QUESTIONS
        # ---------------------------------
        cursor.execute("""
            SELECT
                q.question_id,
                q.correct_answer,
                q.marks

            FROM test_question tq

            JOIN question q
                ON q.question_id = tq.question_id

            WHERE tq.test_id = %s
        """, (
            test_id,
        ))

        questions = cursor.fetchall()

        total_score = 0

        # ---------------------------------
        # CALCULATE RESULT
        # ---------------------------------
        for question in questions:

            question_id = question["question_id"]
            correct_answer = question["correct_answer"]
            question_marks = question["marks"]

            cursor.execute("""
                SELECT
                    answer_id,
                    selected_answer
                FROM student_answer
                WHERE attempt_id = %s
                  AND question_id = %s
                LIMIT 1
            """, (
                attempt_id,
                question_id
            ))

            answer = cursor.fetchone()

            if answer and answer["selected_answer"]:

                selected_answer = answer["selected_answer"]

                is_correct = (
                    correct_answer is not None
                    and selected_answer.upper() == correct_answer.upper()
                )

                if is_correct:

                    marks_obtained = question_marks
                    total_score += float(question_marks)

                else:

                    marks_obtained = 0

                cursor.execute("""
                    UPDATE student_answer
                    SET
                        is_correct = %s,
                        marks_obtained = %s
                    WHERE answer_id = %s
                """, (
                    1 if is_correct else 0,
                    marks_obtained,
                    answer["answer_id"]
                ))

            else:

                cursor.execute("""
                    INSERT INTO student_answer
                    (
                        attempt_id,
                        question_id,
                        selected_answer,
                        is_correct,
                        marks_obtained
                    )
                    VALUES
                    (
                        %s,
                        %s,
                        NULL,
                        0,
                        0
                    )
                """, (
                    attempt_id,
                    question_id
                ))

        # ---------------------------------
        # MARK ATTEMPT AS SUBMITTED
        # ---------------------------------
        cursor.execute("""
            UPDATE test_attempt
            SET
                submitted_at = NOW(),
                score = %s,
                status = 'Submitted'
            WHERE attempt_id = %s
              AND student_id = %s
              AND test_id = %s
              AND status = 'In Progress'
        """, (
            total_score,
            attempt_id,
            student_id,
            test_id
        ))

        if cursor.rowcount != 1:

            conn.rollback()

            flash(
                "Test could not be submitted. Please try again.",
                "error"
            )

            return redirect(
                url_for(
                    "student.available_tests"
                )
            )

        conn.commit()

        return redirect(
            url_for(
                "student.test_result",
                attempt_id=attempt_id
            )
        )

    except Exception as e:

        if conn:
            conn.rollback()

        print("\n========== SUBMIT TEST ERROR ==========")
        import traceback
        traceback.print_exc()
        print("=======================================\n")

        flash(
            "An error occurred while submitting the test.",
            "error"
        )

        return redirect(
            url_for(
                "student.available_tests"
            )
        )

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# ---------------------------------
# TEST HISTORY
# ---------------------------------
@student_bp.route("/test_history")
@role_required("Student")
def test_history():

    student_id = session.get("user_id")

    conn = None
    cursor = None

    try:

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                ta.attempt_id,
                ta.test_id,

                t.test_name,
                t.total_marks,

                sub.subject_name AS subject_name,

                st.standard_name AS standard_name,

                ta.score,
                ta.started_at,
                ta.submitted_at,
                ta.status

            FROM test_attempt ta

            JOIN test t
                ON t.test_id = ta.test_id

            JOIN subject sub
                ON sub.subject_id = t.subject_id

            LEFT JOIN standard st
                ON st.standard_id = sub.standard_id

            WHERE ta.student_id = %s
              AND ta.status = 'Submitted'

            ORDER BY ta.submitted_at DESC
        """, (
            student_id,
        ))

        results = cursor.fetchall()

        # ---------------------------------
        # CALCULATE PERCENTAGE
        # ---------------------------------
        for result in results:

            total_marks = result["total_marks"] or 0
            score = result["score"] or 0

            if float(total_marks) > 0:

                result["percentage"] = round(
                    (
                        float(score)
                        /
                        float(total_marks)
                    ) * 100,
                    2
                )

            else:

                result["percentage"] = 0

        return render_template(
            "student/test_history.html",
            results=results
        )

    except Exception as e:

        print("\n========== TEST HISTORY ERROR ==========")
        print(e)
        print("========================================\n")

        flash(
            "Unable to load test history.",
            "error"
        )

        return redirect(
            url_for("student.student_home")
        )

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

# ---------------------------------
# TEST RESULT
# ---------------------------------
@student_bp.route("/test_result/<int:attempt_id>")
@role_required("Student")
def test_result(attempt_id):

    student_id = session.get("user_id")

    conn = None
    cursor = None

    try:

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # ---------------------------------
        # GET SUBMITTED ATTEMPT
        # ---------------------------------
        cursor.execute("""
            SELECT
                ta.attempt_id,
                ta.test_id,
                ta.score,
                ta.status,
                ta.started_at,
                ta.submitted_at,

                t.test_name,
                t.total_marks,

                sub.subject_name AS subject_name,
                sub.assessment_type AS assessment_type,

                st.standard_name AS standard_name

            FROM test_attempt ta

            JOIN test t
                ON t.test_id = ta.test_id

            JOIN subject sub
                ON sub.subject_id = t.subject_id

            LEFT JOIN standard st
                ON st.standard_id = sub.standard_id

            WHERE ta.attempt_id = %s
              AND ta.student_id = %s
              AND ta.status = 'Submitted'
        """, (
            attempt_id,
            student_id
        ))

        result = cursor.fetchone()

        if not result:

            flash(
                "Result not found.",
                "error"
            )

            return redirect(
                url_for("student.test_history")
            )

        # ---------------------------------
        # CALCULATE PERCENTAGE
        # ---------------------------------
        total_marks = result["total_marks"] or 0
        score = result["score"] or 0

        if float(total_marks) > 0:

            percentage = round(
                (
                    float(score)
                    /
                    float(total_marks)
                ) * 100,
                2
            )

        else:

            percentage = 0

        # ---------------------------------
        # GET ANSWER REVIEW
        #
        # Traditional:
        #     question -> chapter
        #
        # OBE:
        #     question -> course outcome
        #
        # Also retrieve all option text so
        # the result can display:
        #
        # B. Noun
        # A. Pronoun
        # ---------------------------------
        cursor.execute("""
            SELECT
                sa.answer_id,

                q.question_id,
                q.question_text,

                q.option_a,
                q.option_b,
                q.option_c,
                q.option_d,

                q.correct_answer AS correct_option,

                q.chapter_id,
                c.chapter_name,

                q.co_id,

                co.co_code AS co_name,
                co.co_description,

                sa.selected_answer,
                sa.is_correct,
                sa.marks_obtained

            FROM student_answer sa

            JOIN question q
                ON q.question_id = sa.question_id

            LEFT JOIN chapter c
                ON c.chapter_id = q.chapter_id

            LEFT JOIN course_outcome co
                ON co.co_id = q.co_id

            WHERE sa.attempt_id = %s

            ORDER BY sa.answer_id ASC
        """, (
            attempt_id,
        ))

        answers = cursor.fetchall()

        # ---------------------------------
        # CONVERT OPTION LETTERS
        # TO ACTUAL ANSWER TEXT
        # ---------------------------------
        option_map = {
            "A": "option_a",
            "B": "option_b",
            "C": "option_c",
            "D": "option_d"
        }

        for answer in answers:

            # -----------------------------
            # STUDENT'S SELECTED ANSWER
            # -----------------------------
            selected = answer["selected_answer"]

            if selected:

                selected = str(selected).strip().upper()

                answer["selected_option"] = selected

                selected_column = option_map.get(selected)

                if selected_column:

                    answer["selected_answer_text"] = (
                        answer[selected_column]
                    )

                else:

                    answer["selected_answer_text"] = selected

            else:

                answer["selected_option"] = None

                answer["selected_answer_text"] = None

            # -----------------------------
            # CORRECT ANSWER
            # -----------------------------
            correct = answer["correct_option"]

            if correct:

                correct = str(correct).strip().upper()

                answer["correct_option"] = correct

                correct_column = option_map.get(correct)

                if correct_column:

                    answer["correct_answer_text"] = (
                        answer[correct_column]
                    )

                else:

                    answer["correct_answer_text"] = correct

            else:

                answer["correct_answer_text"] = "-"

        # ---------------------------------
        # FIND WEAK AREAS
        #
        # Traditional -> Chapters
        # OBE         -> Course Outcomes
        # ---------------------------------
        weak_topic_data = {}

        if result["assessment_type"] == "OBE":

            for answer in answers:

                if (
                    answer["selected_answer"]
                    and not answer["is_correct"]
                    and answer["co_name"]
                ):

                    co_name = answer["co_name"]

                    if co_name not in weak_topic_data:

                        weak_topic_data[co_name] = {
                            "co_name": co_name,
                            "incorrect_count": 0
                        }

                    weak_topic_data[
                        co_name
                    ]["incorrect_count"] += 1

        else:

            for answer in answers:

                if (
                    answer["selected_answer"]
                    and not answer["is_correct"]
                    and answer["chapter_name"]
                ):

                    chapter_name = answer["chapter_name"]

                    if chapter_name not in weak_topic_data:

                        weak_topic_data[chapter_name] = {
                            "chapter_name": chapter_name,
                            "incorrect_count": 0
                        }

                    weak_topic_data[
                        chapter_name
                    ]["incorrect_count"] += 1

        # ---------------------------------
        # CONVERT TO LIST
        # ---------------------------------
        weak_topics = list(
            weak_topic_data.values()
        )

        # ---------------------------------
        # MOST AFFECTED AREAS FIRST
        # ---------------------------------
        weak_topics.sort(
            key=lambda x: x["incorrect_count"],
            reverse=True
        )

        # ---------------------------------
        # CALCULATE OBE CO PERFORMANCE
        # ---------------------------------
        co_performance = {}

        if result["assessment_type"] == "OBE":

            for answer in answers:

                if not answer["co_id"]:
                    continue

                co_id = answer["co_id"]

                if co_id not in co_performance:

                    co_performance[co_id] = {
                        "co_id": co_id,
                        "co_name": answer["co_name"],
                        "co_description": answer["co_description"],
                        "total_questions": 0,
                        "correct_questions": 0,
                        "incorrect_questions": 0
                    }

                co_performance[co_id][
                    "total_questions"
                ] += 1

                if answer["selected_answer"]:

                    if answer["is_correct"]:

                        co_performance[co_id][
                            "correct_questions"
                        ] += 1

                    else:

                        co_performance[co_id][
                            "incorrect_questions"
                        ] += 1

            # ---------------------------------
            # CALCULATE CO ATTAINMENT
            # ---------------------------------
            for co in co_performance.values():

                total_questions = co["total_questions"]

                if total_questions > 0:

                    co["attainment_percentage"] = round(
                        (
                            co["correct_questions"]
                            /
                            total_questions
                        ) * 100,
                        2
                    )

                else:

                    co["attainment_percentage"] = 0

        co_performance = list(
            co_performance.values()
        )

        # ---------------------------------
        # RENDER RESULT
        # ---------------------------------
        return render_template(
            "student/test_result.html",

            result=result,

            percentage=percentage,

            answers=answers,

            weak_topics=weak_topics,

            co_performance=co_performance
        )

    except Exception as e:

        print("\n========== TEST RESULT ERROR ==========")
        print(e)
        print("=======================================\n")

        flash(
            "Unable to load test result.",
            "error"
        )

        return redirect(
            url_for("student.test_history")
        )

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

# ---------------------------------
# LEARNING PROGRESS
# ---------------------------------
@student_bp.route("/my_progress")
@role_required("Student")
def my_progress():

    student_id = session.get("user_id")

    conn = None
    cursor = None

    try:

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # ---------------------------------
        # OVERALL STATISTICS
        # ---------------------------------
        cursor.execute("""
            SELECT

                COUNT(*) AS completed_tests,

                COALESCE(
                    ROUND(
                        AVG(
                            CASE
                                WHEN t.total_marks > 0
                                THEN
                                    (ta.score / t.total_marks) * 100
                            END
                        ),
                        2
                    ),
                    0
                ) AS average_percentage,

                COALESCE(
                    ROUND(
                        MAX(
                            CASE
                                WHEN t.total_marks > 0
                                THEN
                                    (ta.score / t.total_marks) * 100
                            END
                        ),
                        2
                    ),
                    0
                ) AS highest_percentage

            FROM test_attempt ta

            JOIN test t
                ON t.test_id = ta.test_id

            WHERE ta.student_id = %s
              AND ta.status = 'Submitted'
        """, (
            student_id,
        ))

        stats = cursor.fetchone()

        # ---------------------------------
        # SUBJECT-WISE PERFORMANCE
        # ---------------------------------
        cursor.execute("""
            SELECT

                sub.subject_name,

                COUNT(ta.attempt_id) AS tests_completed,

                ROUND(
                    AVG(
                        CASE
                            WHEN t.total_marks > 0
                            THEN
                                (ta.score / t.total_marks) * 100
                        END
                    ),
                    2
                ) AS average_percentage

            FROM test_attempt ta

            JOIN test t
                ON t.test_id = ta.test_id

            JOIN subject sub
                ON sub.subject_id = t.subject_id

            WHERE ta.student_id = %s
              AND ta.status = 'Submitted'

            GROUP BY
                sub.subject_id,
                sub.subject_name

            ORDER BY
                average_percentage DESC
        """, (
            student_id,
        ))

        subject_performance = cursor.fetchall()

        # ---------------------------------
        # ADD PERFORMANCE LABEL
        # ---------------------------------
        for subject in subject_performance:

            percentage = float(
                subject["average_percentage"] or 0
            )

            if percentage >= 75:
                subject["performance"] = "Strong"
            elif percentage >= 60:
                subject["performance"] = "Good"
            elif percentage >= 50:
                subject["performance"] = "Average"
            else:
                subject["performance"] = "Needs Improvement"
        
        # ---------------------------------
        # RECENT RESULTS
        # ---------------------------------
        cursor.execute("""
            SELECT

                t.test_name,

                sub.subject_name,

                ta.score,

                t.total_marks,

                ROUND(
                    CASE
                        WHEN t.total_marks > 0
                        THEN
                            (ta.score / t.total_marks) * 100
                        ELSE 0
                    END,
                    2
                ) AS percentage,

                ta.submitted_at

            FROM test_attempt ta

            JOIN test t
                ON t.test_id = ta.test_id

            JOIN subject sub
                ON sub.subject_id = t.subject_id

            WHERE ta.student_id = %s
              AND ta.status = 'Submitted'

            ORDER BY ta.submitted_at DESC

            LIMIT 5
        """, (
            student_id,
        ))

        recent_results = cursor.fetchall()

        # ---------------------------------
        # STRONGEST SUBJECT
        # ---------------------------------
        strongest_subject = None

        if subject_performance:

            strongest_subject = subject_performance[0]

        # ---------------------------------
        # NEEDS IMPROVEMENT SUBJECT
        # ---------------------------------
        weakest_subject = None

        if subject_performance:

            weakest_subject = subject_performance[-1]

        return render_template(
            "student/my_progress.html",

            stats=stats,

            subject_performance=subject_performance,

            recent_results=recent_results,

            strongest_subject=strongest_subject,

            weakest_subject=weakest_subject
        )

    except Exception as e:

        print("\n========== LEARNING PROGRESS ERROR ==========")
        print(e)
        print("=============================================\n")

        flash(
            "Unable to load learning progress.",
            "error"
        )

        return redirect(
            url_for("student.student_home")
        )

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# ---------------------------------
# PERSONALIZED REVISION PLANNER
# ---------------------------------
@student_bp.route("/revision_planner")
@role_required("Student")
def revision_planner():

    student_id = session.get("user_id")

    conn = None
    cursor = None

    try:

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # ---------------------------------
        # FIND WEAK CHAPTERS
        # ---------------------------------
        cursor.execute("""
            SELECT
                c.chapter_id,
                c.chapter_name,
                sub.subject_name,

                COUNT(sa.answer_id) AS incorrect_count

            FROM student_answer sa

            JOIN test_attempt ta
                ON ta.attempt_id = sa.attempt_id

            JOIN question q
                ON q.question_id = sa.question_id

            JOIN chapter c
                ON c.chapter_id = q.chapter_id

            JOIN test t
                ON t.test_id = ta.test_id

            JOIN subject sub
                ON sub.subject_id = t.subject_id

            WHERE ta.student_id = %s
              AND ta.status = 'Submitted'
              AND sa.is_correct = 0
              AND q.chapter_id IS NOT NULL

            GROUP BY
                c.chapter_id,
                c.chapter_name,
                sub.subject_id,
                sub.subject_name

            ORDER BY
                incorrect_count DESC

            LIMIT 10
        """, (
            student_id,
        ))

        revision_topics = cursor.fetchall()

        # ---------------------------------
        # ADD REVISION PRIORITY
        # ---------------------------------
        for topic in revision_topics:

            count = topic["incorrect_count"]

            if count >= 5:

                topic["priority"] = "High"

            elif count >= 3:

                topic["priority"] = "Medium"

            else:

                topic["priority"] = "Light"

        return render_template(
            "student/revision_planner.html",
            revision_topics=revision_topics
        )

    except Exception as e:

        print("\n========== REVISION PLANNER ERROR ==========")
        print(e)
        print("============================================\n")

        flash(
            "Unable to load revision planner.",
            "error"
        )

        return redirect(
            url_for("student.student_home")
        )

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()     

# ---------------------------------
# LEARNING JOURNEY
# ---------------------------------
@student_bp.route("/learning_journey")
@role_required("Student")
def learning_journey():

    student_id = session.get("user_id")

    conn = None
    cursor = None

    try:

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # ---------------------------------
        # GET COMPLETED ASSESSMENTS
        # ---------------------------------
        cursor.execute("""
            SELECT

                ta.attempt_id,

                t.test_name,
                t.total_marks,

                sub.subject_name,

                ta.score,
                ta.submitted_at

            FROM test_attempt ta

            JOIN test t
                ON t.test_id = ta.test_id

            JOIN subject sub
                ON sub.subject_id = t.subject_id

            WHERE ta.student_id = %s
              AND ta.status = 'Submitted'

            ORDER BY ta.submitted_at ASC
        """, (
            student_id,
        ))

        assessments = cursor.fetchall()

        # ---------------------------------
        # EMPTY JOURNEY
        # ---------------------------------
        if not assessments:

            return render_template(
                "student/learning_journey.html",
                journey=None
            )

        # ---------------------------------
        # CALCULATE PERCENTAGES
        # ---------------------------------
        for assessment in assessments:

            total_marks = assessment["total_marks"] or 0
            score = assessment["score"] or 0

            if float(total_marks) > 0:

                assessment["percentage"] = round(
                    (
                        float(score)
                        /
                        float(total_marks)
                    ) * 100,
                    2
                )

            else:

                assessment["percentage"] = 0

        # ---------------------------------
        # BASIC JOURNEY STATISTICS
        # ---------------------------------
        total_tests = len(assessments)

        subjects = set()

        for assessment in assessments:

            if assessment["subject_name"]:

                subjects.add(
                    assessment["subject_name"]
                )

        subject_count = len(subjects)

        # ---------------------------------
        # HIGHEST SCORE
        # ---------------------------------
        highest_assessment = max(
            assessments,
            key=lambda x: x["percentage"]
        )

        # ---------------------------------
        # FIRST ASSESSMENT
        # ---------------------------------
        first_assessment = assessments[0]

        # ---------------------------------
        # RECENT PROGRESS
        #
        # Compare earlier assessments with
        # the student's more recent results.
        # ---------------------------------
        recent_count = min(3, total_tests)

        recent_assessments = assessments[
            -recent_count:
        ]

        earlier_assessments = assessments[
            :-recent_count
        ]

        recent_average = round(
            sum(
                item["percentage"]
                for item in recent_assessments
            )
            /
            len(recent_assessments),
            2
        )

        earlier_average = None

        if earlier_assessments:

            earlier_average = round(
                sum(
                    item["percentage"]
                    for item in earlier_assessments
                )
                /
                len(earlier_assessments),
                2
            )

        # ---------------------------------
        # SUBJECT PERFORMANCE
        # ---------------------------------
        subject_data = {}

        for assessment in assessments:

            subject = assessment["subject_name"]

            if subject not in subject_data:

                subject_data[subject] = []

            subject_data[subject].append(
                assessment["percentage"]
            )

        subject_averages = {}

        for subject, scores in subject_data.items():

            subject_averages[subject] = round(
                sum(scores) / len(scores),
                2
            )

        strongest_subject = max(
            subject_averages,
            key=subject_averages.get
        )

        weakest_subject = min(
            subject_averages,
            key=subject_averages.get
        )

        # ---------------------------------
        # BUILD MILESTONES
        # ---------------------------------
        milestones = []

        # First assessment
        milestones.append({
            "icon": "🚀",
            "title": "Your assessment journey began",
            "description": (
                f"You completed your first assessment "
                f"— {first_assessment['test_name']} "
                f"({first_assessment['subject_name']})."
            ),
            "date": first_assessment["submitted_at"]
        })

        # Consistency milestone
        if total_tests >= 5:

            milestones.append({
                "icon": "📚",
                "title": "Building consistency",
                "description": (
                    f"You have now completed "
                    f"{total_tests} assessments "
                    f"across {subject_count} "
                    f"{'subject' if subject_count == 1 else 'subjects'}."
                ),
                "date": assessments[4]["submitted_at"]
            })

        elif total_tests >= 3:

            milestones.append({
                "icon": "📚",
                "title": "Building consistency",
                "description": (
                    f"You have completed "
                    f"{total_tests} assessments so far."
                ),
                "date": assessments[2]["submitted_at"]
            })

        # Highest score
        milestones.append({
            "icon": "🏆",
            "title": "Your highest score so far",
            "description": (
                f"{highest_assessment['percentage']}% "
                f"in {highest_assessment['test_name']} "
                f"({highest_assessment['subject_name']})."
            ),
            "date": highest_assessment["submitted_at"]
        })

        # Recent performance
        if earlier_average is not None:

            difference = round(
                recent_average - earlier_average,
                2
            )

            if difference > 0:

                progress_text = (
                    f"Your average across your latest "
                    f"{recent_count} assessments is "
                    f"{recent_average}%, compared with "
                    f"{earlier_average}% across your earlier "
                    f"assessments."
                )

                progress_icon = "📈"

            elif difference < 0:

                progress_text = (
                    f"Your average across your latest "
                    f"{recent_count} assessments is "
                    f"{recent_average}%. Your earlier "
                    f"average was {earlier_average}%."
                )

                progress_icon = "🔎"

            else:

                progress_text = (
                    f"Your latest {recent_count} assessments "
                    f"average {recent_average}%, the same as "
                    f"your earlier average."
                )

                progress_icon = "📊"

            milestones.append({
                "icon": progress_icon,
                "title": "A look at your recent progress",
                "description": progress_text,
                "date": recent_assessments[0]["submitted_at"]
            })

        else:

            milestones.append({
                "icon": "📊",
                "title": "Your current snapshot",
                "description": (
                    f"Your completed assessments currently "
                    f"average {recent_average}%."
                ),
                "date": recent_assessments[0]["submitted_at"]
            })

        # Current focus
        if strongest_subject == weakest_subject:

            focus_text = (
                f"You currently have assessments in "
                f"{strongest_subject}. Keep building "
                f"your understanding through practice."
            )

        else:

            focus_text = (
                f"{weakest_subject} currently has your "
                f"lowest subject average at "
                f"{subject_averages[weakest_subject]}%. "
                f"This is an area worth giving some "
                f"extra attention to."
            )

        milestones.append({
            "icon": "🌱",
            "title": "Your current focus",
            "description": focus_text,
            "date": assessments[-1]["submitted_at"]
        })

        # ---------------------------------
        # GROUP MILESTONES BY DATE
        # ---------------------------------
        grouped_milestones = {}

        for milestone in milestones:

            milestone_date = milestone["date"].date()

            if milestone_date not in grouped_milestones:

                grouped_milestones[milestone_date] = []

            grouped_milestones[milestone_date].append(
                milestone
            )


        # ---------------------------------
        # CONVERT TO TEMPLATE-FRIENDLY LIST
        # ---------------------------------
        milestone_groups = []

        for milestone_date, items in sorted(
            grouped_milestones.items(),
            reverse=True
        ):

            milestone_groups.append({
                "date": items[0]["date"],
                "milestones": list(reversed(items))
            })


        # ---------------------------------
        # RENDER
        # ---------------------------------

        return render_template(
            "student/learning_journey.html",
            milestones=milestone_groups,
            total_tests=total_tests,
            subject_count=subject_count,
            recent_average=recent_average,
            strongest_subject=strongest_subject,
            strongest_percentage=subject_averages[strongest_subject],
            weakest_subject=weakest_subject,
            weakest_percentage=subject_averages[weakest_subject]
        )

    except Exception as e:

        print("\n========== LEARNING JOURNEY ERROR ==========")
        print(e)
        print("=============================================\n")

        flash(
            "Unable to load learning journey.",
            "error"
        )

        return redirect(
            url_for("student.student_home")
        )

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()