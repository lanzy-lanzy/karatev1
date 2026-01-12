# Unpaid Registration Approval Restriction

## Overview
Implemented a feature to prevent admin approval of registrations with unpaid payment status. This ensures that new members cannot be approved as trainees without payment confirmation.

## Changes Made

### 1. Backend Validation (core/views/admin_registrations.py)

#### `registration_detail()` - POST handler for detailed approval
- **Added validation check** (line 123-126):
  ```python
  if registration.payment_status == 'unpaid' and not request.POST.get('mark_payment'):
      messages.error(request, f'Cannot approve registration. Payment must be marked as paid first.')
      return redirect('admin_registration_detail', registration_id=registration.id)
  ```
- Returns error message if attempting to approve without marking payment as paid

#### `registration_approve()` - Quick approval endpoint  
- **Added validation check** (line 233-236):
  ```python
  if registration.payment_status == 'unpaid':
      messages.error(request, f'Cannot approve registration. Payment must be marked as paid first.')
      return redirect('admin_registration_detail', registration_id=registration.id)
  ```
- Prevents approval via quick-approve button if payment is unpaid

### 2. UI Updates

#### List View (templates/admin/registrations/list.html)
- **Conditional Approve Button** (lines 379-390):
  - Paid registrations: Display clickable "Approve" link
  - Unpaid registrations: Display disabled button with tooltip "Payment must be marked as paid first"
  - Visual indicator: Button appears grayed out (opacity: 0.5)

#### Detail View (templates/admin/registrations/detail.html)

**Warning Message** (lines 521-525):
- Shows orange warning box when payment is unpaid
- Message: "Registration cannot be approved until payment is marked as paid. Check the 'Mark as Payment Paid' checkbox below or process payment first."

**Checkbox Enhancement** (lines 530-535):
- Added `required` attribute to "Mark as Payment Paid" checkbox
- Added red asterisk (*) to indicate required field
- Helper text: "This must be checked to approve the registration"

**Approve Button** (lines 540-543):
- Initially disabled when payment is unpaid
- Button styling: opacity 0.5, cursor not-allowed
- Dynamic JavaScript enables/disables based on checkbox state

**Interactive JavaScript** (lines 322-350):
- Monitors checkbox state changes
- Enables approve button only when checkbox is checked
- Updates button opacity and cursor style accordingly
- Initial state validation on page load

## Behavior

### Unpaid Registration
1. Admin views pending registration with "Unpaid" payment status
2. Approve button appears disabled (grayed out) in both list and detail views
3. In detail view, warning message appears explaining payment requirement
4. Checkbox "Mark as Payment Paid" becomes required
5. Approve button only becomes enabled when checkbox is checked
6. Backend validates payment status before final approval
7. Error message shown if attempt to approve without payment confirmation

### Paid Registration
1. Approve button is fully functional (enabled)
2. No warning message
3. Checkbox not required
4. Registration can be approved normally

## Security & Validation
- **Two-layer validation**: Both frontend (UI) and backend (Python) checks
- **No bypass possible**: Even if checkbox is manually enabled via dev tools, backend validation prevents approval
- **Clear messaging**: Admin receives error message explaining why approval failed
- **Audit trail**: Message indicates payment requirement clearly

## Testing Scenarios

### Scenario 1: Quick Approve with Unpaid Status
- Navigate to registrations list
- Click "Approve" on unpaid registration
- Expected: Button disabled, cannot click through

### Scenario 2: Detailed Approval with Unpaid Status
- Click "View" on unpaid registration
- Expected: Warning message shows, approve button disabled, checkbox required
- Uncheck checkbox: Approve button disabled
- Check checkbox: Approve button enabled
- Click approve: Registration approved and marked as paid

### Scenario 3: Detailed Approval with Paid Status
- Click "View" on paid registration
- Expected: No warning message, approve button enabled, no checkbox
- Click approve: Registration approved normally

## Files Modified
- `core/views/admin_registrations.py` - Backend validation logic
- `templates/admin/registrations/list.html` - List view UI
- `templates/admin/registrations/detail.html` - Detail view UI with JavaScript

## Rollout Notes
- No database migrations required
- No API changes
- Existing approved unpaid registrations remain approved
- Feature affects only pending registrations
- Settings and payments remain unchanged
