🎓 Student Management System (SMS)

A comprehensive Django-based web application for managing students, courses, attendance, and marks with role‑based access for teachers and students.

It includes separate dashboards, full CRUD operations for teachers, read-only views for students, and seamless integration with AWS S3 for attendance exports and AWS SNS for exam notifications.

📋 Overview

The Student Management System streamlines academic administration by providing:

🧑‍🏫 Role‑based dashboards: Teachers manage all data; students view only their records.

🔒 Secure authentication: Sign up with a role and redirect to the appropriate dashboard.

📝 Complete student lifecycle: Add, edit, delete, and view student profiles.

📚 Course & enrollment management: Create courses and enroll students.

📅 Attendance tracking: Mark attendance per course and date.

🖊 Exams & marks: Schedule exams and record marks.

☁️ AWS integration:

Export attendance as plain text files to Amazon S3.

Send exam notifications via Amazon SNS.

🔗 REST API (optional) via Django REST Framework for programmatic access.

✨ Features
🧑‍🏫 For Teachers

✅ Full CRUD operations on students, courses, enrollments, attendance, exams, and marks.
✅ Mark attendance for specific courses and dates.
✅ Export attendance to AWS S3 as a downloadable .txt file.
✅ Create/update exams – automatically notify enrolled students via SNS.
✅ View all records in a clean, tabular format.

👀 For Students

👀 Read-only access to personal profile, enrollments, attendance, and marks.
👀 View personal dashboard with aggregated information.

🌐 General

🔐 Role-based redirection: Unauthenticated users → login page; logged-in users → dashboard.
🧠 Graceful handling of missing profiles (e.g., superusers created via createsuperuser).
☁️ Cloud-ready AWS integrations for export and notifications.
📡 REST API with filtering, searching, and pagination (teachers only for write operations).

🛠 Technology Stack
Layer	Technology
Backend	Python 3.13, Django 5.x
Database	SQLite (default, easily switchable)
Frontend	HTML, CSS (simple templates)
Authentication	Django built-in auth + UserProfile
API	Django REST Framework, django-filters
Cloud Services	AWS S3 (storage), AWS SNS (notifications)
Other	boto3, python-dotenv 


📁 Project Structure

student_management/
├── manage.py
├── db.sqlite3
├── student_management/          # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/                     # Custom user profiles & auth
│   ├── models.py (UserProfile)
│   ├── views.py (signup, login, logout)
│   └── templates/accounts/
├── students/                     # Student management
│   ├── models.py (Student)
│   ├── views.py (dashboards & CRUD)
│   └── templates/students/
├── courses/                      # Courses & enrollments
│   ├── models.py (Course, Enrollment)
│   └── views.py
├── attendance/                   # Attendance tracking
│   ├── models.py (Attendance)
│   ├── views.py (including AWS S3 export)
│   └── templates/attendance/
├── marks/                         # Exams & marks
│   ├── models.py (Exam, Marks)
│   ├── views.py (including AWS SNS notifications)
│   └── templates/marks/
├── api/                           # REST API
│   ├── serializers.py
│   ├── views.py (ViewSets)
│   ├── permissions.py
│   └── urls.py
└── requirements.txt


☁️ AWS Integration Details
📤 Attendance Export to S3

Teacher clicks "Export Attendance to AWS S3"

App fetches records → converts to .txt with timestamp → uploads to S3 → provides download link

Bucket must be publicly readable or use pre-signed URLs.

📩 Exam Notifications via SNS

Creating/updating an exam:

Finds enrolled students

Retrieves their emails

Publishes a message to SNS topic

Subscribed emails receive notifications

Student emails must be confirmed in SNS (manual or automated during signup).

📱 Usage
Sign Up

Visit /accounts/signup/ → choose role (Teacher/Student)

Log in with credentials

Login & Redirection

Unauthenticated users → /accounts/login/

Teachers → /students/teacher/dashboard/

Students → /students/student/dashboard/

Teacher Dashboard

Manage Students, Courses, Enrollments

Mark attendance & export to S3

Schedule Exams → automatic SNS notifications

Record Marks for each student

Student Dashboard

View profile, enrolled courses, attendance, and marks (read-only)

REST API

Base: /api/ (authentication required)

Endpoints: /api/students/, /api/courses/, /api/enrollments/, /api/attendance/, /api/exams/, /api/marks/

Teachers: full read/write

Students: read-only own data

Supports filtering, searching, ordering, pagination
