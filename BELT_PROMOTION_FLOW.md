# Belt Promotion - Flow Diagrams & Architecture

## User Interaction Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    ADMIN USER JOURNEY                           │
└─────────────────────────────────────────────────────────────────┘

                          Admin Login
                             │
                             ▼
              Admin Dashboard (Authenticated)
                             │
            ┌────────────────┴────────────────┐
            │                                 │
            ▼                                 ▼
     Sidebar Navigation              Navigation Bar
            │                             │
            ▼                             │
    Click "Belt Promotion" ◄─────────────┘
            │
            ▼
    ┌──────────────────────────────┐
    │  BELT PROMOTION LIST PAGE    │
    │  ─────────────────────────   │
    │  • Search bar                │
    │  • Filter dropdowns          │
    │  • Trainee table             │
    │  • Promote buttons           │
    └──────────────────────────────┘
            │
            ├─ Search/Filter (HTMX)
            │       └─► Table updates live
            │
            └─ Click "Promote" button
                     │
                     ▼
         ┌───────────────────────────────────┐
         │  PROMOTION FORM PAGE              │
         │  ───────────────────────────────  │
         │  • Trainee info card              │
         │  • Current rank & points          │
         │  • New belt rank selector         │
         │  • Admin notes textarea           │
         │  • Promotion history display      │
         │  • Promote/Cancel buttons         │
         └───────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
      Cancel            Select New Rank
         │               Add Notes
         │               Click Promote
         │                    │
         ▼                    ▼
    Redirect to        Validation
    List Page          (Server-side)
                            │
                  ┌─────────┴─────────┐
                  │                   │
                Invalid          Valid
                  │                   │
                  ▼                   ▼
            Error Message    Update Database
            Redisplay Form     │
                           ├─ Update Trainee.belt_rank
                           ├─ Create BeltRankProgress
                           ├─ Create Notification
                           │
                           ▼
                      Success Message
                      Redirect to List
                            │
                            ▼
                   Trainee Notified (In-App)
                   History Updated
```

## Database Schema (New/Modified)

```
┌─────────────────────────────────────────────────────────────┐
│                   BeltRankProgress                          │
│  ─────────────────────────────────────────────────────────  │
│  • id (Primary Key)                                         │
│  • trainee_id (Foreign Key → Trainee)                       │
│  • old_belt_rank (CharField)                                │
│  • new_belt_rank (CharField)                                │
│  • points_earned (Integer)                                  │
│  ┌─ NEW FIELDS ─────────────────────────────────┐          │
│  │ • promotion_type ('automatic' | 'override')  │          │
│  │ • admin_notes (TextField)                    │          │
│  │ • promoted_by (Foreign Key → User)           │          │
│  └─────────────────────────────────────────────┘          │
│  • promoted_at (DateTime)                                   │
│                                                             │
│  Indexes: [trainee_id], [promoted_at]                      │
│  Ordering: -promoted_at                                    │
└─────────────────────────────────────────────────────────────┘

Relationships:
  BeltRankProgress.trainee ──┐
                             ├─→ Trainee (1:N)
                                   │
                                   ├─→ Trainee.points (TraineePoints)
                                   │
                                   └─→ Trainee.profile (UserProfile)
                                           │
                                           └─→ User

  BeltRankProgress.promoted_by ──→ User (admin who made change)
