import re
from flask import Blueprint, render_template, request, redirect, url_for, session
from session_utils import role_required
from db import conn, cursor


# ============================================================
# ADMIN BLUEPRINT
# ============================================================

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)


# ============================================================
# VALIDATION PATTERNS
# ============================================================

EMAIL_PATTERN = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)

NAME_PATTERN = re.compile(
    r"^[A-Za-z][A-Za-z .'-]{1,99}$"
)

PHONE_PATTERN = re.compile(
    r"^[0-9]{10}$"
)

PINCODE_PATTERN = re.compile(
    r"^[0-9]{6}$"
)

INSTITUTION_CODE_PATTERN = re.compile(
    r"^[A-Za-z0-9_-]{2,30}$"
)

TEXT_NAME_PATTERN = re.compile(
    r"^[A-Za-z][A-Za-z .'-]{0,99}$"
)


# ============================================================
# COMMON DATABASE HELPERS
# ============================================================

def get_institutions():

    cursor.execute("""
        SELECT DATABASE()
    """)

    current_db = cursor.fetchone()

    print("======================================")
    print("FLASK CONNECTED DATABASE:", current_db)
    print("======================================")


    cursor.execute("""
        SELECT
            institution_id,
            institution_name,
            institution_code,
            institution_category,
            status
        FROM institution
        ORDER BY institution_name ASC
    """)

    institutions = cursor.fetchall()

    print("======================================")
    print("INSTITUTIONS FOUND:", institutions)
    print("TOTAL INSTITUTIONS:", len(institutions))
    print("======================================")

    return institutions


def get_parents(institution_id=None):

    if institution_id:
        cursor.execute("""
            SELECT parent_id, name
            FROM parent
            WHERE institution_id = %s
            ORDER BY name ASC
        """, (institution_id,))
    else:
        cursor.execute("""
            SELECT parent_id, name
            FROM parent
            ORDER BY name ASC
        """)

    return cursor.fetchall()


def get_standards(institution_id=None):

    if institution_id:
        cursor.execute("""
            SELECT
                standard_id,
                standard_name
            FROM standard
            WHERE institution_id = %s
            ORDER BY standard_name ASC
        """, (institution_id,))
    else:
        cursor.execute("""
            SELECT
                standard_id,
                standard_name
            FROM standard
            ORDER BY standard_name ASC
        """)

    return cursor.fetchall()


def get_subjects(institution_id=None):

    if institution_id:

        cursor.execute("""
            SELECT
                sub.subject_id,
                sub.subject_name,
                std.standard_name
            FROM subject sub
            JOIN standard std
                ON sub.standard_id = std.standard_id
            WHERE sub.institution_id = %s
            ORDER BY
                std.standard_name ASC,
                sub.subject_name ASC
        """, (institution_id,))

    else:

        cursor.execute("""
            SELECT
                sub.subject_id,
                sub.subject_name,
                std.standard_name
            FROM subject sub
            JOIN standard std
                ON sub.standard_id = std.standard_id
            ORDER BY
                std.standard_name ASC,
                sub.subject_name ASC
        """)

    return cursor.fetchall()


def get_courses(institution_category=None):

    if institution_category:

        cursor.execute("""
            SELECT
                course_id,
                course_name,
                institution_category,
                course_level,
                stream,
                specialization
            FROM course_master
            WHERE institution_category = %s
              AND status = 'Active'
            ORDER BY course_name ASC
        """, (institution_category,))

    else:

        cursor.execute("""
            SELECT
                course_id,
                course_name,
                institution_category,
                course_level,
                stream,
                specialization
            FROM course_master
            WHERE status = 'Active'
            ORDER BY course_name ASC
        """)

    return cursor.fetchall()


def get_departments(institution_category=None):

    if institution_category:

        cursor.execute("""
            SELECT
                department_id,
                department_name,
                institution_category
            FROM department_master
            WHERE institution_category = %s
              AND status = 'Active'
            ORDER BY department_name ASC
        """, (institution_category,))

    else:

        cursor.execute("""
            SELECT
                department_id,
                department_name,
                institution_category
            FROM department_master
            WHERE status = 'Active'
            ORDER BY department_name ASC
        """)

    return cursor.fetchall()


def get_designations(institution_category=None):

    if institution_category:

        cursor.execute("""
            SELECT
                designation_id,
                designation_name,
                institution_category
            FROM designation_master
            WHERE institution_category = %s
              AND status = 'Active'
            ORDER BY designation_name ASC
        """, (institution_category,))

    else:

        cursor.execute("""
            SELECT
                designation_id,
                designation_name,
                institution_category
            FROM designation_master
            WHERE status = 'Active'
            ORDER BY designation_name ASC
        """)

    return cursor.fetchall()


# ============================================================
# ADMIN HOME
# ============================================================

@admin_bp.route("/")
@admin_bp.route("/dashboard")
@role_required("Admin")
def admin_home():

    return render_template(
        "admin_home.html"
    )


# ============================================================
# ============================================================
# INSTITUTION MANAGEMENT
# ============================================================

# ============================================================
# ADD INSTITUTION
# ============================================================

@admin_bp.route("/add_institution", methods=["GET", "POST"])
@role_required("Admin")
def add_institution():

    if request.method == "POST":

        institution_name = request.form.get(
            "institution_name", ""
        ).strip()

        institution_code = request.form.get(
            "institution_code", ""
        ).strip().upper()

        institution_category = request.form.get(
            "institution_category", ""
        ).strip()

        institution_type = request.form.get(
            "institution_type", ""
        ).strip()

        address = request.form.get(
            "address", ""
        ).strip()

        city = request.form.get(
            "city", ""
        ).strip()

        state = request.form.get(
            "state", ""
        ).strip()

        pincode = request.form.get(
            "pincode", ""
        ).strip()

        email = request.form.get(
            "email", ""
        ).strip().lower()

        phone = request.form.get(
            "phone", ""
        ).strip()

        website = request.form.get(
            "website", ""
        ).strip()

        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if not institution_name:
            return render_template(
                "add_institution.html",
                err="Institution name is required."
            )

        if not institution_code:
            return render_template(
                "add_institution.html",
                err="Institution code is required."
            )

        if not INSTITUTION_CODE_PATTERN.fullmatch(institution_code):
            return render_template(
                "add_institution.html",
                err="Institution code can contain only letters, numbers, underscore and hyphen."
            )

        if institution_category not in [
            "School",
            "Jr College",
            "Degree College"
        ]:
            return render_template(
                "add_institution.html",
                err="Please select a valid institution category."
            )

        if institution_type not in [
            "Traditional",
            "OBE"
        ]:
            return render_template(
                "add_institution.html",
                err="Please select a valid institution type."
            )

        if not address:
            return render_template(
                "add_institution.html",
                err="Address is required."
            )

        if not city:
            return render_template(
                "add_institution.html",
                err="City is required."
            )

        if not state:
            return render_template(
                "add_institution.html",
                err="State is required."
            )

        if not PINCODE_PATTERN.fullmatch(pincode):
            return render_template(
                "add_institution.html",
                err="Pincode must contain exactly 6 digits."
            )

        if not EMAIL_PATTERN.fullmatch(email):
            return render_template(
                "add_institution.html",
                err="Please enter a valid email address."
            )

        if phone and not PHONE_PATTERN.fullmatch(phone):
            return render_template(
                "add_institution.html",
                err="Phone number must contain exactly 10 digits."
            )

        try:

            cursor.execute("""
                SELECT institution_id
                FROM institution
                WHERE institution_code = %s
            """, (institution_code,))

            if cursor.fetchone():

                return render_template(
                    "add_institution.html",
                    err="Institution code already exists."
                )

            cursor.execute("""
                SELECT institution_id
                FROM institution
                WHERE email = %s
            """, (email,))

            if cursor.fetchone():

                return render_template(
                    "add_institution.html",
                    err="Institution email already exists."
                )

            cursor.execute("""
                INSERT INTO institution
                (
                    institution_name,
                    institution_code,
                    institution_category,
                    institution_type,
                    address,
                    city,
                    state,
                    pincode,
                    email,
                    phone,
                    website
                )
                VALUES
                (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s
                )
            """, (
                institution_name,
                institution_code,
                institution_category,
                institution_type,
                address,
                city,
                state,
                pincode,
                email,
                phone if phone else None,
                website if website else None
            ))

            conn.commit()

            return render_template(
                "add_institution.html",
                msg="Institution added successfully!"
            )

        except Exception as e:

            conn.rollback()

            return render_template(
                "add_institution.html",
                err="Error adding institution: " + str(e)
            )

    return render_template(
        "add_institution.html"
    )

# ============================================================
# MANAGE INSTITUTION - ASSIGN MASTER DATA
# ============================================================

