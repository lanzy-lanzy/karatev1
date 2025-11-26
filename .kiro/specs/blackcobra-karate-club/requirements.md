# Requirements Document

## Introduction

The BlackCobra Karate Club System is a comprehensive web application for managing karate club operations. The system provides role-based dashboards for administrators, trainees, and judges. It handles trainee management, event scheduling, matchmaking (including auto-matchmaking), payment tracking, and reporting. The frontend uses TailwindCSS CDN, HTMX CDN, and AlpineJS CDN for a modern, interactive, mobile-responsive experience built on Django framework.

## Glossary

- **System**: The BlackCobra Karate Club web application
- **Admin**: Club administrator with full system access
- **Trainee**: Registered karate student/member
- **Judge**: Certified official who scores matches
- **Event**: A karate competition or tournament
- **Match**: A competitive bout between two trainees
- **Matchmaking**: The process of pairing trainees for competition
- **Auto-Matchmaking**: Automated pairing based on weight class, belt rank, and age
- **Payment**: Financial transaction for membership, events, or fees
- **Sidebar Nav**: Collapsible navigation menu on the left side of the interface

## Requirements

### Requirement 1: User Authentication and Role Management

**User Story:** As a system user, I want to log in with my credentials and access features based on my role, so that I can perform my designated tasks securely.

#### Acceptance Criteria

1. WHEN a user submits valid credentials THEN the System SHALL authenticate the user and redirect to their role-specific dashboard
2. WHEN a user submits invalid credentials THEN the System SHALL display an error message and remain on the login page
3. WHILE a user is authenticated THEN the System SHALL display only navigation items appropriate to their role (Admin, Trainee, or Judge)
4. WHEN an unauthenticated user attempts to access a protected page THEN the System SHALL redirect to the login page
5. WHEN a user clicks logout THEN the System SHALL terminate the session and redirect to the login page

### Requirement 2: Admin Dashboard

**User Story:** As an admin, I want to view a dashboard with key metrics and quick actions, so that I can monitor club operations at a glance.

#### Acceptance Criteria

1. WHEN an admin accesses the dashboard THEN the System SHALL display total trainee count, active events count, pending payments count, and upcoming matches count
2. WHEN an admin views the dashboard THEN the System SHALL display recent activity feed showing latest registrations, payments, and match results
3. WHEN an admin clicks a metric card THEN the System SHALL navigate to the corresponding management section
4. WHILE on the admin dashboard THEN the System SHALL display the sidebar navigation with links to Dashboard, Trainee Management, Event Management, Matchmaking Management, Payments, and Reports

### Requirement 3: Trainee Management

**User Story:** As an admin, I want to manage trainee records, so that I can maintain accurate membership information.

#### Acceptance Criteria

1. WHEN an admin accesses trainee management THEN the System SHALL display a searchable, sortable list of all trainees with name, belt rank, age, weight class, and status
2. WHEN an admin clicks "Add Trainee" THEN the System SHALL display a form to enter trainee details including name, date of birth, contact info, belt rank, weight, and emergency contact
3. WHEN an admin submits a valid trainee form THEN the System SHALL create the trainee record and display a success notification
4. WHEN an admin clicks edit on a trainee THEN the System SHALL display a pre-filled form for updating trainee information
5. WHEN an admin clicks delete on a trainee THEN the System SHALL prompt for confirmation before removing the record
6. WHEN an admin searches trainees THEN the System SHALL filter results in real-time without page reload using HTMX

### Requirement 4: Event Management

**User Story:** As an admin, I want to create and manage karate events, so that I can organize competitions and tournaments.

#### Acceptance Criteria

1. WHEN an admin accesses event management THEN the System SHALL display a list of all events with name, date, location, status, and participant count
2. WHEN an admin clicks "Create Event" THEN the System SHALL display a form with fields for event name, date, location, description, registration deadline, and maximum participants
3. WHEN an admin submits a valid event form THEN the System SHALL create the event and display a success notification
4. WHEN an admin views event details THEN the System SHALL display registered participants, assigned judges, and scheduled matches
5. WHEN an admin updates event status THEN the System SHALL reflect the change immediately using HTMX partial updates

### Requirement 5: Matchmaking Management

**User Story:** As an admin, I want to create matches between trainees and assign judges, so that I can organize fair competitions.

#### Acceptance Criteria

1. WHEN an admin accesses matchmaking management THEN the System SHALL display all matches grouped by event with competitor names, judge assignments, and match status
2. WHEN an admin clicks "Create Match" THEN the System SHALL display a form to select event, two competitors, scheduled time, and assign judges
3. WHEN an admin clicks "Auto-Matchmaking" for an event THEN the System SHALL automatically pair registered trainees based on weight class (within 5kg), belt rank (same or adjacent), and age group (within 3 years)
4. WHEN auto-matchmaking completes THEN the System SHALL display proposed matches for admin review before confirmation
5. WHEN an admin assigns judges to a match THEN the System SHALL validate that the judge is not a competitor in the same event
6. WHEN an admin confirms match assignments THEN the System SHALL notify assigned judges and competitors via the system

### Requirement 6: Payment Management

**User Story:** As an admin, I want to track and manage payments, so that I can maintain financial records for the club.

#### Acceptance Criteria

1. WHEN an admin accesses payments THEN the System SHALL display a list of all payments with trainee name, amount, type, date, and status
2. WHEN an admin clicks "Record Payment" THEN the System SHALL display a form to select trainee, enter amount, payment type (membership, event fee, equipment), and payment method
3. WHEN an admin submits a payment record THEN the System SHALL create the payment entry and update the trainee's payment history
4. WHEN an admin filters payments by status THEN the System SHALL display only matching records (pending, completed, overdue)
5. WHEN an admin marks a payment as completed THEN the System SHALL update the status and timestamp immediately