```

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     WEB BROWSER                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  HTML/CSS/JavaScript (Tailwind, AlpineJS, HTMX) │  │
│  └──────────────┬───────────────────────────────────┘  │
└─────────────────┼──────────────────────────────────────┘
                  │ HTTP Requests
                  ▼
┌─────────────────────────────────────────────────────────┐
│               DJANGO WEB SERVER                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  URLs (core/urls.py)                            │  │
│  │  └─→ Routes to appropriate views                │  │
│  └──────────────┬───────────────────────────────────┘  │
│                 │                                       │
│  ┌──────────────▼───────────────────────────────────┐  │
│  │  Views (core/views/admin.py)                    │  │
│  │  ┌─ belt_rank_promotion_list                   │  │
│  │  ├─ belt_rank_promotion_list_partial (HTMX)   │  │
│  │  ├─ belt_rank_promote                         │  │
│  │  └─ belt_rank_promotion_history                │  │
│  └──────────────┬───────────────────────────────────┘  │
│                 │                                       │
│  ┌──────────────▼───────────────────────────────────┐  │
│  │  Models (core/models.py)                        │  │
│  │  • Trainee                                      │  │
│  │  • BeltRankProgress (enhanced)                  │  │
│  │  • User                                         │  │
│  │  • Notification                                 │  │
│  └──────────────┬───────────────────────────────────┘  │
│                 │                                       │
│  ┌──────────────▼───────────────────────────────────┐  │
│  │  Decorators (core/decorators.py)                │  │
│  │  @admin_required - Authorization check          │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────┬──────────────────────────────────────┘
                  │ Django ORM
                  ▼
┌─────────────────────────────────────────────────────────┐
│                   DATABASE                             │
│  • BeltRankProgress (promotion records)                │
│  • Trainee (belt_rank field)                           │
│  • Notification (trainee notifications)               │
│  • auth_user (admin tracking)                          │
└─────────────────────────────────────────────────────────┘

                  Templates
                      │
    ┌─────────────────┼─────────────────┐
    │                 │                 │
    ▼                 ▼                 ▼
list.html    promote_form.html    history.html
    │                 │                 │
    ├─► list_partial.html
    │
    └─► Rendered & sent to browser
```

## Data Flow - Promotion Operation

```
          INPUT PHASE
          ────────────
             │
             ▼
    User clicks "Promote" button
             │
             ├─ belt_rank_promote(GET)
             │      │
             │      ├─ Check @admin_required ✓
             │      │
             │      ├─ Load trainee data
             │      │
             │      ├─ Get belt choices
             │      │
             │      └─ Render form.html
             │             │
             └─────────────┤ Display to user


         PROCESSING PHASE
         ─────────────────
             │
             ▼
    User fills form & submits
             │
             ├─ belt_rank_promote(POST)
             │      │
             │      ├─ Check @admin_required ✓
             │      │
             │      ├─ VALIDATION
             │      │  ├─ Check belt_rank is valid
             │      │  └─ Check belt_rank ≠ current rank
             │      │
             │      ├─ Get current belt rank
             │      │      │
             │      │      └─ trainee.belt_rank
             │      │
             │      ├─ Try to get trainee.points
             │      │      │
             │      │      ├─ If exists: points.total_points
             │      │      └─ If not: 0
             │      │
             │      └─ PROCESSING
                            │
                            ├─ Save trainee
                            │  └─ trainee.belt_rank = new_rank
                            │     trainee.save()
                            │
                            ├─ Create BeltRankProgress record
                            │  ├─ trainee_id
                            │  ├─ old_belt_rank
                            │  ├─ new_belt_rank
                            │  ├─ points_earned
                            │  ├─ promotion_type='admin_override'
                            │  ├─ admin_notes
                            │  ├─ promoted_by=request.user
                            │  └─ save()
                            │
                            ├─ Create Notification
                            │  ├─ type='belt_promotion'
                            │  ├─ title with new belt
                            │  ├─ message
                            │  ├─ recipient=trainee.user
                            │  └─ save()
                            │
                            └─ Success message


         OUTPUT PHASE
         ─────────────
             │
             ▼
    Return success response
             │
             ├─ If HTMX: HX-Redirect header
             │
             └─ Otherwise: HTTP redirect
                    │
                    ▼
             Redirect to admin_belt_promotion
                    │
                    ▼
             Show updated list with success banner


         NOTIFICATION PHASE
         ────────────────────
             │
             ▼
    Trainee logs in or refreshes
             │
             ├─ notification_list view loads
             │      │
             │      └─ Displays new notification
             │             │
             │             ├─ Title: "Belt Promotion to [Belt]"
             │             ├─ Message: Congratulations...
             │             └─ Date: current timestamp
             │
             └─ Trainee sees notification
                    │
                    └─ Can mark as read
```

## Request/Response Cycle

