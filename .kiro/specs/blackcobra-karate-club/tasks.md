# Implementation Plan

- [x] 1. Set up project structure and base templates





  - [x] 1.1 Create base HTML template with TailwindCSS, HTMX, and AlpineJS CDN links


    - Create `templates/base.html` with responsive meta tags, CDN imports, and base layout structure
    - Include toast notification component and loading indicator styles
    - _Requirements: 15.1, 16.2, 16.3_

  - [x] 1.2 Create sidebar navigation component with mobile hamburger menu

    - Create `templates/components/sidebar.html` with AlpineJS toggle functionality
    - Implement responsive collapse behavior for mobile screens
    - _Requirements: 15.2, 15.3, 2.4, 8.3, 12.3_

  - [x] 1.3 Create reusable UI components (cards, tables, forms, modals)

    - Create `templates/components/` directory with card.html, table.html, form.html, modal.html
    - Ensure 44px minimum touch targets for mobile
    - _Requirements: 15.4, 15.5, 16.4_

  - [x] 1.4 Set up command shortcuts in pyproject.toml

    - Add uvmm, uvm, uvr script shortcuts
    - _Requirements: Introduction_
-

- [x] 2. Implement user authentication and role management





  - [x] 2.1 Create UserProfile model with role field

    - Extend Django User with OneToOne UserProfile containing role, phone, address, profile_image, date_of_birth
    - Create model in `core/models.py`
    - _Requirements: 1.1, 1.3_

  - [x] 2.2 Create role-based access decorators

    - Implement admin_required, trainee_required, judge_required decorators in `core/decorators.py`
    - _Requirements: 1.3, 1.4_
  - [ ]* 2.3 Write property test for role-based dashboard redirect
    - **Property 1: Role-based dashboard redirect**
    - **Validates: Requirements 1.1**
  - [ ]* 2.4 Write property test for protected route access control
    - **Property 3: Protected route access control**
    - **Validates: Requirements 1.4**
  - [x] 2.5 Create login/logout views and templates


    - Create `core/views/auth.py` with login_view, logout_view
    - Create `templates/auth/login.html` with modern styling
    - _Requirements: 1.1, 1.2, 1.5_
  - [x] 2.6 Implement role-based redirect after login


    - Redirect to /admin/dashboard/, /trainee/dashboard/, or /judge/dashboard/ based on role
    - _Requirements: 1.1_
  - [ ]* 2.7 Write property test for role-based navigation filtering
    - **Property 2: Role-based navigation filtering**
    - **Validates: Requirements 1.3**
- [x] 3. Implement Trainee and Judge models




- [ ] 3. Implement Trainee and Judge models


  - [x] 3.1 Create Trainee model with all fields

    - Implement belt_rank, weight, weight_class, emergency_contact, status, joined_date
    - Add weight class calculation method
    - _Requirements: 3.1, 3.3_
  - [x] 3.2 Create Judge model with certification fields


    - Implement certification_level, certification_date, is_active
    - _Requirements: 12.1_

  - [x] 3.3 Run migrations

    - Execute uvmm and uvm to create database tables
    - _Requirements: 2.1, 3.1_
-

- [x] 4. Implement Admin Dashboard




  - [x] 4.1 Create admin dashboard view with metrics


    - Display total trainee count, active events, pending payments, upcoming matches
    - Create `core/views/admin.py` with dashboard_view
    - _Requirements: 2.1_

  - [x] 4.2 Create admin dashboard template

    - Create `templates/admin/dashboard.html` with metric cards and activity feed
    - Implement clickable cards linking to management sections
    - _Requirements: 2.1, 2.2, 2.3_

  - [x] 4.3 Implement recent activity feed

    - Query latest registrations, payments, and match results
    - _Requirements: 2.2_