@admin_bp.route("/manage_institution", methods=["GET", "POST"])
@role_required("Admin")
def manage_institution():

    try:

        # ====================================================
        # GET ALL ACTIVE INSTITUTIONS
        # ====================================================

        institutions = get_institutions()

        # ====================================================
        # DEFAULT VALUES
        # ====================================================

        selected_institution_id = None
        selected_category = None

        selected_courses = []
        selected_departments = []
        selected_designations = []

        courses = []
        departments = []
        designations = []

        # ====================================================
        # GET REQUEST
        # ====================================================

        if request.method == "GET":

            selected_institution_id = request.args.get(
                "institution_id"
            )

            # =================================================
            # NO INSTITUTION SELECTED
            # =================================================

            if not selected_institution_id:

                return render_template(
                    "manage_institution.html",

                    institutions=institutions,

                    courses=[],
                    departments=[],
                    designations=[],

                    selected_institution_id=None,
                    selected_category=None,

                    selected_courses=[],
                    selected_departments=[],
                    selected_designations=[]
                )

            # =================================================
            # GET CATEGORY FROM INSTITUTION TABLE
            # =================================================

            cursor.execute("""
                SELECT
                    institution_category
                FROM institution
                WHERE institution_id = %s
            """, (
                selected_institution_id,
            ))

            institution = cursor.fetchone()

            # =================================================
            # INSTITUTION NOT FOUND
            # =================================================

            if not institution:

                return render_template(
                    "manage_institution.html",

                    institutions=institutions,

                    courses=[],
                    departments=[],
                    designations=[],

                    selected_institution_id=selected_institution_id,
                    selected_category=None,

                    selected_courses=[],
                    selected_departments=[],
                    selected_designations=[],

                    err="Institution not found."
                )

            # =================================================
            # GET INSTITUTION CATEGORY
            # =================================================

            selected_category = institution["institution_category"]

            # =================================================
            # GET COURSES FOR CATEGORY
            # =================================================

            cursor.execute("""
                SELECT
                    course_id,
                    course_name
                FROM course_master
                WHERE institution_category = %s
                ORDER BY course_name ASC
            """, (
                selected_category,
            ))

            courses = cursor.fetchall()

            # =================================================
            # GET DEPARTMENTS FOR CATEGORY
            # =================================================

            cursor.execute("""
                SELECT
                    department_id,
                    department_name
                FROM department_master
                WHERE institution_category = %s
                ORDER BY department_name ASC
            """, (
                selected_category,
            ))

            departments = cursor.fetchall()

            # =================================================
            # GET DESIGNATIONS FOR CATEGORY
            # =================================================

            cursor.execute("""
                SELECT
                    designation_id,
                    designation_name
                FROM designation_master
                WHERE institution_category = %s
                ORDER BY designation_name ASC
            """, (
                selected_category,
            ))

            designations = cursor.fetchall()

            # =================================================
            # GET EXISTING COURSE ASSIGNMENTS
            # =================================================

            cursor.execute("""
                SELECT
                    course_id
                FROM institution_course
                WHERE institution_id = %s
            """, (
                selected_institution_id,
            ))

            selected_courses = [
                str(row["course_id"])
                for row in cursor.fetchall()
            ]

            # =================================================
            # GET EXISTING DEPARTMENT ASSIGNMENTS
            # =================================================

            cursor.execute("""
                SELECT
                    department_id
                FROM institution_department
                WHERE institution_id = %s
            """, (
                selected_institution_id,
            ))

            selected_departments = [
                str(row["department_id"])
                for row in cursor.fetchall()
            ]

            # =================================================
            # GET EXISTING DESIGNATION ASSIGNMENTS
            # =================================================

            cursor.execute("""
                SELECT
                    designation_id
                FROM institution_designation
                WHERE institution_id = %s
            """, (
                selected_institution_id,
            ))

            selected_designations = [
                str(row["designation_id"])
                for row in cursor.fetchall()
            ]

            # =================================================
            # DISPLAY PAGE
            # =================================================

            return render_template(
                "manage_institution.html",

                institutions=institutions,

                courses=courses,
                departments=departments,
                designations=designations,

                selected_institution_id=selected_institution_id,
                selected_category=selected_category,

                selected_courses=selected_courses,
                selected_departments=selected_departments,
                selected_designations=selected_designations
            )

        # ====================================================
        # POST REQUEST - SAVE ASSIGNMENTS
        # ====================================================

        institution_id = request.form.get(
            "institution_id"
        )

        # ====================================================
        # VALIDATE INSTITUTION
        # ====================================================

        if not institution_id:

            return render_template(
                "manage_institution.html",

                institutions=institutions,

                courses=[],
                departments=[],
                designations=[],

                selected_institution_id=None,
                selected_category=None,

                selected_courses=[],
                selected_departments=[],
                selected_designations=[],

                err="Please select an institution."
            )

        # ====================================================
        # GET CATEGORY FROM DATABASE
        # ====================================================

        cursor.execute("""
            SELECT
                institution_category
            FROM institution
            WHERE institution_id = %s
        """, (
            institution_id,
        ))

        institution = cursor.fetchone()

        # ====================================================
        # INSTITUTION NOT FOUND
        # ====================================================

        if not institution:

            return render_template(
                "manage_institution.html",

                institutions=institutions,

                courses=[],
                departments=[],
                designations=[],

                selected_institution_id=institution_id,
                selected_category=None,

                selected_courses=[],
                selected_departments=[],
                selected_designations=[],

                err="Institution not found."
            )

        # ====================================================
        # GET INSTITUTION CATEGORY
        # ====================================================

        institution_category = institution[
            "institution_category"
        ]

        # ====================================================
        # GET SELECTED MASTER IDs
        # ====================================================

        selected_courses = request.form.getlist(
            "courses"
        )

        selected_departments = request.form.getlist(
            "departments"
        )

        selected_designations = request.form.getlist(
            "designations"
        )

        # ====================================================
        # CLEAR EXISTING COURSE LINKS
        # ====================================================

        cursor.execute("""
            DELETE FROM institution_course
            WHERE institution_id = %s
        """, (
            institution_id,
        ))

        # ====================================================
        # CLEAR EXISTING DEPARTMENT LINKS
        # ====================================================

        cursor.execute("""
            DELETE FROM institution_department
            WHERE institution_id = %s
        """, (
            institution_id,
        ))

        # ====================================================
        # CLEAR EXISTING DESIGNATION LINKS
        # ====================================================

        cursor.execute("""
            DELETE FROM institution_designation
            WHERE institution_id = %s
        """, (
            institution_id,
        ))

        # ====================================================
        # INSERT COURSES
        # ====================================================

        for course_id in selected_courses:

            cursor.execute("""
                INSERT INTO institution_course
                (
                    institution_id,
                    course_id
                )
                SELECT
                    %s,
                    course_id
                FROM course_master
                WHERE course_id = %s
                  AND institution_category = %s
            """, (
                institution_id,
                course_id,
                institution_category
            ))

        # ====================================================
        # INSERT DEPARTMENTS
        # ====================================================

        for department_id in selected_departments:

            cursor.execute("""
                INSERT INTO institution_department
                (
                    institution_id,
                    department_id
                )
                SELECT
                    %s,
                    department_id
                FROM department_master
                WHERE department_id = %s
                  AND institution_category = %s
            """, (
                institution_id,
                department_id,
                institution_category
            ))

        # ====================================================
        # INSERT DESIGNATIONS
        # ====================================================

        for designation_id in selected_designations:

            cursor.execute("""
                INSERT INTO institution_designation
                (
                    institution_id,
                    designation_id
                )
                SELECT
                    %s,
                    designation_id
                FROM designation_master
                WHERE designation_id = %s
                  AND institution_category = %s
            """, (
                institution_id,
                designation_id,
                institution_category
            ))

        # ====================================================
        # COMMIT
        # ====================================================

        conn.commit()

        # ====================================================
        # REDIRECT BACK TO SAME INSTITUTION
        # ====================================================

        return redirect(
            url_for(
                "admin.manage_institution",
                institution_id=institution_id
            )
        )

    # ========================================================
    # ERROR HANDLING
    # ========================================================

    except Exception as e:

        conn.rollback()

        return render_template(
            "manage_institution.html",

            institutions=institutions,

            courses=courses,
            departments=departments,
            designations=designations,

            selected_institution_id=selected_institution_id,
            selected_category=selected_category,

            selected_courses=selected_courses,
            selected_departments=selected_departments,
            selected_designations=selected_designations,

            err="Database error: " + str(e)
        )

# ============================================================
# ============================================================
# VIEW INSTITUTIONS
# ============================================================

@admin_bp.route("/view_institutions")
@role_required("Admin")
def view_institutions():

    try:

        # ====================================================
        # GET ALL INSTITUTIONS
        # ====================================================

        cursor.execute("""
            SELECT
                institution_id,
                institution_name,
                institution_code,
                institution_category,
                institution_type,
                address,
                city,
                state,
                pincode,
                email,
                phone,
                website,
                status
            FROM institution
            ORDER BY institution_name ASC
        """)

        institutions = cursor.fetchall()


        # ====================================================
        # DISPLAY PAGE
        # ====================================================

        return render_template(
            "view_institutions.html",
            institutions=institutions
        )


    # ========================================================
    # ERROR HANDLING
    # ========================================================

    except Exception as e:

        return render_template(
            "view_institutions.html",

            institutions=[],

            err="Database error: " + str(e)
        )

# ============================================================
# DELETE INSTITUTION
# ============================================================

@admin_bp.route(
    "/delete_institution/<int:institution_id>",
    methods=["POST"]
)
@role_required("Admin")
def delete_institution(institution_id):

    try:

        # ====================================================
        # CHECK IF INSTITUTION EXISTS
        # ====================================================

        cursor.execute("""
            SELECT
                institution_id,
                institution_name
            FROM institution
            WHERE institution_id = %s
        """, (
            institution_id,
        ))

        institution = cursor.fetchone()


        if not institution:

            return redirect(
                url_for("admin.view_institutions")
            )


        # ====================================================
        # DELETE COURSE ASSIGNMENTS
        # ====================================================

        cursor.execute("""
            DELETE FROM institution_course
            WHERE institution_id = %s
        """, (
            institution_id,
        ))


        # ====================================================
        # DELETE DEPARTMENT ASSIGNMENTS
        # ====================================================

        cursor.execute("""
            DELETE FROM institution_department
            WHERE institution_id = %s
        """, (
            institution_id,
        ))


        # ====================================================
        # DELETE DESIGNATION ASSIGNMENTS
        # ====================================================

        cursor.execute("""
            DELETE FROM institution_designation
            WHERE institution_id = %s
        """, (
            institution_id,
        ))


        # ====================================================
        # DELETE INSTITUTION
        # ====================================================

        cursor.execute("""
            DELETE FROM institution
            WHERE institution_id = %s
        """, (
            institution_id,
        ))


        # ====================================================
        # COMMIT
        # ====================================================

        conn.commit()


        # ====================================================
        # REDIRECT TO VIEW PAGE
        # ====================================================

        return redirect(
            url_for(
                "admin.view_institutions",
                msg="Institution deleted successfully."
            )
        )


    # ========================================================
    # ERROR HANDLING
    # ========================================================

    except Exception as e:

        conn.rollback()

        return redirect(
            url_for(
                "admin.view_institutions",
                err="Unable to delete institution: " + str(e)
            )
        )
    
    
# ============================================================
# ============================================================
# STREAM MASTER
# ============================================================
# ============================================================

