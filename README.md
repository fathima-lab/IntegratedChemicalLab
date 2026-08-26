# ICLMS – Integrated Chemical Laboratory Management System

## Project Overview

ICLMS (Integrated Chemical Laboratory Management System) is a fully functional Django web application developed to manage laboratory resources, users, experiments, samples, chemicals, equipment, maintenance, reports, external services, equipment bookings, and payments through a centralized web-based system.

The application is designed with a modular Django architecture and includes user authentication, role-based access control, database integration, CRUD operations, responsive user interfaces, external user services, and proper project documentation.

---

## Project Requirements

| Requirement | ICLMS Implementation |
|---|---|
| User Authentication System | Registration, Login and Logout |
| Role-Based Access Control | Central Admin, Sub-admin, Researcher, Technician and External User |
| CRUD Operations | Chemicals, Equipment, Experiments, Samples, Reports and User Management |
| Database Integration | SQLite with Django ORM and migrations |
| Responsive UI | HTML5, CSS3, Bootstrap and responsive layouts |
| Proper Project Structure | Modular Django applications |
| Documentation | README and organized source code |
| Templates | Dedicated Django templates for all major modules |

---

# 1. User Authentication System

ICLMS provides a complete authentication system using Django authentication.

Users can:

- Register
- Login
- Logout
- Access authorized dashboards
- Access features according to their role
- Manage their account information

The application uses a custom Django user model.

## Internal User Registration

Internal users can register with:

- First Name
- Last Name
- Username
- Email
- Phone
- Institution / Company
- Location / Place
- Role
- Supervisor
- Password
- Confirm Password

Institution / Company and Location / Place are used for:

- Sub Administrator
- Researcher
- Technician

Researchers and Technicians can also be assigned a supervisor.

## External User Registration

External users can register independently with:

- First Name
- Last Name
- Username
- Email
- Phone
- User Type
- Institution / Company
- Location / Place
- Password
- Confirm Password

External user types include:

- Teacher
- Student
- Other

---

# 2. Role-Based Access Control

ICLMS provides role-based access control to ensure that users can access only the features appropriate to their roles.

## Internal Users

### Central Administrator

Responsible for overall system administration and user management.

### Sub Administrator

Responsible for managing laboratory activities and assigned laboratory users.

### Researcher

Can manage and access laboratory resources and experiments according to assigned permissions.

### Technician

Can manage laboratory equipment and maintenance-related activities.

## External Users

External users can register independently and access selected laboratory services.

External user categories include:

- Teacher
- Student
- Other

Different dashboards and permissions are provided according to the user's role.

---

# 3. CRUD Operations

ICLMS implements database-driven CRUD operations.

CRUD means:

- Create
- Read
- Update
- Delete

## Chemical Management

Users with appropriate permissions can:

- Create chemicals
- View chemicals
- Update chemicals
- Delete chemicals

## Equipment Management

Users can:

- Register equipment
- View equipment
- Update equipment
- Remove equipment
- Check equipment status
- Check equipment location

## Experiment Management

Users can:

- Create experiments
- View experiments
- Edit experiments
- Delete experiments
- Record experiment conclusions

## Sample Management

Users can:

- Create samples
- View samples
- Edit samples
- Delete samples

## Report Management

Users can:

- Create reports
- View reports
- Edit reports
- Delete reports

## User Management

Authorized administrators can:

- Create users
- View users
- Edit users
- Delete users

---

# 4. Database Integration

The application uses Django's ORM for database integration.

The development database is:

**SQLite**

The database stores information related to:

- Users
- User roles
- Institutions
- Locations
- Chemicals
- Equipment
- Equipment maintenance
- Experiments
- Samples
- Reports
- External users
- Equipment bookings
- Payment-related records

Django migrations are used to create and update database tables.

---

# 5. Responsive User Interface

The application provides a responsive user interface designed for different screen sizes.

Technologies used include:

- HTML5
- CSS3
- Bootstrap
- JavaScript
- Font Awesome / Bootstrap Icons where applicable

The interface includes:

- Responsive navigation
- Dashboard cards
- Responsive forms
- Responsive tables
- Responsive buttons
- Mobile-friendly layouts
- Consistent styling
- Responsive registration pages

---

# 6. Main Application Modules

## Accounts

Handles:

- User registration
- Login
- Logout
- Custom user model
- User roles
- User information
- Supervisor assignment

## Dashboard

Provides role-specific dashboards for:

- Central Administrator
- Sub Administrator
- Researcher
- Technician
- External User

