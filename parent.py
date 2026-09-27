from flask import Blueprint, render_template, session, redirect, url_for, flash
from db import get_db_connection
from session_utils import role_required


parent_bp = Blueprint(
    "parent",
    __name__,
    url_prefix="/parent"
)
# ============================================================
# PARENT HOME
# ============================================================

@parent_bp.route("/")
@role_required("Parent")
def parent_home():

    parent_id = session.get("user_id")

    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Get parent's own details
        cursor.execute("""
            SELECT
                parent_id,
                parent_name
            FROM parent
            WHERE parent_id = %s
        """, (parent_id,))

        parent = cursor.fetchone()

        # Get parent's child
        cursor.execute("""
            SELECT
                student_id,
                student_name,
                email,
                standard_id,
                institution_id
            FROM student
            WHERE parent_id = %s
              AND status = 'Active'
            ORDER BY student_name
            LIMIT 1
        """, (parent_id,))

        child = cursor.fetchone()

        if not child:
            return render_template(
                "parent/parent_home.html",
                parent=parent,
                child=None
            )

        # Count submitted tests
        cursor.execute("""
            SELECT COUNT(*) AS test_count
            FROM test_attempt
            WHERE student_id = %s
              AND status = 'Submitted'
        """, (child["student_id"],))

        test_count = cursor.fetchone()["test_count"] or 0

        # Average score
        cursor.execute("""
            SELECT
                AVG(
                    CASE
                        WHEN t.total_marks > 0
                        THEN (ta.score / t.total_marks) * 100
                        ELSE 0
                    END
                ) AS average_percentage
            FROM test_attempt ta
            JOIN test t
                ON t.test_id = ta.test_id
            WHERE ta.student_id = %s
              AND ta.status = 'Submitted'
        """, (child["student_id"],))

        average_result = cursor.fetchone()

        average_percentage = round(
            float(average_result["average_percentage"] or 0),
            2
        )

        return render_template(
            "parent/parent_home.html",
            parent=parent,
            child=child,
            test_count=test_count,
            average_percentage=average_percentage
        )

    except Exception as e:

        print("\n========== PARENT HOME ERROR ==========")
        print(e)
        print("=======================================\n")

        flash("Unable to load parent dashboard.", "error")

        return redirect(url_for("auth.login_page"))

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

# ============================================================
# CHILD TEST RESULTS - LIST
# ============================================================