### Requirement 7: Reports

**User Story:** As an admin, I want to generate reports, so that I can analyze club performance and make informed decisions.

#### Acceptance Criteria

1. WHEN an admin accesses reports THEN the System SHALL display report type options including membership statistics, financial summary, event participation, and match results
2. WHEN an admin selects a report type and date range THEN the System SHALL generate and display the report with relevant charts and data tables
3. WHEN an admin clicks "Export" THEN the System SHALL download the report in the selected format (PDF or CSV)
4. WHEN viewing financial reports THEN the System SHALL display total revenue, payment breakdown by type, and outstanding balances

### Requirement 8: Trainee Dashboard

**User Story:** As a trainee, I want to view my dashboard with personal information and upcoming activities, so that I can stay informed about my training and competitions.

#### Acceptance Criteria

1. WHEN a trainee accesses their dashboard THEN the System SHALL display their profile summary including name, belt rank, and membership status
2. WHEN a trainee views the dashboard THEN the System SHALL display upcoming events they are registered for and scheduled matches
3. WHILE on the trainee dashboard THEN the System SHALL display the sidebar navigation with links to Dashboard, Upcoming Events, Schedule Match, and Payments History

### Requirement 9: Trainee Event View

**User Story:** As a trainee, I want to view and register for upcoming events, so that I can participate in competitions.

#### Acceptance Criteria

1. WHEN a trainee accesses upcoming events THEN the System SHALL display a list of open events with name, date, location, and registration status
2. WHEN a trainee clicks "Register" for an event THEN the System SHALL add them to the event participant list and display confirmation
3. WHEN a trainee is already registered for an event THEN the System SHALL display "Registered" status instead of register button
4. WHEN registration deadline has passed THEN the System SHALL disable the register button and display "Registration Closed"

### Requirement 10: Trainee Match Schedule

**User Story:** As a trainee, I want to view my scheduled matches, so that I can prepare for competitions.

#### Acceptance Criteria

1. WHEN a trainee accesses schedule match THEN the System SHALL display all their upcoming and past matches with opponent name, event, date, time, and result
2. WHEN a trainee views match details THEN the System SHALL display assigned judges and match location
3. WHEN a match result is recorded THEN the System SHALL update the trainee's match history immediately

### Requirement 11: Trainee Payment History

**User Story:** As a trainee, I want to view my payment history, so that I can track my financial obligations to the club.

#### Acceptance Criteria

1. WHEN a trainee accesses payments history THEN the System SHALL display all their payments with date, amount, type, and status
2. WHEN a trainee has pending payments THEN the System SHALL highlight them prominently at the top of the list
3. WHEN a trainee views payment details THEN the System SHALL display payment method and receipt information

### Requirement 12: Judge Dashboard

**User Story:** As a judge, I want to view my dashboard with assigned duties, so that I can prepare for officiating matches.

#### Acceptance Criteria

1. WHEN a judge accesses their dashboard THEN the System SHALL display their profile and certification information
2. WHEN a judge views the dashboard THEN the System SHALL display count of upcoming assigned matches and recent judging history
3. WHILE on the judge dashboard THEN the System SHALL display the sidebar navigation with links to Dashboard, Upcoming Events, Schedule Match, and Results

### Requirement 13: Judge Event and Match View

**User Story:** As a judge, I want to view events and my assigned matches, so that I can fulfill my officiating duties.

#### Acceptance Criteria

1. WHEN a judge accesses upcoming events THEN the System SHALL display events where they are assigned as judge
2. WHEN a judge accesses schedule match THEN the System SHALL display all matches assigned to them with competitor names, event, date, and time
3. WHEN a judge views match details THEN the System SHALL display competitor information and match rules

### Requirement 14: Judge Results Entry

**User Story:** As a judge, I want to record match results, so that competition outcomes are officially documented.

#### Acceptance Criteria

1. WHEN a judge accesses results THEN the System SHALL display matches they have judged with result entry status
2. WHEN a judge clicks "Enter Result" for a match THEN the System SHALL display a form to select winner, enter scores, and add notes
3. WHEN a judge submits match results THEN the System SHALL record the result and update both competitors' match history
4. WHEN results are submitted THEN the System SHALL prevent further modifications without admin override

### Requirement 15: Mobile Responsive Design

**User Story:** As a user, I want to access the system on mobile devices, so that I can use the application anywhere.

#### Acceptance Criteria

1. WHEN a user accesses the system on a mobile device THEN the System SHALL display a responsive layout that adapts to screen size
2. WHEN viewing on mobile THEN the System SHALL collapse the sidebar navigation into a hamburger menu
3. WHEN a user taps the hamburger menu THEN the System SHALL display the sidebar as an overlay with smooth animation
4. WHEN viewing data tables on mobile THEN the System SHALL display a card-based layout instead of traditional tables
5. WHEN interacting with forms on mobile THEN the System SHALL display appropriately sized touch targets (minimum 44px)

### Requirement 16: Interactive UI with Real-time Updates

**User Story:** As a user, I want interactive elements and real-time updates, so that I have a modern, seamless experience.

#### Acceptance Criteria

1. WHEN data changes occur THEN the System SHALL update the relevant page sections without full page reload using HTMX
2. WHEN a user performs an action THEN the System SHALL display loading indicators during processing
3. WHEN an action completes THEN the System SHALL display toast notifications for success or error feedback
4. WHEN a user interacts with dropdowns or modals THEN the System SHALL animate transitions smoothly using AlpineJS
5. WHEN hovering over interactive elements THEN the System SHALL display visual feedback indicating clickability