@admin_bp.route(
    "/stream-master",
    methods=["GET", "POST"]
)
@role_required("Admin")
def stream_master():

    msg = request.args.get("msg")
    err = request.args.get("err")

    # ========================================================
    # ADD STREAM
    # ========================================================

    if request.method == "POST":

        stream_name = request.form.get(
            "stream_name",
            ""
        ).strip()

        institution_category = request.form.get(
            "institution_category",
            ""
        ).strip()

        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if not stream_name:

            err = "Stream name is required."

        elif institution_category not in [
            "School",
            "Jr College",
            "Degree College"
        ]:

            err = "Please select a valid institution category."

        else:

            try:

                # ------------------------------------------------
                # CHECK DUPLICATE
                # ------------------------------------------------

                cursor.execute("""
                    SELECT stream_id
                    FROM stream_master
                    WHERE LOWER(stream_name) = LOWER(%s)
                      AND institution_category = %s
                """, (
                    stream_name,
                    institution_category
                ))

                if cursor.fetchone():

                    err = (
                        "This stream already exists for "
                        + institution_category
                        + "."
                    )

                else:

                    # ------------------------------------------------
                    # INSERT STREAM
                    # ------------------------------------------------

                    cursor.execute("""
                        INSERT INTO stream_master
                        (
                            stream_name,
                            institution_category
                        )
                        VALUES (%s, %s)
                    """, (
                        stream_name,
                        institution_category
                    ))

                    conn.commit()

                    msg = "Stream added successfully."

            except Exception as e:

                conn.rollback()

                err = (
                    "Error adding stream: "
                    + str(e)
                )

    # ========================================================
    # FILTER
    # ========================================================

    selected_category = request.args.get(
        "category",
        ""
    ).strip()

    # ========================================================
    # GET STREAMS
    # ========================================================

    if selected_category in [
        "School",
        "Jr College",
        "Degree College"
    ]:

        cursor.execute("""
            SELECT
                stream_id,
                stream_name,
                institution_category,
                status,
                created_at,
                updated_at
            FROM stream_master
            WHERE institution_category = %s
            ORDER BY
                institution_category,
                stream_name
        """, (
            selected_category,
        ))

    else:

        selected_category = ""

        cursor.execute("""
            SELECT
                stream_id,
                stream_name,
                institution_category,
                status,
                created_at,
                updated_at
            FROM stream_master
            ORDER BY
                institution_category,
                stream_name
        """)

    streams = cursor.fetchall()

    return render_template(
        "stream_master.html",
        streams=streams,
        selected_category=selected_category,
        msg=msg,
        err=err
    )


# ============================================================
# EDIT STREAM
# ============================================================

@admin_bp.route(
    "/edit_stream/<int:stream_id>",
    methods=["GET", "POST"]
)
@role_required("Admin")
def edit_stream(stream_id):

    err = None

    if request.method == "POST":

        stream_name = request.form.get(
            "stream_name",
            ""
        ).strip()

        institution_category = request.form.get(
            "institution_category",
            ""
        ).strip()

        status = request.form.get(
            "status",
            "Active"
        ).strip()

        if not stream_name:

            err = "Stream name is required."

        elif institution_category not in [
            "School",
            "Jr College",
            "Degree College"
        ]:

            err = "Invalid institution category."

        elif status not in [
            "Active",
            "Inactive"
        ]:

            err = "Invalid status."

        else:

            try:

                cursor.execute("""
                    SELECT stream_id
                    FROM stream_master
                    WHERE LOWER(stream_name) = LOWER(%s)
                      AND institution_category = %s
                      AND stream_id != %s
                """, (
                    stream_name,
                    institution_category,
                    stream_id
                ))

                if cursor.fetchone():

                    err = "This stream already exists."

                else:

                    cursor.execute("""
                        UPDATE stream_master
                        SET
                            stream_name = %s,
                            institution_category = %s,
                            status = %s
                        WHERE stream_id = %s
                    """, (
                        stream_name,
                        institution_category,
                        status,
                        stream_id
                    ))

                    conn.commit()

                    return redirect(
                        url_for(
                            "admin.stream_master",
                            msg="Stream has been updated successfully."
                        )
                    )

            except Exception as e:

                conn.rollback()

                err = (
                    "Unable to update stream: "
                    + str(e)
                )

    cursor.execute("""
        SELECT
            stream_id,
            stream_name,
            institution_category,
            status,
            created_at,
            updated_at
        FROM stream_master
        WHERE stream_id = %s
    """, (stream_id,))

    stream = cursor.fetchone()

    if not stream:

        return redirect(
            url_for("admin.stream_master")
        )

    return render_template(
        "edit_stream.html",
        stream=stream,
        err=err
    )


# ============================================================
# DELETE STREAM
# ============================================================

@admin_bp.route(
    "/delete_stream/<int:stream_id>",
    methods=["POST"]
)
@role_required("Admin")
def delete_stream(stream_id):

    try:

        cursor.execute("""
            DELETE FROM stream_master
            WHERE stream_id = %s
        """, (stream_id,))

        conn.commit()

        return redirect(
            url_for(
                "admin.stream_master",
                msg="Stream has been deleted successfully."
            )
        )

    except Exception:

        conn.rollback()

        return redirect(
            url_for(
                "admin.stream_master",
                err="Unable to delete stream."
            )
        )

# ============================================================
# TOGGLE STREAM STATUS
# ============================================================

@admin_bp.route(
    "/toggle_stream/<int:stream_id>",
    methods=["POST"]
)
@role_required("Admin")
def toggle_stream(stream_id):

    try:

        # ====================================================
        # GET CURRENT STATUS
        # ====================================================

        cursor.execute("""
            SELECT status
            FROM stream_master
            WHERE stream_id = %s
        """, (stream_id,))

        stream = cursor.fetchone()

        if not stream:

            return redirect(
                url_for(
                    "admin.stream_master",
                    err="Stream not found."
                )
            )

        # ====================================================
        # TOGGLE STATUS
        # ====================================================

        current_status = stream["status"]

        if current_status == "Active":
            new_status = "Inactive"
        else:
            new_status = "Active"

        # ====================================================
        # UPDATE STATUS
        # ====================================================

        cursor.execute("""
            UPDATE stream_master
            SET status = %s
            WHERE stream_id = %s
        """, (
            new_status,
            stream_id
        ))

        conn.commit()

        return redirect(
            url_for(
                "admin.stream_master",
                msg="Stream status updated successfully."
            )
        )

    except Exception as e:

        conn.rollback()

        return redirect(
            url_for(
                "admin.stream_master",
                err="Unable to update stream status: " + str(e)
            )
        )

# ============================================================
# COURSE MASTER
# ============================================================

@admin_bp.route("/course_master", methods=["GET", "POST"])
@role_required("Admin")
def course_master():

    msg = request.args.get("msg")
    err = None

    # ========================================================
    # VALID ACADEMIC YEARS BY INSTITUTION CATEGORY
    # ========================================================
    #
    # School:
    #     Not Applicable
    #
    # Jr College:
    #     FY
    #     SY
    #
    # Degree College:
    #     FY
    #     SY
    #     TY
    #     4th Year
    #
    # ========================================================

    valid_academic_years = {

        "School": [
            "Not Applicable"
        ],

        "Jr College": [
            "FY",
            "SY"
        ],

        "Degree College": [
            "FY",
            "SY",
            "TY",
            "4th Year"
        ]

    }


    # ========================================================
    # ADD COURSE
    # ========================================================

    if request.method == "POST":

        # ----------------------------------------------------
        # GET FORM DATA
        # ----------------------------------------------------

        course_name = request.form.get(
            "course_name",
            ""
        ).strip()

        institution_category = request.form.get(
            "institution_category",
            ""
        ).strip()

        academic_year = request.form.get(
            "academic_year",
            ""
        ).strip()

        status = request.form.get(
            "status",
            "Active"
        ).strip()


        # ====================================================
        # VALIDATION
        # ====================================================

        # ----------------------------------------------------
        # COURSE NAME
        # ----------------------------------------------------

        if not course_name:

            err = "Course name is required."


        # ----------------------------------------------------
        # INSTITUTION CATEGORY
        # ----------------------------------------------------

        elif institution_category not in [
            "School",
            "Jr College",
            "Degree College"
        ]:

            err = "Invalid institution category."


        # ----------------------------------------------------
        # ACADEMIC YEAR
        # ----------------------------------------------------

        elif not academic_year:

            err = "Please select an academic year."


        # ----------------------------------------------------
        # CATEGORY + ACADEMIC YEAR
        # ----------------------------------------------------

        elif academic_year not in valid_academic_years[
            institution_category
        ]:

            err = (
                "Invalid academic year selected for "
                + institution_category
                + "."
            )


        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        elif status not in [
            "Active",
            "Inactive"
        ]:

            err = "Invalid status."


        # ====================================================
        # INSERT INTO DATABASE
        # ====================================================

        if not err:

            try:

                # ------------------------------------------------
                # CHECK WHETHER COURSE ALREADY EXISTS
                # ------------------------------------------------

                cursor.execute(
                    """
                    SELECT
                        course_id

                    FROM course_master

                    WHERE LOWER(course_name) = LOWER(%s)

                      AND institution_category = %s
                    """,
                    (
                        course_name,
                        institution_category
                    )
                )

                existing_course = cursor.fetchone()


                # ------------------------------------------------
                # DUPLICATE COURSE
                # ------------------------------------------------

                if existing_course:

                    err = (
                        "This course already exists for "
                        "this institution category."
                    )


                else:

                    # ============================================
                    # INSERT INTO COURSE MASTER
                    # ============================================

                    cursor.execute(
                        """
                        INSERT INTO course_master
                        (
                            course_name,
                            institution_category,
                            status
                        )

                        VALUES
                        (
                            %s,
                            %s,
                            %s
                        )
                        """,
                        (
                            course_name,
                            institution_category,
                            status
                        )
                    )


                    # ------------------------------------------------
                    # GET NEW COURSE ID
                    # ------------------------------------------------

                    course_id = cursor.lastrowid


                    # ============================================
                    # INSERT ACADEMIC YEAR
                    # ============================================

                    cursor.execute(
                        """
                        INSERT INTO course_academic_year
                        (
                            course_id,
                            academic_year,
                            status
                        )

                        VALUES
                        (
                            %s,
                            %s,
                            %s
                        )
                        """,
                        (
                            course_id,
                            academic_year,
                            status
                        )
                    )


                    # ============================================
                    # COMMIT
                    # ============================================

                    conn.commit()


                    # ============================================
                    # SUCCESS
                    # ============================================

                    return redirect(
                        url_for(
                            "admin.course_master",
                            msg="Course has been added successfully."
                        )
                    )


            except Exception as e:

                # ------------------------------------------------
                # ROLLBACK IF ANY ERROR OCCURS
                # ------------------------------------------------

                conn.rollback()

                err = (
                    "Unable to add course: "
                    + str(e)
                )


    # ========================================================
    # LOAD ALL EXISTING COURSES
    # ========================================================

    try:

        cursor.execute(
            """
            SELECT

                c.course_id,

                c.course_name,

                c.institution_category,

                c.status,

                GROUP_CONCAT(
                    cay.academic_year
                    ORDER BY
                        CASE cay.academic_year

                            WHEN 'Not Applicable'
                                THEN 1

                            WHEN 'FY'
                                THEN 2

                            WHEN 'SY'
                                THEN 3

                            WHEN 'TY'
                                THEN 4

                            WHEN '4th Year'
                                THEN 5

                            ELSE 6

                        END

                    SEPARATOR ', '
                ) AS academic_years


            FROM course_master AS c


            LEFT JOIN course_academic_year AS cay

                ON c.course_id = cay.course_id


            GROUP BY

                c.course_id,

                c.course_name,

                c.institution_category,

                c.status


            ORDER BY

                c.course_id ASC
            """
        )


        courses = cursor.fetchall()


    except Exception as e:

        err = (
            "Unable to load courses: "
            + str(e)
        )

        courses = []


    # ========================================================
    # CONVERT GROUP_CONCAT STRING INTO LIST
    # ========================================================

    for course in courses:

        if course["academic_years"]:

            course["academic_years"] = (
                course["academic_years"]
                .split(", ")
            )

        else:

            course["academic_years"] = []


    # ========================================================
    # RENDER COURSE MASTER
    # ========================================================

    return render_template(
        "course_master.html",
        courses=courses,
        msg=msg,
        err=err
    )