- [x] 5. Implement Trainee Management (Admin)





  - [x] 5.1 Create trainee list view with HTMX search


    - Implement searchable, sortable list with real-time filtering
    - Create `templates/admin/trainees/list.html`
    - _Requirements: 3.1, 3.6_
  - [ ]* 5.2 Write property test for search filter accuracy
    - **Property 13: Search filter accuracy**
    - **Validates: Requirements 3.6**

  - [x] 5.3 Create trainee add/edit forms
    - Implement form with all trainee fields
    - Create `templates/admin/trainees/form.html`
    - _Requirements: 3.2, 3.4_
  - [x] 5.4 Implement trainee CRUD operations
    - Create, read, update, delete views with HTMX partial updates
    - _Requirements: 3.3, 3.4, 3.5_
  - [ ]* 5.5 Write property test for trainee creation persistence
    - **Property 4: Trainee creation persistence**
    - **Validates: Requirements 3.3**
-

- [x] 6. Checkpoint - Ensure all tests pass




  - Ensure all tests pass, ask the user if questions arise.
-

- [x] 7. Implement Event model and management




  - [x] 7.1 Create Event and EventRegistration models


    - Implement Event with status, dates, location, max_participants
    - Implement EventRegistration linking trainees to events
    - _Requirements: 4.1, 4.4_

  - [x] 7.2 Create event list and detail views

    - Display events with participant count, status
    - Show registered participants, judges, matches on detail page
    - _Requirements: 4.1, 4.4_


  - [x] 7.3 Create event add/edit forms
    - Implement form with all event fields
    - _Requirements: 4.2, 4.3_
  - [ ]* 7.4 Write property test for event creation persistence
    - **Property 5: Event creation persistence**

    - **Validates: Requirements 4.3**
  - [x] 7.5 Implement event status update with HTMX

    - Update status without page reload
    - _Requirements: 4.5_
-

- [x] 8. Implement Match model and Matchmaking




  - [x] 8.1 Create Match, MatchJudge, and MatchResult models


    - Implement Match with competitors, scheduled_time, status
    - Implement MatchJudge for judge assignments
    - Implement MatchResult for recording outcomes
    - _Requirements: 5.1, 5.2_

  - [x] 8.2 Create matchmaking list view grouped by event

    - Display matches with competitor names, judges, status
    - _Requirements: 5.1_


  - [x] 8.3 Create manual match creation form
    - Select event, competitors, judges, scheduled time

    - _Requirements: 5.2_
  - [x] 8.4 Implement MatchmakingService with auto-matchmaking algorithm

    - Pair trainees by weight (≤5kg), belt rank (same/adjacent), age (≤3 years)
    - Return proposed matches for admin review
    - _Requirements: 5.3, 5.4_
  - [ ]* 8.5 Write property test for auto-matchmaking weight constraint
    - **Property 7: Auto-matchmaking weight constraint**
    - **Validates: Requirements 5.3**
  - [ ]* 8.6 Write property test for auto-matchmaking belt rank constraint
    - **Property 8: Auto-matchmaking belt rank constraint**
    - **Validates: Requirements 5.3**
  - [ ]* 8.7 Write property test for auto-matchmaking age constraint
    - **Property 9: Auto-matchmaking age constraint**
    - **Validates: Requirements 5.3**

  - [x] 8.8 Implement judge assignment with conflict validation

    - Validate judge is not competing in same event
    - _Requirements: 5.5, 5.6_
  - [ ]* 8.9 Write property test for judge conflict validation
    - **Property 10: Judge conflict validation**
    - **Validates: Requirements 5.5**

- [x] 9. Checkpoint - Ensure all tests pass





  - Ensure all tests pass, ask the user if questions arise.
-

- [x] 10. Implement Payment model and management


  - [x] 10.1 Create Payment model


    - Implement amount, payment_type, payment_method, status, payment_date
    - _Requirements: 6.1_


  - [x] 10.2 Create payment list view with status filtering
    - Display payments with trainee, amount, type, status
    - Implement HTMX filter by status
    - _Requirements: 6.1, 6.4_
  - [ ]* 10.3 Write property test for payment status filter accuracy
    - **Property 14: Payment status filter accuracy**

    - **Validates: Requirements 6.4**

  - [x] 10.4 Create payment recording form
    - Select trainee, enter amount, type, method
    - _Requirements: 6.2, 6.3_
  - [ ]* 10.5 Write property test for payment creation and history update
    - **Property 6: Payment creation and history update**

    - **Validates: Requirements 6.3**

  - [x] 10.6 Implement mark payment as completed

    - Update status and timestamp
    - _Requirements: 6.5_