```
REQUEST: GET /admin/belt-promotion/
  Headers:
    User-Agent: Mozilla/5.0...
    Cookie: sessionid=...
    
DJANGO PROCESSING:
  1. URL matching → belt_rank_promotion_list
  2. @admin_required decorator check
  3. Retrieve query parameters
  4. Query database
  5. Render template
  
RESPONSE: 200 OK
  Content-Type: text/html
  Body: HTML list page


REQUEST: GET /admin/belt-promotion/partial/
              ?search=john&belt_filter=yellow
  Headers:
    HX-Request: true
    
DJANGO PROCESSING:
  1. URL matching → belt_rank_promotion_list_partial
  2. Apply filters
  3. Render partial template (table only)
  
RESPONSE: 200 OK
  Body: HTML table rows


REQUEST: POST /admin/belt-promotion/<id>/promote/
  Body:
    new_belt_rank=blue
    admin_notes=Good performance
    csrfmiddlewaretoken=...
    
DJANGO PROCESSING:
  1. Validation
  2. Database updates
  3. Notification creation
  4. Redirect header
  
RESPONSE: 200 OK
  Header: HX-Redirect: /admin/belt-promotion/
```

## Error Handling Flow

```
User submits form
      │
      ▼
Server receives POST request
      │
      ├─ Check authentication
      │     │
      │     ├─ NOT authenticated
      │     │     └─ Redirect to login
      │     │
      │     └─ Authenticated ✓
      │
      ├─ Check admin permission
      │     │
      │     ├─ NOT admin
      │     │     └─ Redirect to home
      │     │
      │     └─ Admin ✓
      │
      ├─ Validate belt_rank
      │     │
      │     ├─ Invalid belt
      │     │     └─ Render form with error
      │     │
      │     └─ Valid belt ✓
      │
      ├─ Validate belt differs
      │     │
      │     ├─ Same as current
      │     │     └─ Render form with error
      │     │
      │     └─ Different ✓
      │
      ├─ Update database
      │     │
      │     ├─ Database error
      │     │     └─ Render form with error
      │     │
      │     └─ Success ✓
      │
      └─ Return success response
```

## Component Interaction

```
┌─────────────────────────────────────────────────────────────┐
│                  BELT PROMOTION LIST PAGE                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌────────────────┐   ┌──────────────┐   ┌────────────┐   │
│  │  Search Input  │   │   Belt Filter │   │  Status    │   │
│  │                │───→ HTMX Request  │───→  Filter    │   │
│  │ onkeyup event  │   │   (300ms deb) │   │  Dropdown  │   │
│  └────────────────┘   └──────────────┘   └────────────┘   │
│          │                    │                 │            │
│          └────────────────────┴─────────────────┘            │
│                               │                              │
│                               ▼                              │
│                    Django Query Processing                   │
│                  (Trainee.objects.filter...)                │
│                               │                              │
│                               ▼                              │
│              ┌────────────────────────────────┐             │
│              │   Database Query Results       │             │
│              │  (Filtered Trainee List)       │             │
│              └────────────────────────────────┘             │
│                               │                              │
│                               ▼                              │
│              ┌────────────────────────────────┐             │
│              │   Render list_partial.html     │             │
│              │  (Table rows with data)        │             │
│              └────────────────────────────────┘             │
│                               │                              │
│                               ▼                              │
│        ┌─────────────────────────────────────┐              │
│        │    Trainee Table Rows               │              │
│        │  ┌──────────────┐ ┌─────────────┐  │              │
│        │  │ Name | Belt  │ │ Points |    │  │              │
│        │  │──────────────│ │ Status | ⚡ │  │              │
│        │  │ John | Green │ │ 150   | Promote             │
│        │  │ Jane | Yellow│ │ 200   | Promote             │
│        │  └──────────────┘ └─────────────┘  │              │
│        └─────────────────────────────────────┘              │
│                        │                                    │
│                        ▼                                    │
│                   Click "Promote"                          │
│                   Navigate to form                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Legend

```
─────  Process flow
│      Connection
▼      Next step
→      Goes to
├─     Condition/option
└─     End/alternative
✓      Success/valid
⚡     Action button
```

---

**Visual Architecture Complete**
All major flows, interactions, and data transformations documented.
