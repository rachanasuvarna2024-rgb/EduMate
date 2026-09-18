from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    flash
)

from db import get_db_connection
from session_utils import role_required


# ---------------------------------
# PARENT BLUEPRINT
# ---------------------------------
parent_bp = Blueprint(
    "parent",
    __name__,
    url_prefix="/parent"
)


# ---------------------------------
# PARENT HOME
# ---------------------------------
@parent_bp.route("/")
@role_required("Parent")
def parent_home():

    parent_id = session.get("user_id")

    if not parent_id:

        flash(
            "Parent session information not found.",
            "error"
        )

        return redirect(
            url_for("auth.login_page")
        )

    conn = None
    cursor = None

    try:

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # ---------------------------------
        # GET PARENT INFORMATION
        # ---------------------------------
        cursor.execute("""
            SELECT
                parent_id,
                parent_name,
                email,
                phone
            FROM parent
            WHERE parent_id = %s
        """, (
            parent_id,
        ))

        parent = cursor.fetchone()

        if not parent:

            flash(
                "Parent information not found.",
                "error"
            )

            return redirect(
                url_for("auth.login_page")
            )


        # ---------------------------------
        # WELCOME PARENT
        # ---------------------------------
        return render_template(
            "parent/parent_home.html",
            parent=parent
        )


    except Exception as e:

        print("\n========== PARENT HOME ERROR ==========")
        print(e)
        print("=======================================\n")

        flash(
            "Unable to load parent portal.",
            "error"
        )

        return redirect(
            url_for("auth.login_page")
        )

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# ---------------------------------
# CHILD TEST RESULTS
# ---------------------------------
@parent_bp.route("/child_test_results")
@role_required("Parent")
def child_test_results():

    parent_id = session.get("user_id")

    if not parent_id:

        flash(
            "Parent session information not found.",
            "error"
        )

        return redirect(
            url_for("auth.login_page")
        )


    conn = None
    cursor = None

    try:

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)


        # ---------------------------------
        # GET CHILD INFORMATION
        # ---------------------------------
        cursor.execute("""
            SELECT
                student_id,
                student_name,
                email,
                phone
            FROM student
            WHERE parent_id = %s
              AND status = 'Active'
            LIMIT 1
        """, (
            parent_id,
        ))

        child = cursor.fetchone()


        # ---------------------------------
        # GET CHILD'S SUBMITTED TEST RESULTS
        # ---------------------------------
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

            JOIN student s
                ON s.student_id = ta.student_id

            JOIN test t
                ON t.test_id = ta.test_id

            JOIN subject sub
                ON sub.subject_id = t.subject_id

            WHERE s.parent_id = %s
              AND s.status = 'Active'
              AND ta.status = 'Submitted'

            ORDER BY ta.submitted_at DESC
        """, (
            parent_id,
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
            "parent/child_test_results.html",
            results=results,
            child=child,
            detailed_result=None,
            answers=[],
            weak_topics=[],
            percentage=None
        )


    except Exception as e:

        print("\n========== CHILD TEST RESULTS ERROR ==========")
        print(e)
        print("==============================================\n")

        flash(
            "Unable to load child test results.",
            "error"
        )

        return redirect(
            url_for("parent.parent_home")
        )


    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# ---------------------------------
# CHILD TEST RESULT DETAIL
# ---------------------------------
@parent_bp.route("/child_test_result/<int:attempt_id>")
@role_required("Parent")
def child_test_result(attempt_id):

    parent_id = session.get("user_id")

    if not parent_id:

        flash(
            "Parent session information not found.",
            "error"
        )

        return redirect(
            url_for("auth.login_page")
        )


    conn = None
    cursor = None

    try:

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)


        # ---------------------------------
        # GET CHILD + TEST RESULT
        #
        # The parent_id condition is important.
        # It ensures a parent can only view
        # their own child's result.
        # ---------------------------------
        cursor.execute("""
            SELECT
                ta.attempt_id,
                ta.test_id,
                ta.score,
                ta.status,
                ta.started_at,
                ta.submitted_at,

                s.student_id,
                s.student_name,
                s.email,
                s.phone,

                t.test_name,
                t.total_marks,

                sub.subject_name AS subject_name,

                NULL AS standard_name

            FROM test_attempt ta

            JOIN student s
                ON s.student_id = ta.student_id

            JOIN test t
                ON t.test_id = ta.test_id

            JOIN subject sub
                ON sub.subject_id = t.subject_id

            WHERE ta.attempt_id = %s
              AND s.parent_id = %s
              AND s.status = 'Active'
              AND ta.status = 'Submitted'
        """, (
            attempt_id,
            parent_id
        ))

        result = cursor.fetchone()


        if not result:

            flash(
                "Result not found.",
                "error"
            )

            return redirect(
                url_for("parent.child_test_results")
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
            "parent/child_test_results.html",
            results=[],
            child={
                "student_id": result["student_id"],
                "student_name": result["student_name"],
                "email": result["email"],
                "phone": result["phone"]
            },
            detailed_result=result,
            answers=answers,
            weak_topics=weak_topics,
            percentage=percentage
        )


    except Exception as e:

        print("\n========== CHILD TEST RESULT ERROR ==========")
        print(e)
        print("=============================================\n")

        flash(
            "Unable to load child test result.",
            "error"
        )

        return redirect(
            url_for("parent.child_test_results")
        )


    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()