# ============================================================
# EDIT COURSE
# ============================================================

@admin_bp.route(
    "/edit_course/<int:course_id>",
    methods=["GET", "POST"]
)
@role_required("Admin")
def edit_course(course_id):

    err = None


    # ========================================================
    # VALID ACADEMIC YEARS BY INSTITUTION CATEGORY
    # ========================================================

    valid_academic_years = {

        "School": [
            "Not Applicable"
        ],

        "Jr College": [
            "FY",
            "SY"
        ],

        "Degree College": [
            "FY",
            "SY",
            "TY",
            "4th Year"
        ]

    }


    # ========================================================
    # UPDATE COURSE
    # ========================================================

    if request.method == "POST":

        # ----------------------------------------------------
        # GET FORM DATA
        # ----------------------------------------------------

        course_name = request.form.get(
            "course_name",
            ""
        ).strip()

        institution_category = request.form.get(
            "institution_category",
            ""
        ).strip()

        academic_year = request.form.get(
            "academic_year",
            ""
        ).strip()

        status = request.form.get(
            "status",
            "Active"
        ).strip()


        # ====================================================
        # VALIDATION
        # ====================================================

        # ----------------------------------------------------
        # COURSE NAME
        # ----------------------------------------------------

        if not course_name:

            err = "Course name is required."


        # ----------------------------------------------------
        # INSTITUTION CATEGORY
        # ----------------------------------------------------

        elif institution_category not in [
            "School",
            "Jr College",
            "Degree College"
        ]:

            err = "Invalid institution category."


        # ----------------------------------------------------
        # ACADEMIC YEAR
        # ----------------------------------------------------

        elif not academic_year:

            err = "Please select an academic year."


        # ----------------------------------------------------
        # CATEGORY + ACADEMIC YEAR
        # ----------------------------------------------------

        elif academic_year not in valid_academic_years[
            institution_category
        ]:

            err = (
                "Invalid academic year selected for "
                + institution_category
                + "."
            )


        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        elif status not in [
            "Active",
            "Inactive"
        ]:

            err = "Invalid status."


        # ====================================================
        # UPDATE DATABASE
        # ====================================================

        if not err:

            try:

                # ============================================
                # CHECK COURSE EXISTS
                # ============================================

                cursor.execute(
                    """
                    SELECT
                        course_id

                    FROM course_master

                    WHERE course_id = %s
                    """,
                    (course_id,)
                )

                course_exists = cursor.fetchone()


                if not course_exists:

                    err = "Course not found."


                else:

                    # ========================================
                    # CHECK DUPLICATE COURSE
                    # ========================================

                    cursor.execute(
                        """
                        SELECT
                            course_id

                        FROM course_master

                        WHERE LOWER(course_name) = LOWER(%s)

                          AND institution_category = %s

                          AND course_id != %s
                        """,
                        (
                            course_name,
                            institution_category,
                            course_id
                        )
                    )

                    duplicate_course = cursor.fetchone()


                    if duplicate_course:

                        err = (
                            "This course already exists for "
                            "this institution category."
                        )


                    else:

                        # ====================================
                        # UPDATE COURSE MASTER
                        # ====================================

                        cursor.execute(
                            """
                            UPDATE course_master

                            SET

                                course_name = %s,

                                institution_category = %s,

                                status = %s

                            WHERE course_id = %s
                            """,
                            (
                                course_name,
                                institution_category,
                                status,
                                course_id
                            )
                        )


                        # ====================================
                        # DELETE OLD ACADEMIC YEAR
                        # ====================================

                        cursor.execute(
                            """
                            DELETE FROM course_academic_year

                            WHERE course_id = %s
                            """,
                            (course_id,)
                        )


                        # ====================================
                        # INSERT UPDATED ACADEMIC YEAR
                        # ====================================

                        cursor.execute(
                            """
                            INSERT INTO course_academic_year
                            (
                                course_id,
                                academic_year,
                                status
                            )

                            VALUES
                            (
                                %s,
                                %s,
                                %s
                            )
                            """,
                            (
                                course_id,
                                academic_year,
                                status
                            )
                        )


                        # ====================================
                        # COMMIT
                        # ====================================

                        conn.commit()


                        # ====================================
                        # SUCCESS
                        # ====================================

                        return redirect(
                            url_for(
                                "admin.course_master",
                                msg="Course has been updated successfully."
                            )
                        )


            except Exception as e:

                # ------------------------------------------------
                # ROLLBACK
                # ------------------------------------------------

                conn.rollback()

                err = (
                    "Unable to update course: "
                    + str(e)
                )


    # ========================================================
    # LOAD COURSE DETAILS
    # ========================================================

    try:

        cursor.execute(
            """
            SELECT

                course_id,

                course_name,

                institution_category,

                status

            FROM course_master

            WHERE course_id = %s
            """,
            (course_id,)
        )

        course = cursor.fetchone()


    except Exception as e:

        return redirect(
            url_for(
                "admin.course_master",
                msg="Unable to load course: " + str(e)
            )
        )


    # ========================================================
    # COURSE NOT FOUND
    # ========================================================

    if not course:

        return redirect(
            url_for(
                "admin.course_master",
                msg="Course not found."
            )
        )


    # ========================================================
    # LOAD ACADEMIC YEAR
    # ========================================================

    try:

        cursor.execute(
            """
            SELECT

                academic_year

            FROM course_academic_year

            WHERE course_id = %s

            ORDER BY

                CASE academic_year

                    WHEN 'Not Applicable'
                        THEN 1

                    WHEN 'FY'
                        THEN 2

                    WHEN 'SY'
                        THEN 3

                    WHEN 'TY'
                        THEN 4

                    WHEN '4th Year'
                        THEN 5

                    ELSE 6

                END
            """,
            (course_id,)
        )

        academic_year_row = cursor.fetchone()


    except Exception as e:

        academic_year_row = None

        if not err:

            err = (
                "Unable to load academic year: "
                + str(e)
            )


    # ========================================================
    # GET ACADEMIC YEAR VALUE
    # ========================================================

    if academic_year_row:

        academic_year = academic_year_row[
            "academic_year"
        ]

    else:

        academic_year = ""


    # ========================================================
    # RENDER EDIT COURSE
    # ========================================================

    return render_template(
        "edit_course.html",
        course=course,
        academic_year=academic_year,
        err=err
    )


# ============================================================
# DELETE COURSE
# ============================================================

@admin_bp.route(
    "/delete_course/<int:course_id>",
    methods=["GET"]
)
@role_required("Admin")
def delete_course(course_id):

    try:

        # ====================================================
        # CHECK COURSE EXISTS
        # ====================================================

        cursor.execute(
            """
            SELECT
                course_id,
                course_name

            FROM course_master

            WHERE course_id = %s
            """,
            (course_id,)
        )

        course = cursor.fetchone()


        # ----------------------------------------------------
        # COURSE NOT FOUND
        # ----------------------------------------------------

        if not course:

            return redirect(
                url_for(
                    "admin.course_master",
                    msg="Course not found."
                )
            )


        # ====================================================
        # DELETE COURSE
        # ====================================================
        #
        # course_academic_year has:
        #
        # ON DELETE CASCADE
        #
        # Therefore, deleting the course automatically
        # deletes its academic-year mapping.
        #
        # ====================================================

        cursor.execute(
            """
            DELETE FROM course_master

            WHERE course_id = %s
            """,
            (course_id,)
        )


        # ====================================================
        # COMMIT
        # ====================================================

        conn.commit()


        # ====================================================
        # SUCCESS
        # ====================================================

        return redirect(
            url_for(
                "admin.course_master",
                msg="Course has been deleted successfully."
            )
        )


    except Exception as e:

        # ====================================================
        # ROLLBACK
        # ====================================================

        conn.rollback()


        # ====================================================
        # ERROR
        # ====================================================

        return redirect(
            url_for(
                "admin.course_master",
                msg="Unable to delete course: " + str(e)
            )
        )

# ============================================================
# ============================================================
# DEPARTMENT MASTER
# ============================================================
# ============================================================