## Chemicals

Provides laboratory chemical inventory management.

Features include:

- Chemical registration
- Chemical listing
- Chemical details
- Chemical updates
- Chemical deletion
- External chemical purchasing

## Equipment

Provides laboratory equipment management.

Features include:

- Equipment registration
- Equipment details
- Equipment status
- Equipment location
- Manufacturer information
- Equipment updates
- Equipment removal
- Equipment availability

## Maintenance

Provides equipment maintenance management.

Features include:

- Maintenance scheduling
- Maintenance records
- Maintenance dates
- Maintenance status
- Equipment maintenance tracking

## Experiments

Provides laboratory experiment management.

Features include:

- Experiment creation
- Experiment listing
- Experiment editing
- Experiment deletion
- Experiment conclusions

## Samples

Provides laboratory sample management.

Features include:

- Sample registration
- Sample listing
- Sample details
- Sample editing
- Sample deletion
- Sample tracking

## Reports

Provides laboratory report management.

Features include:

- Report creation
- Report listing
- Report editing
- Report deletion
- Report access

## External Users

External users can:

- Register
- Login
- View their dashboard
- Browse chemicals
- Purchase chemicals
- View available equipment
- Schedule equipment
- View equipment bookings
- Access laboratory reports
- Make payments for selected services

## Payment

The payment module provides payment-related functionality for external laboratory services.

External users may be required to complete payment before accessing selected paid services.

---

# 7. Equipment Management

Equipment information includes:

- Equipment Name
- Equipment ID
- Description
- Manufacturer
- Model Number
- Location
- Status
- Purchase Date
- Last Maintenance Date
- Next Maintenance Date

Equipment statuses include:

- Available
- In Use
- Under Maintenance
- Out of Service

---

# 8. Maintenance Management

The maintenance module allows laboratory equipment maintenance to be scheduled and monitored.

Features include:

- Schedule Maintenance
- View Maintenance Records
- Maintenance Dates
- Maintenance Status
- Equipment Maintenance Tracking

---

# 9. External Equipment Booking

External users can view available laboratory equipment and schedule equipment according to availability.

The booking functionality includes:

- Available equipment
- Equipment selection
- Booking date
- Booking records
- User-specific booking information

---

# 10. Payment Module

The payment module is designed to handle paid laboratory services for external users.

External users may be required to complete payment before accessing selected services such as:

- Chemical purchasing
- Equipment booking
- Laboratory reports

Payment-related pages include:

- Payment Checkout
- Payment Success

---

# 11. Django Templates

The project uses Django templates to provide the frontend interface.

All templates extend the common:

```text
templates/base.html

The project follows Django's modular application structure:
IntegratedChemicalLab/
│
├── accounts/
│   ├── migrations/
│   ├── forms.py
│   ├── models.py
│   ├── views.py
│   └── ...
│
├── chemicals/
│   ├── migrations/
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── ...
│
├── dashboard/
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── equipment/
│   ├── migrations/
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── experiments/
│   ├── migrations/
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── external/
│   ├── migrations/
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── payment/
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── reports/
│   ├── migrations/
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── samples/
│   ├── migrations/
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── iclms/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── static/
├── templates/
│
├── manage.py
├── db.sqlite3
└── .gitignore

Templates include:
templates/
│
├── base.html
│
├── home.html
├── about.html
├── features.html
├── contact.html
│
├── login.html
├── register.html
├── registration_choice.html
├── external_register.html
│
├── dashboard.html
├── sub_admin_dashboard.html
├── external_dashboard.html
│
├── create_sub_admin.html
├── edit_sub_admin.html
├── delete_sub_admin.html
│
├── create_team_member.html
├── edit_team_member.html
├── delete_team_member.html
│
├── chemicals.html
├── create_chemical.html
├── edit_chemicals.html
├── delete_chemicals.html
│
├── equipment.html
├── create_equipment.html
├── update_equipment.html
├── remove_equipment.html
│
├── maintenance.html
├── schedule_maintenance.html
│
├── experiments.html
├── create_experiment.html
├── edit_experiment.html
├── delete_experiment.html
│
├── samples.html
├── create_sample.html
├── edit_samples.html
├── delete_samples.html
│
├── reports.html
├── create_report.html
├── edit_report.html
├── delete_report.html
│
├── external_chemicals.html
├── external_equipment.html
├── external_equipment_booking.html
├── external_reports.html
├── external_laboratory_reports.html
├── external_booking_reports.html
│
├── payment_checkout.html
└── payment_success.html
