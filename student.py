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

    return render_template(
        "student/student_home.html"
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

                NULL AS standard_name,

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

            WHERE t.status = 'Published'

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
        # ---------------------------------
        cursor.execute("""
            SELECT
                t.test_id,
                t.test_name,
                t.description,
                t.total_marks,
                t.duration_minutes,

                sub.subject_name AS subject_name,

                NULL AS standard_name

            FROM test t

            JOIN subject sub
                ON sub.subject_id = t.subject_id

            WHERE t.test_id = %s
              AND t.status = 'Published'
        """, (
            test_id,
        ))

        test = cursor.fetchone()

        if not test:

            flash(
                "Test not found or is no longer available.",
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

                NULL AS standard_name,

                ta.score,
                ta.started_at,
                ta.submitted_at,
                ta.status

            FROM test_attempt ta

            JOIN test t
                ON t.test_id = ta.test_id

            JOIN subject sub
                ON sub.subject_id = t.subject_id

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

                NULL AS standard_name

            FROM test_attempt ta

            JOIN test t
                ON t.test_id = ta.test_id

            JOIN subject sub
                ON sub.subject_id = t.subject_id

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
        # ---------------------------------
        cursor.execute("""
            SELECT
                q.question_text,
                q.option_a,
                q.option_b,
                q.option_c,
                q.option_d,

                q.correct_answer AS correct_option,

                q.chapter_id,
                c.chapter_name,

                sa.selected_answer,
                sa.is_correct,
                sa.marks_obtained

            FROM student_answer sa

            JOIN question q
                ON q.question_id = sa.question_id

            LEFT JOIN chapter c
                ON c.chapter_id = q.chapter_id

            WHERE sa.attempt_id = %s

            ORDER BY sa.answer_id ASC
        """, (
            attempt_id,
        ))

        answers = cursor.fetchall()

        # ---------------------------------
        # FIND WEAK TOPICS
        #
        # Only answered questions that were
        # marked incorrect are counted.
        # ---------------------------------
        weak_topic_data = {}

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
        # SHOW MOST AFFECTED CHAPTERS FIRST
        # ---------------------------------
        weak_topics.sort(
            key=lambda x: x["incorrect_count"],
            reverse=True
        )

        return render_template(
            "student/test_result.html",
            result=result,
            percentage=percentage,
            answers=answers,
            weak_topics=weak_topics
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
# MY PROGRESS
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
        # TEST STATISTICS
        # ---------------------------------
        cursor.execute("""
            SELECT
                COUNT(*) AS total_tests,

                SUM(
                    CASE
                        WHEN status = 'Submitted'
                        THEN 1
                        ELSE 0
                    END
                ) AS completed_tests

            FROM test_attempt

            WHERE student_id = %s
        """, (
            student_id,
        ))

        stats = cursor.fetchone()

        # ---------------------------------
        # RECENT RESULTS
        # ---------------------------------
        cursor.execute("""
            SELECT
                t.test_name,
                ta.score,
                t.total_marks,
                ta.submitted_at

            FROM test_attempt ta

            JOIN test t
                ON t.test_id = ta.test_id

            WHERE ta.student_id = %s
              AND ta.status = 'Submitted'

            ORDER BY ta.submitted_at DESC

            LIMIT 5
        """, (
            student_id,
        ))

        recent_results = cursor.fetchall()

        return render_template(
            "student/my_progress.html",
            stats=stats,
            recent_results=recent_results
        )

    except Exception as e:

        print("\n========== MY PROGRESS ERROR ==========")
        print(e)
        print("=======================================\n")

        flash(
            "Unable to load progress.",
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
# STUDENT PROFILE
# ---------------------------------
@student_bp.route("/profile")
@role_required("Student")
def student_profile():

    student_id = session.get("user_id")

    conn = None
    cursor = None

    try:

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM user
            WHERE user_id = %s
        """, (
            student_id,
        ))

        student = cursor.fetchone()

        return render_template(
            "student/student_profile.html",
            student=student
        )

    except Exception as e:

        print("\n========== STUDENT PROFILE ERROR ==========")
        print(e)
        print("===========================================\n")

        flash(
            "Unable to load profile.",
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