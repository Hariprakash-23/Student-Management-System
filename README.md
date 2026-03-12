Student Management System (SMS)
A comprehensive Django-based web application for managing students, courses, attendance, and marks with role‑based access for teachers and students. The system features separate dashboards, full CRUD operations for teachers, read‑only views for students, and seamless integration with AWS S3 for attendance exports and AWS SNS for exam notifications.

📋 Overview
The Student Management System streamlines academic administration by providing:

Role‑based dashboards: Teachers manage all data; students view their own records.

Secure authentication: Users sign up with a role (teacher/student) and are redirected to the appropriate dashboard after login.

Complete student lifecycle: Add, edit, delete, and view student profiles.

Course & enrollment management: Create courses and enroll students.

Attendance tracking: Mark attendance per course and date.

Exams & marks: Schedule exams and record marks.

AWS integration:

Export attendance records as plain text files to Amazon S3.

Send exam notifications via Amazon SNS to all enrolled students.

REST API (optional) for programmatic access, built with Django REST Framework.

✨ Features
For Teachers
✅ Full CRUD on students, courses, enrollments, attendance, exams, and marks.

✅ Mark attendance for a specific course and date.

✅ Export attendance to AWS S3 as a downloadable .txt file.

✅ Create/update exams – automatically notifies enrolled students via SNS.

✅ View all records in a clean, tabular format.

For Students
👀 Read‑only access to their own profile, enrollments, attendance, and marks.

👀 View personal dashboard with aggregated information.

General
🔐 Role‑based redirection: unauthenticated users are sent to login; logged‑in users go to their respective dashboard.

🧠 Graceful handling of missing profiles (e.g., for superusers created via createsuperuser).

☁️ Cloud‑ready AWS integrations for export and notifications.

📡 REST API with filtering, searching, and pagination (teachers only for write operations).

🛠️ Technology Stack
Layer	Technology
Backend	Python 3.13, Django 5.x
Database	SQLite (default), easily switchable
Frontend	HTML, CSS (simple templates)
Authentication	Django built‑in auth + UserProfile
API	Django REST Framework, django‑filters
Cloud Services	AWS S3 (storage), AWS SNS (notifications)
Other	boto3, python‑dotenv (optional)
📁 Project Structure
text
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
├── students/                      # Student management
│   ├── models.py (Student)
│   ├── views.py (dashboards & CRUD)
│   └── templates/students/
├── courses/                        # Courses & enrollments
│   ├── models.py (Course, Enrollment)
│   └── views.py
├── attendance/                     # Attendance tracking
│   ├── models.py (Attendance)
│   ├── views.py (including AWS S3 export)
│   └── templates/attendance/
├── marks/                           # Exams & marks
│   ├── models.py (Exam, Marks)
│   ├── views.py (including AWS SNS notifications)
│   └── templates/marks/
├── api/                              # REST API
│   ├── serializers.py
│   ├── views.py (ViewSets)
│   ├── permissions.py
│   └── urls.py
└── requirements.txt
🚀 Getting Started
Prerequisites
Python 3.10+

pip

(Optional) AWS account for S3 and SNS features

Installation
Clone the repository

bash
git clone https://github.com/yourusername/student-management-system.git
cd student-management-system
Create and activate a virtual environment

bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies

bash
pip install -r requirements.txt
Apply migrations

bash
python manage.py makemigrations accounts students courses attendance marks api
python manage.py migrate
Create a superuser (optional)

bash
python manage.py createsuperuser
Note: Superusers created this way won't have a UserProfile. Either create one via the admin panel or use the signup form.

Configure AWS settings (if using S3/SNS)

Edit student_management/settings.py and add your AWS credentials and bucket/topic ARNs:

python
AWS_ACCESS_KEY_ID = "your-access-key"
AWS_SECRET_ACCESS_KEY = "your-secret-key"
AWS_STORAGE_BUCKET_NAME = "your-bucket-name"
AWS_S3_REGION_NAME = "ap-south-1"   # e.g., us-east-1
AWS_SNS_TOPIC_ARN = "arn:aws:sns:region:account-id:topic-name"
Run the development server

bash
python manage.py runserver
Access the application at http://127.0.0.1:8000/ – you'll be redirected to the login page.

☁️ AWS Integration Details
Attendance Export to S3
When a teacher clicks "Export Attendance to AWS S3", the app:

Fetches all attendance records.
Converts them into a plain text file with a timestamp.
Uploads the file to the configured S3 bucket.
Returns a direct download link to the file.
Bucket must be publicly readable (or use pre‑signed URLs – extend as needed).

Exam Notifications via SNS
On creating or updating an exam, the system:

Finds all students enrolled in that course.
Retrieves their email addresses.
Publishes a message to the SNS topic.
All subscribed email addresses receive the notification.
Important: Student email addresses must be subscribed and confirmed in the SNS topic. You can do this manually in the AWS Console or automate it during signup.

📱 Usage
Sign Up
Visit /accounts/signup/ and choose a role (Teacher or Student).

After signup, you can log in.

Login & Redirection
Unauthenticated users are redirected to /accounts/login/.

Upon successful login, users are sent to their role‑specific dashboard:

Teacher: /students/teacher/dashboard/

Student: /students/student/dashboard/

Teacher Dashboard
Manage Students: list, add, edit, delete, view details.

Manage Courses: create, update, delete.

Manage Enrollments: enroll students in courses.

Manage Attendance: mark attendance per course, edit/delete records, export to S3.

Manage Exams: schedule exams – automatic SNS notifications.

Manage Marks: record marks for each student/exam.

Student Dashboard
View personal profile (roll number, DOB, phone, address, photo).

View list of enrolled courses.

View attendance records (read‑only).

View marks obtained in exams.

REST API
Available at /api/ (requires authentication).

Endpoints: /api/students/, /api/courses/, /api/enrollments/, /api/attendance/, /api/exams/, /api/marks/.

Teachers have full read/write access; students have read‑only access to their own data.

Supports filtering, searching, ordering, and pagination.