@admin_bp.route("/department_master", methods=["GET", "POST"])
@role_required("Admin")
def department_master():

    msg = request.args.get("msg")
    err = request.args.get("err")

    if request.method == "POST":

        department_name = request.form.get(
            "department_name", ""
        ).strip()

        institution_category = request.form.get(
            "institution_category", ""
        ).strip()

        if not department_name:

            err = "Department name is required."

        elif institution_category not in [
            "School",
            "Jr College",
            "Degree College"
        ]:

            err = "Please select a valid institution category."

        else:

            try:

                cursor.execute("""
                    SELECT department_id
                    FROM department_master
                    WHERE LOWER(department_name) = LOWER(%s)
                      AND institution_category = %s
                """, (
                    department_name,
                    institution_category
                ))

                if cursor.fetchone():

                    err = "This department already exists."

                else:

                    cursor.execute("""
                        INSERT INTO department_master
                        (
                            department_name,
                            institution_category
                        )
                        VALUES (%s, %s)
                    """, (
                        department_name,
                        institution_category
                    ))

                    conn.commit()

                    msg = "Department added successfully!"

            except Exception as e:

                conn.rollback()

                err = "Unable to add department: " + str(e)

    cursor.execute("""
        SELECT
            department_id,
            department_name,
            institution_category,
            status
        FROM department_master
        ORDER BY department_id ASC
    """)

    departments = cursor.fetchall()

    return render_template(
        "department_master.html",
        departments=departments,
        msg=msg,
        err=err
    )


# ============================================================
# EDIT DEPARTMENT
# ============================================================

@admin_bp.route(
    "/edit_department/<int:department_id>",
    methods=["GET", "POST"]
)
@role_required("Admin")
def edit_department(department_id):

    err = None

    if request.method == "POST":

        department_name = request.form.get(
            "department_name", ""
        ).strip()

        institution_category = request.form.get(
            "institution_category", ""
        ).strip()

        status = request.form.get(
            "status", "Active"
        ).strip()

        if not department_name:

            err = "Department name is required."

        elif institution_category not in [
            "School",
            "Jr College",
            "Degree College"
        ]:

            err = "Invalid institution category."

        elif status not in [
            "Active",
            "Inactive"
        ]:

            err = "Invalid status."

        else:

            try:

                # Check duplicate department
                cursor.execute("""
                    SELECT department_id
                    FROM department_master
                    WHERE LOWER(department_name) = LOWER(%s)
                      AND institution_category = %s
                      AND department_id != %s
                """, (
                    department_name,
                    institution_category,
                    department_id
                ))

                if cursor.fetchone():

                    err = "This department already exists."

                else:

                    # Update selected department
                    cursor.execute("""
                        UPDATE department_master
                        SET
                            department_name = %s,
                            institution_category = %s,
                            status = %s
                        WHERE department_id = %s
                    """, (
                        department_name,
                        institution_category,
                        status,
                        department_id
                    ))

                    conn.commit()

                    return redirect(
                        url_for(
                            "admin.department_master",
                            msg="Department has been updated successfully."
                        )
                    )

            except Exception as e:

                conn.rollback()

                err = "Unable to update department: " + str(e)


    # Get selected department
    cursor.execute("""
        SELECT *
        FROM department_master
        WHERE department_id = %s
    """, (department_id,))

    department = cursor.fetchone()

    if not department:

        return redirect(
            url_for("admin.department_master")
        )

    return render_template(
        "edit_department.html",
        department=department,
        err=err
    )

# ============================================================
# DELETE DEPARTMENT
# ============================================================

@admin_bp.route(
    "/delete_department/<int:department_id>",
    methods=["POST"]
)
@role_required("Admin")
def delete_department(department_id):

    try:

        cursor.execute("""
            DELETE FROM department_master
            WHERE department_id = %s
        """, (department_id,))

        conn.commit()

        return redirect(
            url_for(
                "admin.department_master",
                msg="Department has been deleted successfully."
            )
        )

    except Exception:

        conn.rollback()

        return redirect(
            url_for(
                "admin.department_master",
                err="Unable to delete department."
            )
        )

# ============================================================
# ============================================================
# DESIGNATION MASTER
# ============================================================
# ============================================================


@admin_bp.route("/designation_master", methods=["GET", "POST"])
@role_required("Admin")
def designation_master():

    msg = request.args.get("msg")
    err = request.args.get("err")

    if request.method == "POST":

        designation_name = request.form.get(
            "designation_name", ""
        ).strip()

        institution_category = request.form.get(
            "institution_category", ""
        ).strip()

        if not designation_name:

            err = "Designation name is required."

        elif institution_category not in [
            "School",
            "Jr College",
            "Degree College"
        ]:

            err = "Please select a valid institution category."

        else:

            try:

                cursor.execute("""
                    SELECT designation_id
                    FROM designation_master
                    WHERE LOWER(designation_name) = LOWER(%s)
                      AND institution_category = %s
                """, (
                    designation_name,
                    institution_category
                ))

                if cursor.fetchone():

                    err = "This designation already exists."

                else:

                    cursor.execute("""
                        INSERT INTO designation_master
                        (
                            designation_name,
                            institution_category
                        )
                        VALUES (%s, %s)
                    """, (
                        designation_name,
                        institution_category
                    ))

                    conn.commit()

                    msg = "Designation added successfully!"

            except Exception as e:

                conn.rollback()

                err = "Unable to add designation: " + str(e)

    cursor.execute("""
        SELECT
            designation_id,
            designation_name,
            institution_category,
            status
        FROM designation_master
        ORDER BY designation_id ASC
    """)

    designations = cursor.fetchall()

    return render_template(
        "designation_master.html",
        designations=designations,
        msg=msg,
        err=err
    )


# ============================================================
# EDIT DESIGNATION
# ============================================================

@admin_bp.route(
    "/edit_designation/<int:designation_id>",
    methods=["GET", "POST"]
)
@role_required("Admin")
def edit_designation(designation_id):

    err = None

    if request.method == "POST":

        designation_name = request.form.get(
            "designation_name", ""
        ).strip()

        institution_category = request.form.get(
            "institution_category", ""
        ).strip()

        status = request.form.get(
            "status", "Active"
        ).strip()

        if not designation_name:

            err = "Designation name is required."

        elif institution_category not in [
            "School",
            "Jr College",
            "Degree College"
        ]:

            err = "Invalid institution category."

        elif status not in [
            "Active",
            "Inactive"
        ]:

            err = "Invalid status."

        else:

            try:

                cursor.execute("""
                    SELECT designation_id
                    FROM designation_master
                    WHERE LOWER(designation_name) = LOWER(%s)
                      AND institution_category = %s
                      AND designation_id != %s
                """, (
                    designation_name,
                    institution_category,
                    designation_id
                ))

                if cursor.fetchone():

                    err = "This designation already exists."

                else:

                    cursor.execute("""
                        UPDATE designation_master
                        SET
                            designation_name = %s,
                            institution_category = %s,
                            status = %s
                        WHERE designation_id = %s
                    """, (
                        designation_name,
                        institution_category,
                        status,
                        designation_id
                    ))

                    conn.commit()

                    return redirect(
                        url_for(
                            "admin.designation_master",
                            msg="Designation has been updated successfully."
                        )
                    )

            except Exception as e:

                conn.rollback()

                err = "Unable to update designation: " + str(e)


    cursor.execute("""
        SELECT *
        FROM designation_master
        WHERE designation_id = %s
    """, (designation_id,))

    designation = cursor.fetchone()

    if not designation:

        return redirect(
            url_for("admin.designation_master")
        )

    return render_template(
        "edit_designation.html",
        designation=designation,
        err=err
    )


# ============================================================
# DELETE DESIGNATION
# ============================================================

@admin_bp.route(
    "/delete_designation/<int:designation_id>",
    methods=["POST"]
)
@role_required("Admin")
def delete_designation(designation_id):

    try:

        cursor.execute("""
            DELETE FROM designation_master
            WHERE designation_id = %s
        """, (designation_id,))

        conn.commit()

        return redirect(
            url_for(
                "admin.designation_master",
                msg="Designation has been deleted successfully."
            )
        )

    except Exception:

        conn.rollback()

        return redirect(
            url_for(
                "admin.designation_master",
                err="Unable to delete designation."
            )
        )


# ============================================================
# ============================================================
# TEACHER MANAGEMENT
# ============================================================
# ============================================================


# ============================================================
# ADD TEACHER
# ============================================================