-

- [x] 11. Implement Reports




  - [x] 11.1 Create ReportService with report generation methods


    - Implement membership_report, financial_report, event_report
    - _Requirements: 7.1, 7.2, 7.4_

  - [x] 11.2 Create reports view with type selection and date range

    - Display report options and generated data
    - _Requirements: 7.1, 7.2_

  - [x] 11.3 Implement PDF and CSV export

    - Use ReportLab for PDF generation

    - _Requirements: 7.3_

- [x] 12. Implement Trainee Dashboard and Features




  - [x] 12.1 Create trainee dashboard view


    - Display profile summary, upcoming events, scheduled matches
    - _Requirements: 8.1, 8.2_

  - [x] 12.2 Create trainee events view with registration

    - Display open events, register button, registration status
    - _Requirements: 9.1, 9.2, 9.3_

  - [x] 12.3 Implement registration deadline enforcement

    - Disable registration after deadline
    - _Requirements: 9.4_
  - [ ]* 12.4 Write property test for registration deadline enforcement
    - **Property 11: Registration deadline enforcement**
    - **Validates: Requirements 9.4**


  - [x] 12.5 Create trainee matches view
    - Display upcoming and past matches with details

    - _Requirements: 10.1, 10.2, 10.3_

  - [x] 12.6 Create trainee payment history view
    - Display payments with pending highlighted
    - _Requirements: 11.1, 11.2, 11.3_
  - [ ]* 12.7 Write property test for trainee-specific payment history
    - **Property 15: Trainee-specific payment history**
    - **Validates: Requirements 11.1**
-

- [x] 13. Checkpoint - Ensure all tests pass




  - Ensure all tests pass, ask the user if questions arise.



- [x] 14. Implement Judge Dashboard and Features








  - [x] 14.1 Create judge dashboard view



    - Display profile, certification, upcoming matches count
    - _Requirements: 12.1, 12.2_


  - [x] 14.2 Create judge events view
    - Display events where judge is assigned


    - _Requirements: 13.1_
  - [x] 14.3 Create judge matches view
    - Display assigned matches with competitor info
    - _Requirements: 13.2, 13.3_
  - [ ]* 14.4 Write property test for judge-specific match assignment


    - **Property 16: Judge-specific match assignment**
    - **Validates: Requirements 13.2**
  - [x] 14.5 Create judge results entry view
    - Display judged matches, result entry form
    - _Requirements: 14.1, 14.2, 14.3_


  - [x] 14.6 Implement result submission with immutability

    - Record result, prevent modifications without admin override
    - _Requirements: 14.3, 14.4_
  - [ ]* 14.7 Write property test for match result immutability
    - **Property 12: Match result immutability**
    - **Validates: Requirements 14.4**

- [-] 15. Implement HTMX partial views and interactions


  - [x] 15.1 Create partial templates for list updates


    - trainee_list_partial, event_list_partial, match_list_partial, payment_list_partial
    - _Requirements: 16.1_

  - [ ] 15.2 Implement toast notification system

    - Success and error notifications with AlpineJS
    - _Requirements: 16.3_
  - [ ] 15.3 Add loading indicators to all HTMX requests
    - Display spinner during processing
    - _Requirements: 16.2_
  - [ ] 15.4 Implement hover effects and visual feedback
    - Add hover states to interactive elements
    - _Requirements: 16.5_

- [x] 16. Configure URL routing



   - [x] 16.1 Set up all admin URLs
     - /admin/dashboard/, /admin/trainees/, /admin/events/, /admin/matchmaking/, /admin/payments/, /admin/reports/
     - _Requirements: 2.4_
   - [x] 16.2 Set up all trainee URLs
     - /trainee/dashboard/, /trainee/events/, /trainee/matches/, /trainee/payments/
     - _Requirements: 8.3_
   - [x] 16.3 Set up all judge URLs
     - /judge/dashboard/, /judge/events/, /judge/matches/, /judge/results/
     - _Requirements: 12.3_

- [x] 17. Final Checkpoint - Ensure all tests pass


   - All Django system checks pass. No custom tests defined yet (placeholder for future test suite).