@parent_bp.route("/child_test_results")
@role_required("Parent")
def child_test_results():

    parent_id = session.get("user_id")

    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Get parent's child
        cursor.execute("""
            SELECT
                student_id,
                student_name,
                email,
                standard_id,
                institution_id
            FROM student
            WHERE parent_id = %s
              AND status = 'Active'
            ORDER BY student_name
            LIMIT 1
        """, (parent_id,))

        child = cursor.fetchone()

        if not child:

            return render_template(
                "parent/child_test_results.html",
                results=[],
                child=None,
                detailed_result=None,
                answers=[],
                weak_topics=[],
                co_performance=[],
                percentage=None
            )

        # Get submitted test attempts of the child
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

                sub.subject_name,
                sub.assessment_type,

                st.standard_name

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
        """, (child["student_id"],))

        results = cursor.fetchall()

        # Calculate percentage for every result
        for result in results:

            total_marks = result["total_marks"] or 0
            score = result["score"] or 0

            if float(total_marks) > 0:

                result["percentage"] = round(
                    (float(score) / float(total_marks)) * 100,
                    2
                )

            else:

                result["percentage"] = 0

        return render_template(
            "parent/child_test_results.html",
            results=results,
            child=child,
            detailed_result=None,
            answers=[],
            weak_topics=[],
            co_performance=[],
            percentage=None
        )

    except Exception as e:

        print("\n========== PARENT TEST RESULTS ERROR ==========")
        print(e)
        print("===============================================\n")

        flash("Unable to load test results.", "error")

        return redirect(url_for("parent.parent_home"))

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# ============================================================
# CHILD TEST RESULT - DETAILED
# ============================================================

@parent_bp.route("/child_test_result/<int:attempt_id>")
@role_required("Parent")
def child_test_result(attempt_id):

    parent_id = session.get("user_id")

    conn = None
    cursor = None

    try:

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # ----------------------------------------------------
        # Get test result
        # ----------------------------------------------------

        cursor.execute("""
            SELECT
                ta.attempt_id,
                ta.test_id,
                ta.student_id,
                ta.score,
                ta.status,
                ta.started_at,
                ta.submitted_at,

                s.student_name,
                s.email,

                t.test_name,
                t.total_marks,

                sub.subject_name,
                sub.assessment_type,

                st.standard_name

            FROM test_attempt ta

            JOIN student s
                ON s.student_id = ta.student_id

            JOIN test t
                ON t.test_id = ta.test_id

            JOIN subject sub
                ON sub.subject_id = t.subject_id

            LEFT JOIN standard st
                ON st.standard_id = sub.standard_id

            WHERE ta.attempt_id = %s
              AND ta.status = 'Submitted'
              AND s.parent_id = %s
              AND s.status = 'Active'
        """, (
            attempt_id,
            parent_id
        ))

        detailed_result = cursor.fetchone()

        if not detailed_result:

            flash("Test result not found.", "error")

            return redirect(
                url_for("parent.child_test_results")
            )

        # ----------------------------------------------------
        # Calculate percentage
        # ----------------------------------------------------

        total_marks = detailed_result["total_marks"] or 0
        score = detailed_result["score"] or 0

        if float(total_marks) > 0:

            percentage = round(
                (float(score) / float(total_marks)) * 100,
                2
            )

        else:

            percentage = 0

        detailed_result["percentage"] = percentage

        # ----------------------------------------------------
        # Get child information
        # ----------------------------------------------------

        cursor.execute("""
            SELECT
                student_id,
                student_name,
                email,
                phone,
                standard_id,
                institution_id
            FROM student
            WHERE student_id = %s
              AND parent_id = %s
              AND status = 'Active'
        """, (
            detailed_result["student_id"],
            parent_id
        ))

        child = cursor.fetchone()

        # ----------------------------------------------------
        # Get answers
        # ----------------------------------------------------

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
        """, (attempt_id,))

        answers = cursor.fetchall()

        # ----------------------------------------------------
        # Convert option letters into option text
        # ----------------------------------------------------

        option_map = {
            "A": "option_a",
            "B": "option_b",
            "C": "option_c",
            "D": "option_d"
        }

        for answer in answers:

            selected = answer["selected_answer"]

            if selected:

                selected = str(selected).strip().upper()

                answer["selected_option"] = selected

                selected_column = option_map.get(selected)

                if selected_column:

                    answer["selected_answer_text"] = answer[
                        selected_column
                    ]

                else:

                    answer["selected_answer_text"] = selected

            else:

                answer["selected_option"] = None
                answer["selected_answer_text"] = None

            correct = answer["correct_option"]

            if correct:

                correct = str(correct).strip().upper()

                answer["correct_option"] = correct

                correct_column = option_map.get(correct)

                if correct_column:

                    answer["correct_answer_text"] = answer[
                        correct_column
                    ]

                else:

                    answer["correct_answer_text"] = correct

            else:

                answer["correct_answer_text"] = "-"

        # ----------------------------------------------------
        # Areas to Improve
        #
        # OBE       -> Course Outcomes
        # Traditional -> Chapters
        # ----------------------------------------------------

        weak_topic_data = {}

        if detailed_result["assessment_type"] == "OBE":

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

                    weak_topic_data[co_name][
                        "incorrect_count"
                    ] += 1

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

                    weak_topic_data[chapter_name][
                        "incorrect_count"
                    ] += 1

        weak_topics = list(
            weak_topic_data.values()
        )

        weak_topics.sort(
            key=lambda x: x["incorrect_count"],
            reverse=True
        )

        # ----------------------------------------------------
        # OBE Course Outcome Performance
        # ----------------------------------------------------

        co_performance = {}

        if detailed_result["assessment_type"] == "OBE":

            for answer in answers:

                if not answer["co_id"]:
                    continue

                co_id = answer["co_id"]

                if co_id not in co_performance:

                    co_performance[co_id] = {
                        "co_id": co_id,
                        "co_name": answer["co_name"],
                        "co_description": answer[
                            "co_description"
                        ],
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

        # ----------------------------------------------------
        # Calculate CO attainment percentage
        # ----------------------------------------------------

        for co in co_performance.values():

            total_questions = co["total_questions"]

            if total_questions > 0:

                co["attainment_percentage"] = round(
                    (
                        co["correct_questions"]
                        / total_questions
                    ) * 100,
                    2
                )

            else:

                co["attainment_percentage"] = 0

        co_performance = list(
            co_performance.values()
        )

        # ----------------------------------------------------
        # Render same detailed result structure as Student
        # ----------------------------------------------------

        return render_template(
            "parent/child_test_results.html",

            results=[],

            child=child,

            detailed_result=detailed_result,

            answers=answers,

            weak_topics=weak_topics,

            co_performance=co_performance,

            percentage=percentage
        )

    except Exception as e:

        print("\n========== PARENT TEST RESULT ERROR ==========")
        print(e)
        print("==============================================\n")

        flash("Unable to load test result.", "error")

        return redirect(
            url_for("parent.child_test_results")
        )

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

# ---------------------------------
# CHILD PROGRESS SUMMARY
# ---------------------------------
@parent_bp.route("/progress_summary")
@role_required("Parent")
def progress_summary():

    parent_id = session.get("user_id")

    conn = None
    cursor = None

    try:

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # ---------------------------------
        # GET CHILD
        # ---------------------------------
        cursor.execute("""
            SELECT
                student_id,
                student_name
            FROM student
            WHERE parent_id = %s
              AND status = 'Active'
            LIMIT 1
        """, (parent_id,))

        child = cursor.fetchone()

        if not child:
            flash("No active student is linked to your account.", "error")
            return redirect(url_for("parent.parent_home"))

        student_id = child["student_id"]

        # ---------------------------------
        # OVERALL PERFORMANCE
        # ---------------------------------
        cursor.execute("""
            SELECT
                COUNT(*) AS completed_tests,
                COALESCE(
                    ROUND(
                        AVG(
                            CASE
                                WHEN t.total_marks > 0
                                THEN (ta.score / t.total_marks) * 100
                                ELSE 0
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
                                THEN (ta.score / t.total_marks) * 100
                                ELSE 0
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
        """, (student_id,))

        stats = cursor.fetchone()

        # ---------------------------------
        # SUBJECT-WISE PERFORMANCE
        # ---------------------------------
        cursor.execute("""
            SELECT
                sub.subject_name,

                COUNT(*) AS tests_completed,

                ROUND(
                    AVG(
                        CASE
                            WHEN t.total_marks > 0
                            THEN (ta.score / t.total_marks) * 100
                            ELSE 0
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

            ORDER BY average_percentage DESC
        """, (student_id,))

        subject_performance = cursor.fetchall()

        # ---------------------------------
        # PERFORMANCE LABEL
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
                subject["performance"] = "Keep Practising"

        # ---------------------------------
        # STRONGEST / AREA FOR IMPROVEMENT
        # ---------------------------------
        strongest_subject = None
        weakest_subject = None

        if subject_performance:

            strongest_subject = subject_performance[0]

            weakest_subject = min(
                subject_performance,
                key=lambda x: float(
                    x["average_percentage"] or 0
                )
            )

        # ---------------------------------
        # RECENT RESULTS
        # ---------------------------------
        cursor.execute("""
            SELECT
                t.test_name,
                sub.subject_name,
                ta.score,
                t.total_marks,
                ta.submitted_at,

                ROUND(
                    CASE
                        WHEN t.total_marks > 0
                        THEN (ta.score / t.total_marks) * 100
                        ELSE 0
                    END,
                    2
                ) AS percentage

            FROM test_attempt ta

            JOIN test t
                ON t.test_id = ta.test_id

            JOIN subject sub
                ON sub.subject_id = t.subject_id

            WHERE ta.student_id = %s
              AND ta.status = 'Submitted'

            ORDER BY ta.submitted_at DESC

            LIMIT 5
        """, (student_id,))

        recent_results = cursor.fetchall()

        return render_template(
            "parent/progress_summary.html",
            child=child,
            stats=stats,
            subject_performance=subject_performance,
            strongest_subject=strongest_subject,
            weakest_subject=weakest_subject,
            recent_results=recent_results
        )

    except Exception as e:

        print("\n========== PROGRESS SUMMARY ERROR ==========")
        print(e)
        print("============================================\n")

        flash("Unable to load progress summary.", "error")

        return redirect(url_for("parent.parent_home"))

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()