@admin_bp.route("/add_teacher", methods=["GET", "POST"])
@role_required("Admin")
def add_teacher():

    institutions = get_institutions()

    if request.method == "GET":

        return render_template(
            "add_teacher.html",
            institutions=institutions
        )

    institution_id = request.form.get(
        "institution_id", ""
    ).strip()

    name = request.form.get(
        "name", ""
    ).strip()

    email = request.form.get(
        "email", ""
    ).strip().lower()

    password = request.form.get(
        "password", ""
    )

    mobile = request.form.get(
        "mobile", ""
    ).strip()

    department_id = request.form.get(
        "department_id", ""
    ).strip()

    designation_id = request.form.get(
        "designation_id", ""
    ).strip()

    if not institution_id:

        return render_template(
            "add_teacher.html",
            institutions=institutions,
            message="Please select an institution."
        )

    if not name:

        return render_template(
            "add_teacher.html",
            institutions=institutions,
            message="Name is required."
        )

    if not email or not EMAIL_PATTERN.fullmatch(email):

        return render_template(
            "add_teacher.html",
            institutions=institutions,
            message="Please enter a valid email address."
        )

    if not password:

        return render_template(
            "add_teacher.html",
            institutions=institutions,
            message="Password is required."
        )

    if mobile and not PHONE_PATTERN.fullmatch(mobile):

        return render_template(
            "add_teacher.html",
            institutions=institutions,
            message="Mobile number must contain exactly 10 digits."
        )

    try:

        cursor.execute("""
            SELECT teacher_id
            FROM teacher
            WHERE email = %s
        """, (email,))

        if cursor.fetchone():

            return render_template(
                "add_teacher.html",
                institutions=institutions,
                message="Teacher email already exists."
            )

        cursor.execute("""
            INSERT INTO teacher
            (
                institution_id,
                department_id,
                designation_id,
                name,
                email,
                password,
                mobile
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            institution_id,
            department_id if department_id else None,
            designation_id if designation_id else None,
            name,
            email,
            password,
            mobile if mobile else None
        ))

        conn.commit()

        return render_template(
            "add_teacher.html",
            institutions=institutions,
            message="Teacher added successfully!"
        )

    except Exception as e:

        conn.rollback()

        return render_template(
            "add_teacher.html",
            institutions=institutions,
            message="Error adding teacher: " + str(e)
        )


# ============================================================
# VIEW TEACHERS
# ============================================================

@admin_bp.route("/view_teachers")
@role_required("Admin")
def view_teachers():

    cursor.execute("""
        SELECT
            t.teacher_id,
            t.name,
            t.email,
            t.mobile,
            i.institution_name,
            d.department_name,
            dg.designation_name
        FROM teacher t

        JOIN institution i
            ON t.institution_id = i.institution_id

        LEFT JOIN department_master d
            ON t.department_id = d.department_id

        LEFT JOIN designation_master dg
            ON t.designation_id = dg.designation_id

        ORDER BY t.teacher_id ASC
    """)

    teachers = cursor.fetchall()

    return render_template(
        "view_teachers.html",
        teachers=teachers
    )


# ============================================================
# DELETE TEACHER
# ============================================================

@admin_bp.route(
    "/delete_teacher/<int:teacher_id>",
    methods=["POST"]
)
@role_required("Admin")
def delete_teacher(teacher_id):

    try:

        cursor.execute("""
            DELETE FROM teacher
            WHERE teacher_id = %s
        """, (teacher_id,))

        conn.commit()

    except Exception as e:

        conn.rollback()

        return "Error deleting teacher: " + str(e)

    return redirect(
        url_for("admin.view_teachers")
    )


# ============================================================
# ============================================================
# PARENT MANAGEMENT
# ============================================================
# ============================================================


# ============================================================
# ADD PARENT
# ============================================================

@admin_bp.route("/add_parent", methods=["GET", "POST"])
@role_required("Admin")
def add_parent():

    institutions = get_institutions()

    if request.method == "GET":

        return render_template(
            "add_parent.html",
            institutions=institutions
        )

    institution_id = request.form.get(
        "institution_id", ""
    ).strip()

    name = request.form.get(
        "name", ""
    ).strip()

    email = request.form.get(
        "email", ""
    ).strip().lower()

    password = request.form.get(
        "password", ""
    )

    mobile = request.form.get(
        "mobile", ""
    ).strip()

    if not institution_id:

        return render_template(
            "add_parent.html",
            institutions=institutions,
            message="Please select an institution."
        )

    if not name:

        return render_template(
            "add_parent.html",
            institutions=institutions,
            message="Name is required."
        )

    if not email or not EMAIL_PATTERN.fullmatch(email):

        return render_template(
            "add_parent.html",
            institutions=institutions,
            message="Please enter a valid email address."
        )

    if not password:

        return render_template(
            "add_parent.html",
            institutions=institutions,
            message="Password is required."
        )

    if mobile and not PHONE_PATTERN.fullmatch(mobile):

        return render_template(
            "add_parent.html",
            institutions=institutions,
            message="Mobile number must contain exactly 10 digits."
        )

    try:

        cursor.execute("""
            SELECT parent_id
            FROM parent
            WHERE email = %s
        """, (email,))

        if cursor.fetchone():

            return render_template(
                "add_parent.html",
                institutions=institutions,
                message="Parent email already exists."
            )

        cursor.execute("""
            INSERT INTO parent
            (
                institution_id,
                name,
                email,
                password,
                mobile
            )
            VALUES (%s, %s, %s, %s, %s)
        """, (
            institution_id,
            name,
            email,
            password,
            mobile if mobile else None
        ))

        conn.commit()

        return render_template(
            "add_parent.html",
            institutions=institutions,
            message="Parent added successfully!"
        )

    except Exception as e:

        conn.rollback()

        return render_template(
            "add_parent.html",
            institutions=institutions,
            message="Error adding parent: " + str(e)
        )


# ============================================================
# VIEW PARENTS
# ============================================================

@admin_bp.route("/view_parents")
@role_required("Admin")
def view_parents():

    cursor.execute("""
        SELECT
            p.parent_id,
            p.name,
            p.email,
            p.mobile,
            i.institution_name
        FROM parent p
        JOIN institution i
            ON p.institution_id = i.institution_id
        ORDER BY p.parent_id ASC
    """)

    parents = cursor.fetchall()

    return render_template(
        "view_parents.html",
        parents=parents
    )


# ============================================================
# DELETE PARENT
# ============================================================

@admin_bp.route(
    "/delete_parent/<int:parent_id>",
    methods=["POST"]
)
@role_required("Admin")
def delete_parent(parent_id):

    try:

        cursor.execute("""
            DELETE FROM parent
            WHERE parent_id = %s
        """, (parent_id,))

        conn.commit()

    except Exception as e:

        conn.rollback()

        return "Error deleting parent: " + str(e)

    return redirect(
        url_for("admin.view_parents")
    )


# ============================================================
# ============================================================
# STUDENT MANAGEMENT
# ============================================================
# ============================================================


# ============================================================
# ADD STUDENT
# ============================================================

@admin_bp.route("/add_student", methods=["GET", "POST"])
@role_required("Admin")
def add_student():

    institutions = get_institutions()

    if request.method == "GET":

        return render_template(
            "add_student.html",
            institutions=institutions,
            parents=[],
            standards=[]
        )

    institution_id = request.form.get(
        "institution_id", ""
    ).strip()

    parent_id = request.form.get(
        "parent_id", ""
    ).strip()

    standard_id = request.form.get(
        "standard_id", ""
    ).strip()

    admission_no = request.form.get(
        "admission_no", ""
    ).strip()

    roll_no = request.form.get(
        "roll_no", ""
    ).strip()

    division = request.form.get(
        "division", ""
    ).strip()

    name = request.form.get(
        "name", ""
    ).strip()

    email = request.form.get(
        "email", ""
    ).strip().lower()

    password = request.form.get(
        "password", ""
    )

    mobile = request.form.get(
        "mobile", ""
    ).strip()

    parents = get_parents(institution_id) if institution_id else []
    standards = get_standards(institution_id) if institution_id else []

    if not institution_id:

        message = "Please select an institution."

    elif not parent_id:

        message = "Please select a parent."

    elif not standard_id:

        message = "Please select a standard."

    elif not roll_no:

        message = "Roll number is required."

    elif not name:

        message = "Student name is required."

    elif not email or not EMAIL_PATTERN.fullmatch(email):

        message = "Please enter a valid email address."

    elif not password:

        message = "Password is required."

    elif mobile and not PHONE_PATTERN.fullmatch(mobile):

        message = "Mobile number must contain exactly 10 digits."

    else:

        try:

            cursor.execute("""
                SELECT student_id
                FROM student
                WHERE email = %s
            """, (email,))

            if cursor.fetchone():

                message = "Student email already exists."

            else:

                cursor.execute("""
                    INSERT INTO student
                    (
                        institution_id,
                        parent_id,
                        standard_id,
                        admission_no,
                        roll_no,
                        division,
                        name,
                        email,
                        password,
                        mobile
                    )
                    VALUES
                    (
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s
                    )
                """, (
                    institution_id,
                    parent_id,
                    standard_id,
                    admission_no if admission_no else None,
                    roll_no,
                    division if division else None,
                    name,
                    email,
                    password,
                    mobile if mobile else None
                ))

                conn.commit()

                message = "Student added successfully!"

        except Exception as e:

            conn.rollback()

            message = "Error adding student: " + str(e)

    return render_template(
        "add_student.html",
        institutions=institutions,
        parents=parents,
        standards=standards,
        message=message
    )


# ============================================================
# VIEW STUDENTS
# ============================================================

@admin_bp.route("/view_students")
@role_required("Admin")
def view_students():

    cursor.execute("""
        SELECT
            s.student_id,
            s.admission_no,
            s.roll_no,
            s.division,
            s.name,
            s.email,
            s.mobile,
            p.name AS parent_name,
            st.standard_name,
            i.institution_name
        FROM student s

        JOIN parent p
            ON s.parent_id = p.parent_id

        JOIN standard st
            ON s.standard_id = st.standard_id

        JOIN institution i
            ON s.institution_id = i.institution_id

        ORDER BY s.student_id ASC
    """)

    students = cursor.fetchall()

    return render_template(
        "view_students.html",
        students=students
    )


# ============================================================
# DELETE STUDENT
# ============================================================

@admin_bp.route(
    "/delete_student/<int:student_id>",
    methods=["POST"]
)
@role_required("Admin")
def delete_student(student_id):

    try:

        cursor.execute("""
            DELETE FROM student
            WHERE student_id = %s
        """, (student_id,))

        conn.commit()

    except Exception as e:

        conn.rollback()

        return "Error deleting student: " + str(e)

    return redirect(
        url_for("admin.view_students")
    )


# ============================================================
# ============================================================
# STANDARD MANAGEMENT
# ============================================================
# ============================================================


@admin_bp.route("/add_standard", methods=["GET", "POST"])
@role_required("Admin")
def add_standard():

    msg = None
    err = None

    institutions = get_institutions()

    if request.method == "POST":

        institution_id = request.form.get(
            "institution_id", ""
        ).strip()

        course_id = request.form.get(
            "course_id", ""
        ).strip()

        standard_name = request.form.get(
            "standard_name", ""
        ).strip()

        if not institution_id:

            err = "Please select an institution."

        elif not course_id:

            err = "Please select a course."

        elif not standard_name:

            err = "Standard name is required."

        elif len(standard_name) > 50:

            err = "Standard name cannot exceed 50 characters."

        else:

            try:

                cursor.execute("""
                    SELECT standard_id
                    FROM standard
                    WHERE institution_id = %s
                      AND course_id = %s
                      AND LOWER(standard_name) = LOWER(%s)
                """, (
                    institution_id,
                    course_id,
                    standard_name
                ))

                if cursor.fetchone():

                    err = "This standard already exists."

                else:

                    cursor.execute("""
                        INSERT INTO standard
                        (
                            institution_id,
                            course_id,
                            standard_name
                        )
                        VALUES (%s, %s, %s)
                    """, (
                        institution_id,
                        course_id,
                        standard_name
                    ))

                    conn.commit()

                    msg = "Standard added successfully!"

            except Exception as e:

                conn.rollback()

                err = "Unable to add standard: " + str(e)

    standards = get_standards()

    courses = get_courses()

    return render_template(
        "add_standard.html",
        msg=msg,
        err=err,
        institutions=institutions,
        courses=courses,
        standards=standards
    )


# ============================================================
# EDIT STANDARD
# ============================================================

@admin_bp.route(
    "/edit_standard/<int:standard_id>",
    methods=["GET", "POST"]
)
@role_required("Admin")
def edit_standard(standard_id):

    err = None

    institutions = get_institutions()
    courses = get_courses()

    if request.method == "POST":

        institution_id = request.form.get(
            "institution_id", ""
        ).strip()

        course_id = request.form.get(
            "course_id", ""
        ).strip()

        standard_name = request.form.get(
            "standard_name", ""
        ).strip()

        if not institution_id:

            err = "Please select an institution."

        elif not course_id:

            err = "Please select a course."

        elif not standard_name:

            err = "Standard name is required."

        elif len(standard_name) > 50:

            err = "Standard name cannot exceed 50 characters."

        else:

            try:

                cursor.execute("""
                    SELECT standard_id
                    FROM standard
                    WHERE institution_id = %s
                      AND course_id = %s
                      AND LOWER(standard_name) = LOWER(%s)
                      AND standard_id != %s
                """, (
                    institution_id,
                    course_id,
                    standard_name,
                    standard_id
                ))

                if cursor.fetchone():

                    err = "This standard already exists."

                else:

                    cursor.execute("""
                        UPDATE standard
                        SET
                            institution_id = %s,
                            course_id = %s,
                            standard_name = %s
                        WHERE standard_id = %s
                    """, (
                        institution_id,
                        course_id,
                        standard_name,
                        standard_id
                    ))

                    conn.commit()

                    return redirect(
                        url_for(
                            "admin.add_standard"
                        )
                    )

            except Exception as e:

                conn.rollback()

                err = "Unable to update standard: " + str(e)

    cursor.execute("""
        SELECT *
        FROM standard
        WHERE standard_id = %s
    """, (standard_id,))

    standard = cursor.fetchone()

    if not standard:

        return redirect(
            url_for("admin.add_standard")
        )

    return render_template(
        "edit_standard.html",
        standard=standard,
        institutions=institutions,
        courses=courses,
        err=err
    )


# ============================================================
# DELETE STANDARD
# ============================================================

@admin_bp.route(
    "/delete_standard/<int:standard_id>",
    methods=["POST"]
)
@role_required("Admin")
def delete_standard(standard_id):

    try:

        cursor.execute("""
            DELETE FROM standard
            WHERE standard_id = %s
        """, (standard_id,))

        conn.commit()

    except Exception:

        conn.rollback()

    return redirect(
        url_for("admin.add_standard")
    )

# ============================================================
# ============================================================
# SUBJECT MASTER
# ============================================================
# ============================================================


@admin_bp.route(
    "/subject-master",
    methods=["GET", "POST"]
)
@role_required("Admin")
def subject_master():

    msg = request.args.get("msg")
    err = request.args.get("err")

    # ========================================================
    # ADD SUBJECT
    # ========================================================

    if request.method == "POST":

        subject_name = request.form.get(
            "subject_name",
            ""
        ).strip()

        course_id = request.form.get(
            "course_id",
            ""
        ).strip()

        institution_category = request.form.get(
            "institution_category",
            ""
        ).strip()

        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if not subject_name:

            err = "Subject name is required."

        elif not course_id:

            err = "Please select a course."

        elif institution_category not in [
            "School",
            "Jr College",
            "Degree College"
        ]:

            err = "Please select a valid institution category."

        else:

            try:

                # ------------------------------------------------
                # CHECK WHETHER COURSE EXISTS
                # ------------------------------------------------

                cursor.execute("""
                    SELECT course_id
                    FROM course_master
                    WHERE course_id = %s
                      AND institution_category = %s
                      AND status = 'Active'
                """, (
                    course_id,
                    institution_category
                ))

                course = cursor.fetchone()

                if not course:

                    err = (
                        "The selected course is not available "
                        "for this institution category."
                    )

                else:

                    # ------------------------------------------------
                    # CHECK DUPLICATE SUBJECT
                    # ------------------------------------------------

                    cursor.execute("""
                        SELECT subject_master_id
                        FROM subject_master
                        WHERE LOWER(subject_name) = LOWER(%s)
                          AND course_id = %s
                          AND institution_category = %s
                    """, (
                        subject_name,
                        course_id,
                        institution_category
                    ))

                    existing_subject = cursor.fetchone()

                    if existing_subject:

                        err = (
                            "This subject already exists "
                            "for the selected course."
                        )

                    else:

                        # ------------------------------------------------
                        # INSERT SUBJECT
                        # ------------------------------------------------

                        cursor.execute("""
                            INSERT INTO subject_master
                            (
                                subject_name,
                                course_id,
                                institution_category
                            )
                            VALUES (%s, %s, %s)
                        """, (
                            subject_name,
                            course_id,
                            institution_category
                        ))

                        conn.commit()

                        msg = "Subject added successfully."

            except Exception as e:

                conn.rollback()

                err = (
                    "Error adding subject: "
                    + str(e)
                )

    # ========================================================
    # FILTER
    # ========================================================

    selected_category = request.args.get(
        "category",
        ""
    ).strip()

    # ========================================================
    # GET COURSES
    # ========================================================

    cursor.execute("""
        SELECT
            course_id,
            course_name,
            institution_category
        FROM course_master
        WHERE status = 'Active'
        ORDER BY
            institution_category,
            course_name
    """)

    courses = cursor.fetchall()

    # ========================================================
    # GET SUBJECTS
    # ========================================================

    if selected_category in [
        "School",
        "Jr College",
        "Degree College"
    ]:

        cursor.execute("""
            SELECT
                sm.subject_master_id,
                sm.subject_name,
                sm.course_id,
                cm.course_name,
                sm.institution_category,
                sm.status,
                sm.created_at,
                sm.updated_at
            FROM subject_master sm
            INNER JOIN course_master cm
                ON sm.course_id = cm.course_id
            WHERE sm.institution_category = %s
            ORDER BY
                sm.institution_category,
                cm.course_name,
                sm.subject_name
        """, (
            selected_category,
        ))

    else:

        selected_category = ""

        cursor.execute("""
            SELECT
                sm.subject_master_id,
                sm.subject_name,
                sm.course_id,
                cm.course_name,
                sm.institution_category,
                sm.status,
                sm.created_at,
                sm.updated_at
            FROM subject_master sm
            INNER JOIN course_master cm
                ON sm.course_id = cm.course_id
            ORDER BY
                sm.institution_category,
                cm.course_name,
                sm.subject_name
        """)

    subjects = cursor.fetchall()

    # ========================================================
    # RENDER
    # ========================================================

    return render_template(
        "subject_master.html",
        subjects=subjects,
        courses=courses,
        selected_category=selected_category,
        msg=msg,
        err=err
    )


# ============================================================
# EDIT SUBJECT
# ============================================================


@admin_bp.route(
    "/edit_subject/<int:subject_master_id>",
    methods=["GET", "POST"]
)
@role_required("Admin")
def edit_subject(subject_master_id):

    err = None

    # ========================================================
    # UPDATE SUBJECT
    # ========================================================

    if request.method == "POST":

        subject_name = request.form.get(
            "subject_name",
            ""
        ).strip()

        course_id = request.form.get(
            "course_id",
            ""
        ).strip()

        institution_category = request.form.get(
            "institution_category",
            ""
        ).strip()

        status = request.form.get(
            "status",
            "Active"
        ).strip()

        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if not subject_name:

            err = "Subject name is required."

        elif not course_id:

            err = "Please select a course."

        elif institution_category not in [
            "School",
            "Jr College",
            "Degree College"
        ]:

            err = "Invalid institution category."

        elif status not in [
            "Active",
            "Inactive"
        ]:

            err = "Invalid status."

        else:

            try:

                # ------------------------------------------------
                # CHECK COURSE
                # ------------------------------------------------

                cursor.execute("""
                    SELECT course_id
                    FROM course_master
                    WHERE course_id = %s
                      AND institution_category = %s
                      AND status = 'Active'
                """, (
                    course_id,
                    institution_category
                ))

                course = cursor.fetchone()

                if not course:

                    err = (
                        "The selected course is not available "
                        "for this institution category."
                    )

                else:

                    # ------------------------------------------------
                    # CHECK DUPLICATE
                    # ------------------------------------------------

                    cursor.execute("""
                        SELECT subject_master_id
                        FROM subject_master
                        WHERE LOWER(subject_name) = LOWER(%s)
                          AND course_id = %s
                          AND institution_category = %s
                          AND subject_master_id != %s
                    """, (
                        subject_name,
                        course_id,
                        institution_category,
                        subject_master_id
                    ))

                    existing_subject = cursor.fetchone()

                    if existing_subject:

                        err = (
                            "This subject already exists "
                            "for the selected course."
                        )

                    else:

                        # ------------------------------------------------
                        # UPDATE
                        # ------------------------------------------------

                        cursor.execute("""
                            UPDATE subject_master
                            SET
                                subject_name = %s,
                                course_id = %s,
                                institution_category = %s,
                                status = %s
                            WHERE subject_master_id = %s
                        """, (
                            subject_name,
                            course_id,
                            institution_category,
                            status,
                            subject_master_id
                        ))

                        conn.commit()

                        return redirect(
                            url_for(
                                "admin.subject_master",
                                msg="Subject has been updated successfully."
                            )
                        )

            except Exception as e:

                conn.rollback()

                err = (
                    "Unable to update subject: "
                    + str(e)
                )

    # ========================================================
    # GET SUBJECT
    # ========================================================

    cursor.execute("""
        SELECT
            subject_master_id,
            subject_name,
            course_id,
            institution_category,
            status,
            created_at,
            updated_at
        FROM subject_master
        WHERE subject_master_id = %s
    """, (
        subject_master_id,
    ))

    subject = cursor.fetchone()

    # --------------------------------------------------------
    # SUBJECT NOT FOUND
    # --------------------------------------------------------

    if not subject:

        return redirect(
            url_for("admin.subject_master")
        )

    # ========================================================
    # GET COURSES
    # ========================================================

    cursor.execute("""
        SELECT
            course_id,
            course_name,
            institution_category
        FROM course_master
        WHERE status = 'Active'
        ORDER BY
            institution_category,
            course_name
    """)

    courses = cursor.fetchall()

    # ========================================================
    # RENDER EDIT PAGE
    # ========================================================

    return render_template(
        "edit_subject.html",
        subject=subject,
        courses=courses,
        err=err
    )


# ============================================================
# TOGGLE SUBJECT STATUS
# ============================================================


@admin_bp.route(
    "/toggle_subject/<int:subject_master_id>",
    methods=["POST"]
)
@role_required("Admin")
def toggle_subject(subject_master_id):

    try:

        # ====================================================
        # GET CURRENT STATUS
        # ====================================================

        cursor.execute("""
            SELECT status
            FROM subject_master
            WHERE subject_master_id = %s
        """, (
            subject_master_id,
        ))

        subject = cursor.fetchone()

        if not subject:

            return redirect(
                url_for(
                    "admin.subject_master",
                    err="Subject not found."
                )
            )

        # ====================================================
        # TOGGLE STATUS
        # ====================================================

        current_status = subject["status"]

        if current_status == "Active":

            new_status = "Inactive"

        else:

            new_status = "Active"

        # ====================================================
        # UPDATE STATUS
        # ====================================================

        cursor.execute("""
            UPDATE subject_master
            SET status = %s
            WHERE subject_master_id = %s
        """, (
            new_status,
            subject_master_id
        ))

        conn.commit()

        if new_status == "Inactive":

            message = "Subject has been deactivated successfully."

        else:

            message = "Subject has been activated successfully."

        return redirect(
            url_for(
                "admin.subject_master",
                msg=message
            )
        )

    except Exception as e:

        conn.rollback()

        return redirect(
            url_for(
                "admin.subject_master",
                err="Unable to update subject status: " + str(e)
            )
        )


# ============================================================
# DELETE SUBJECT
# ============================================================


@admin_bp.route(
    "/delete_subject/<int:subject_master_id>",
    methods=["POST"]
)
@role_required("Admin")
def delete_subject(subject_master_id):

    try:

        # ====================================================
        # CHECK SUBJECT
        # ====================================================

        cursor.execute("""
            SELECT subject_master_id
            FROM subject_master
            WHERE subject_master_id = %s
        """, (
            subject_master_id,
        ))

        subject = cursor.fetchone()

        if not subject:

            return redirect(
                url_for(
                    "admin.subject_master",
                    err="Subject not found."
                )
            )

        # ====================================================
        # DELETE SUBJECT
        # ====================================================

        cursor.execute("""
            DELETE FROM subject_master
            WHERE subject_master_id = %s
        """, (
            subject_master_id,
        ))

        conn.commit()

        return redirect(
            url_for(
                "admin.subject_master",
                msg="Subject has been deleted successfully."
            )
        )

    except Exception as e:

        conn.rollback()

        return redirect(
            url_for(
                "admin.subject_master",
                err="Unable to delete subject: " + str(e)
            )
        )
# ============================================================
# ============================================================
# CHAPTER MANAGEMENT
# ============================================================
# ============================================================


@admin_bp.route("/add_chapter", methods=["GET", "POST"])
@role_required("Admin")
def add_chapter():

    msg = None
    err = None

    subjects = get_subjects()

    if request.method == "POST":

        subject_id = request.form.get(
            "subject_id", ""
        ).strip()

        chapter_number = request.form.get(
            "chapter_number", ""
        ).strip()

        chapter_name = request.form.get(
            "chapter_name", ""
        ).strip()

        if not subject_id:

            err = "Please select a subject."

        elif not chapter_name:

            err = "Chapter name is required."

        elif len(chapter_name) > 200:

            err = "Chapter name cannot exceed 200 characters."

        elif chapter_number and (
            not chapter_number.isdigit()
            or int(chapter_number) <= 0
        ):

            err = "Chapter number must be a valid positive integer."

        else:

            try:

                chapter_num_value = (
                    int(chapter_number)
                    if chapter_number
                    else None
                )

                cursor.execute("""
                    SELECT chapter_id
                    FROM chapter
                    WHERE subject_id = %s
                      AND (
                            chapter_number = %s
                            OR LOWER(chapter_name) = LOWER(%s)
                      )
                """, (
                    subject_id,
                    chapter_num_value,
                    chapter_name
                ))

                if cursor.fetchone():

                    err = "This chapter already exists."

                else:

                    cursor.execute("""
                        INSERT INTO chapter
                        (
                            subject_id,
                            chapter_number,
                            chapter_name
                        )
                        VALUES (%s, %s, %s)
                    """, (
                        subject_id,
                        chapter_num_value,
                        chapter_name
                    ))

                    conn.commit()

                    msg = "Chapter added successfully!"

            except Exception as e:

                conn.rollback()

                err = "Unable to add chapter: " + str(e)

    cursor.execute("""
        SELECT
            ch.chapter_id,
            ch.chapter_number,
            ch.chapter_name,
            sub.subject_name
        FROM chapter ch
        JOIN subject sub
            ON ch.subject_id = sub.subject_id
        ORDER BY ch.chapter_id ASC
    """)

    chapters = cursor.fetchall()

    return render_template(
        "add_chapter.html",
        msg=msg,
        err=err,
        subjects=subjects,
        chapters=chapters
    )


# ============================================================
# EDIT CHAPTER
# ============================================================

@admin_bp.route(
    "/edit_chapter/<int:chapter_id>",
    methods=["GET", "POST"]
)
@role_required("Admin")
def edit_chapter(chapter_id):

    err = None

    if request.method == "POST":

        subject_id = request.form.get(
            "subject_id", ""
        ).strip()

        chapter_number = request.form.get(
            "chapter_number", ""
        ).strip()

        chapter_name = request.form.get(
            "chapter_name", ""
        ).strip()

        if not subject_id:

            err = "Please select a subject."

        elif not chapter_name:

            err = "Chapter name is required."

        elif chapter_number and (
            not chapter_number.isdigit()
            or int(chapter_number) <= 0
        ):

            err = "Invalid chapter number."

        else:

            try:

                chapter_num_value = (
                    int(chapter_number)
                    if chapter_number
                    else None
                )

                cursor.execute("""
                    SELECT chapter_id
                    FROM chapter
                    WHERE subject_id = %s
                      AND (
                            chapter_number = %s
                            OR LOWER(chapter_name) = LOWER(%s)
                      )
                      AND chapter_id != %s
                """, (
                    subject_id,
                    chapter_num_value,
                    chapter_name,
                    chapter_id
                ))

                if cursor.fetchone():

                    err = "Another chapter with these details already exists."

                else:

                    cursor.execute("""
                        UPDATE chapter
                        SET
                            subject_id = %s,
                            chapter_number = %s,
                            chapter_name = %s
                        WHERE chapter_id = %s
                    """, (
                        subject_id,
                        chapter_num_value,
                        chapter_name,
                        chapter_id
                    ))

                    conn.commit()

                    return redirect(
                        url_for(
                            "admin.add_chapter"
                        )
                    )

            except Exception as e:

                conn.rollback()

                err = "Unable to update chapter: " + str(e)

    cursor.execute("""
        SELECT *
        FROM chapter
        WHERE chapter_id = %s
    """, (chapter_id,))

    chapter = cursor.fetchone()

    if not chapter:

        return redirect(
            url_for("admin.add_chapter")
        )

    subjects = get_subjects()

    return render_template(
        "edit_chapter.html",
        chapter=chapter,
        subjects=subjects,
        err=err
    )


# ============================================================
# DELETE CHAPTER
# ============================================================

@admin_bp.route(
    "/delete_chapter/<int:chapter_id>",
    methods=["POST"]
)
@role_required("Admin")
def delete_chapter(chapter_id):

    try:

        cursor.execute("""
            DELETE FROM chapter
            WHERE chapter_id = %s
        """, (chapter_id,))

        conn.commit()

    except Exception:

        conn.rollback()

    return redirect(
        url_for("admin.add_chapter")
    )


# ============================================================
# ============================================================
# STUDENT PROGRESS
# ============================================================
# ============================================================

@admin_bp.route("/student_progress_for_admin")
@role_required("Admin")
def student_progress_for_admin():

    return render_template(
        "student_progress_for_admin.html"
    )


# ============================================================
# ============================================================
# ADMIN PROFILE
# ============================================================
# ============================================================

@admin_bp.route(
    "/profile",
    methods=["GET", "POST"]
)
@role_required("Admin")
def admin_profile():

    admin_id = session.get(
        "user_id"
    )

    msg = None
    err = None

    if not admin_id:

        return redirect(
            url_for("auth.login")
        )

    if request.method == "POST":

        name = request.form.get(
            "name", ""
        ).strip()

        email = request.form.get(
            "email", ""
        ).strip().lower()

        if not name:

            err = "Name is required."

        elif len(name) > 100:

            err = "Name cannot exceed 100 characters."

        elif not EMAIL_PATTERN.fullmatch(email):

            err = "Please enter a valid email address."

        else:

            try:

                cursor.execute("""
                    SELECT admin_id
                    FROM admin
                    WHERE email = %s
                      AND admin_id != %s
                """, (
                    email,
                    admin_id
                ))

                if cursor.fetchone():

                    err = "Email is already in use."

                else:

                    cursor.execute("""
                        UPDATE admin
                        SET
                            name = %s,
                            email = %s
                        WHERE admin_id = %s
                    """, (
                        name,
                        email,
                        admin_id
                    ))

                    conn.commit()

                    session["name"] = name

                    msg = "Profile updated successfully!"

            except Exception:

                conn.rollback()

                err = "Unable to update profile."

    cursor.execute("""
        SELECT
            admin_id,
            name,
            email
        FROM admin
        WHERE admin_id = %s
    """, (admin_id,))

    admin_data = cursor.fetchone()

    if not admin_data:

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "admin_profile.html",
        admin=admin_data,
        msg=msg,
        err=err
    )