# Software Testing Documentation (STD) – CLINK

This document contains the system test cases for the CLINK – Smart Outpatient Triage and Scheduling System.

## 1. Coverage Summary

| Module | Related Use Case / Requirement | Test Case IDs | Source: Docs / Code / Both |
|---|---|---|---|
| Patient Account Management | UC001, NFR-002 to NFR-005 | TC001_01 to TC001_06 | Both |
| Symptom Submission and AI Triage | UC002, UC003, UC004, UC005 | TC002_01 to TC002_02, TC003_01 to TC003_06 | Both |
| Triage Result Display | UC006 | TC006_01 to TC006_04 | Both |
| Appointment Scheduling | UC007 | TC007_01 to TC007_06 | Both |
| Notifications and Workflow | UC008 | TC008_01 to TC008_04 | Both |
| Doctor Module | UC009, UC010, UC010b | TC009_01 to TC009_02, TC010_01 to TC010_03 | Both |
| Admin Module | UC011, UC012 | TC011_01 to TC011_03, TC012_01 to TC012_03 | Both |
| Role-Based Access Control | NFR-015, NFR-019 | TC019_01 to TC019_03 | Both |

## 2. Test Cases

### 2.1 Test Cases for Module: Patient Account Management

#### 2.1.1 TC001_01: Register with valid inputs

Test Case ID:
TC001_01

Test Case Description:
Verify that a patient can successfully register a new account using valid inputs that meet all format requirements.

Created by:
Shams Ahmed

Version:
1.0

Prerequisites:
| No. | Prerequisites |
|---|---|
| 1 | System is operational and database is accessible. |
| 2 | User is not currently logged in. |

Test Data:
| No. | Test Data |
|---|---|
| 1 | Name: John Doe |
| 2 | Email: johndoe@example.com |
| 3 | Phone: 1234567890 |
| 4 | Password: Password!1 |

Test Conditions:
The user provides valid data for all required fields on the registration page.

Steps:
| Step # | Step Details | Expected Result |
|---|---|---|
| 1 | Navigate to the Registration page. | Registration form is displayed. |
| 2 | Enter valid Name, Email, Phone, and Password. | Fields accept the inputs. |
| 3 | Click the "Register" button. | System validates inputs, creates account, logs the user in, and redirects to Dashboard with success message. |

#### 2.1.2 TC001_02: Register with invalid email format

Test Case ID:
TC001_02

Test Case Description:
Verify that the system rejects registration if the email format is invalid.

Created by:
Shams Ahmed

Version:
1.0

Prerequisites:
| No. | Prerequisites |
|---|---|
| 1 | System is operational. |

Test Data:
| No. | Test Data |
|---|---|
| 1 | Email: invalid-email-format |

Test Conditions:
The user provides an invalid email address during registration.

Steps:
| Step # | Step Details | Expected Result |
|---|---|---|
| 1 | Navigate to Registration page and fill in all fields. | Fields accept input. |
| 2 | Provide invalid email format. | Input is entered. |
| 3 | Click "Register". | System rejects registration and displays "Please enter a valid email address." |

#### 2.1.3 TC001_03: Register with duplicate email

Test Case ID:
TC001_03

Test Case Description:
Verify that the system rejects registration if the email is already in use by another user.

Created by:
Shams Ahmed

Version:
1.0

Prerequisites:
| No. | Prerequisites |
|---|---|
| 1 | System is operational. |
| 2 | An account with email 'existing@example.com' exists in the database. |

Test Data:
| No. | Test Data |
|---|---|
| 1 | Email: existing@example.com |

Test Conditions:
The user attempts to register using an already registered email address.

Steps:
| Step # | Step Details | Expected Result |
|---|---|---|
| 1 | Navigate to Registration page. | Form is displayed. |
| 2 | Enter existing email and valid other details. | Fields accept input. |
| 3 | Click "Register". | System rejects registration and displays "An account with this email already exists." |

#### 2.1.4 TC001_04: Login with valid credentials

Test Case ID:
TC001_04

Test Case Description:
Verify that a patient can log in successfully with valid credentials.

Created by:
Shams Ahmed

Version:
1.0

Prerequisites:
| No. | Prerequisites |
|---|---|
| 1 | Patient account is registered and active. |

Test Data:
| No. | Test Data |
|---|---|
| 1 | Valid Email and Password |

Test Conditions:
The user provides matching email and password on the login page.

Steps:
| Step # | Step Details | Expected Result |
|---|---|---|
| 1 | Navigate to Login page. | Login form is displayed. |
| 2 | Enter valid Email and Password. | Fields accept input. |
| 3 | Click "Login". | System authenticates the user, creates a session, and redirects to Dashboard. |

#### 2.1.5 TC001_05: Login with invalid credentials

Test Case ID:
TC001_05

Test Case Description:
Verify that the system rejects login attempts with incorrect credentials.

Created by:
Shams Ahmed

Version:
1.0

Prerequisites:
| No. | Prerequisites |
|---|---|
| 1 | System is operational. |

Test Data:
| No. | Test Data |
|---|---|
| 1 | Invalid Email or Password |

Test Conditions:
The user provides an incorrect email or password.

Steps:
| Step # | Step Details | Expected Result |
|---|---|---|
| 1 | Navigate to Login page. | Login form is displayed. |
| 2 | Enter invalid Email and/or Password. | Fields accept input. |
| 3 | Click "Login". | System rejects login and displays "Invalid email or password." |

#### 2.1.6 TC001_06: Logout successfully

Test Case ID:
TC001_06

Test Case Description:
Verify that an authenticated user can log out successfully.

Created by:
Shams Ahmed

Version:
1.0

Prerequisites:
| No. | Prerequisites |
|---|---|
| 1 | User is logged into the system. |

Test Data:
| No. | Test Data |
|---|---|
| 1 | None |

Test Conditions:
The user triggers the logout action from the navigation menu.

Steps:
| Step # | Step Details | Expected Result |
|---|---|---|
| 1 | Click "Logout" from the navigation menu. | System destroys the session and redirects the user to the Login page. |

### 2.2 Test Cases for Module: Symptom Submission and AI Triage

#### 2.2.1 TC002_01: Submit valid symptoms successfully

Test Case ID:
TC002_01

Test Case Description:
Verify that a patient can submit valid symptoms for analysis.

Created by:
Shams Ahmed

Version:
1.0

Prerequisites:
| No. | Prerequisites |
|---|---|
| 1 | Patient is logged in. |

Test Data:
| No. | Test Data |
|---|---|
| 1 | Symptoms: "itching", "skin rash" |

Test Conditions:
The patient selects valid symptoms from the available list and submits them.

Steps:
| Step # | Step Details | Expected Result |
|---|---|---|
| 1 | Navigate to Submit Symptoms page. | Symptom selection form is displayed. |
| 2 | Select symptoms and provide optional details. | Selections are recorded. |
| 3 | Click "Submit". | System saves symptom record with 'pending' status and forwards to AI service. |

#### 2.2.2 TC002_02: Submit without selecting any symptom

Test Case ID:
TC002_02

Test Case Description:
Verify that the system prevents submission if no symptoms are selected.

Created by:
Shams Ahmed

Version:
1.0

Prerequisites:
| No. | Prerequisites |
|---|---|
| 1 | Patient is logged in. |

Test Data:
| No. | Test Data |
|---|---|
| 1 | Empty symptom list |

Test Conditions:
The patient attempts to submit the symptom form without selecting any items.

Steps:
| Step # | Step Details | Expected Result |
|---|---|---|
| 1 | Navigate to Submit Symptoms page. | Symptom form is displayed. |
| 2 | Leave symptoms selection empty. | No symptoms selected. |
| 3 | Click "Submit". | System rejects submission and displays "Please select at least one symptom." |

#### 2.2.3 TC003_01: AI analysis returns urgent classification

Test Case ID:
TC003_01

Test Case Description:
Verify that AI Triage service classifies symptoms with high severity (>= 6) as urgent.

Created by:
Shams Ahmed

Version:
1.0

Prerequisites:
| No. | Prerequisites |
|---|---|
| 1 | Patient submits symptoms containing high severity items (e.g., chest pain). |

Test Data:
| No. | Test Data |
|---|---|
| 1 | Symptoms list triggering severity >= 6 |

Test Conditions:
The AI evaluates the severity weights and calculates a max severity of 6 or higher.

Steps:
| Step # | Step Details | Expected Result |
|---|---|---|
| 1 | System sends symptoms to AI Triage Service. | AI processes the input. |
| 2 | Wait for AI response. | AI returns urgency classification as "urgent". |
| 3 | System updates the symptom record. | Record is saved with `urgencyLevel='urgent'`. |

#### 2.2.4 TC003_02: AI analysis returns non-urgent classification

Test Case ID:
TC003_02

Test Case Description:
Verify that AI Triage service classifies symptoms with low severity (< 6) as non-urgent.

Created by:
Shams Ahmed

Version:
1.0

Prerequisites:
| No. | Prerequisites |
|---|---|
| 1 | Patient submits symptoms containing only low severity items (e.g., itching). |

Test Data:
| No. | Test Data |
|---|---|
| 1 | Symptoms list triggering severity < 6 |

Test Conditions:
The AI evaluates the severity weights and calculates a max severity less than 6.

Steps:
| Step # | Step Details | Expected Result |
|---|---|---|
| 1 | System sends symptoms to AI Triage Service. | AI processes the input. |
| 2 | Wait for AI response. | AI returns urgency classification as "non-urgent". |
| 3 | System updates the symptom record. | Record is saved with `urgencyLevel='non-urgent'`. |

#### 2.2.5 TC003_03: AI correctly maps to specialist based on symptom

Test Case ID:
TC003_03

Test Case Description:
Verify that the AI Triage service recommends the correct specialist based on the predicted condition.

Created by:
Shams Ahmed

Version:
1.0

Prerequisites:
| No. | Prerequisites |
|---|---|
| 1 | System is configured with the SPECIALIST_MAP. |

Test Data:
| No. | Test Data |
|---|---|
| 1 | Condition: Diabetes (Expects Endocrinologist) |

Test Conditions:
The AI predicts a condition that exists in the predefined specialist mapping.

Steps:
| Step # | Step Details | Expected Result |
|---|---|---|
| 1 | AI predicts the disease based on features. | Condition predicted correctly. |
| 2 | AI looks up the specialist mapping. | System retrieves the correct specialist name. |
| 3 | Return results to the patient. | Triage result displays the recommended specialist. |

#### 2.2.6 TC003_04: AI fallback to General Practitioner if disease unmapped

Test Case ID:
TC003_04

Test Case Description:
Verify that the AI Triage service defaults to General Practitioner if the predicted condition has no specific specialist mapped.

Created by:
Shams Ahmed

Version:
1.0

Prerequisites:
| No. | Prerequisites |
|---|---|
| 1 | AI predicts a condition not present in SPECIALIST_MAP. |

Test Data:
| No. | Test Data |
|---|---|
| 1 | Unmapped condition prediction |

Test Conditions:
The condition prediction falls outside explicitly mapped specialties.

Steps:
| Step # | Step Details | Expected Result |
|---|---|---|
| 1 | AI predicts the condition. | Condition predicted. |
| 2 | AI looks up the specialist mapping. | Mapping not found, defaults to "General Practitioner". |
| 3 | Return results to the patient. | Triage result displays "General Practitioner". |

#### 2.2.7 TC003_05: Auto-assign available specialist after AI analysis

Test Case ID:
TC003_05

Test Case Description:
Verify that the system automatically assigns an available doctor of the recommended specialty to the patient's case.

Created by:
Shams Ahmed

Version:
1.0

Prerequisites:
| No. | Prerequisites |
|---|---|
| 1 | AI returns a specialist recommendation. |
| 2 | An active, available doctor of that specialty exists. |

Test Data:
| No. | Test Data |
|---|---|
| 1 | Specialist: Dermatologist |

Test Conditions:
The system queries the database for a doctor matching the recommended specialty and availability.

Steps:
| Step # | Step Details | Expected Result |
|---|---|---|
| 1 | Retrieve specialist recommendation from AI. | Recommendation obtained. |
| 2 | Query Doctor table for matching specialization and available status. | Matching doctor found. |
| 3 | Update SymptomRecord with doctor ID. | Symptom record is saved with the assigned `doctor_id`. |

#### 2.2.8 TC003_06: AI service failure/timeout handling

Test Case ID:
TC003_06

Test Case Description:
Verify that the system gracefully handles an exception or timeout from the AI Triage Service.

Created by:
Shams Ahmed

Version:
1.0

Prerequisites:
| No. | Prerequisites |
|---|---|
| 1 | AI Triage model is missing or throws an exception. |

Test Data:
| No. | Test Data |
|---|---|
| 1 | Invalid input or simulated failure |

Test Conditions:
The AI prediction process fails during symptom submission.

Steps:
| Step # | Step Details | Expected Result |
|---|---|---|
| 1 | Patient submits symptoms. | Submission begins. |
| 2 | System attempts to call AI service and catches exception. | Exception caught. |
| 3 | System handles failure state. | Record marked as 'failed', and patient receives message "AI analysis failed. Please try again later." |

### 2.3 Test Cases for Module: Triage Result Display

#### 2.3.1 TC006_01: View complete triage result for a valid record

Test Case ID:
TC006_01

Test Case Description:
Verify that the patient can view their AI triage results including urgency, condition, and specialist.

Created by:
Shams Ahmed

Version:
1.0

Prerequisites:
| No. | Prerequisites |
|---|---|
| 1 | Patient has a completed symptom record. |

Test Data:
| No. | Test Data |
|---|---|
| 1 | Valid Record ID |

Test Conditions:
Patient clicks to view a completed triage result.

Steps:
| Step # | Step Details | Expected Result |
|---|---|---|
| 1 | Navigate to Triage Result page using record ID. | Page loads successfully. |
| 2 | View displayed data. | Page displays Urgency Level, Predicted Condition, Recommended Specialist, Description, and Precautions. |

#### 2.3.2 TC006_02: Prevent access to another patient's triage result

Test Case ID:
TC006_02

Test Case Description:
Verify that a patient cannot view triage records belonging to other patients.

Created by:
Shams Ahmed

Version:
1.0

Prerequisites:
| No. | Prerequisites |
|---|---|
| 1 | Patient is logged in. |
| 2 | Record ID belongs to a different patient. |

Test Data:
| No. | Test Data |
|---|---|
| 1 | Unauthorized Record ID |

Test Conditions:
Patient attempts to access a URL containing another user's record ID.

Steps:
| Step # | Step Details | Expected Result |
|---|---|---|
| 1 | Attempt to load Triage Result page for unauthorized record ID. | System validates ownership. |
| 2 | System responds to unauthorized access. | System returns a 404 Not Found or Access Denied error. |

#### 2.3.3 TC006_03: Handle viewing a non-existent triage record

Test Case ID:
TC006_03

Test Case Description:
Verify that the system handles requests for invalid or deleted record IDs gracefully.

Created by:
Shams Ahmed

Version:
1.0

Prerequisites:
| No. | Prerequisites |
|---|---|
| 1 | Patient is logged in. |

Test Data:
| No. | Test Data |
|---|---|
| 1 | Record ID: 99999 (non-existent) |

Test Conditions:
Patient navigates to a triage result URL with an invalid ID.

Steps:
| Step # | Step Details | Expected Result |
|---|---|---|
| 1 | Navigate to Triage Result page with invalid ID. | System queries the database. |
| 2 | System handles missing record. | System displays a 404 Error Page. |

#### 2.3.4 TC006_04: Patient views triage history with filtering and sorting

Test Case ID:
TC006_04

Test Case Description:
Verify that a patient can view their symptom history and filter by urgency or sort by date.

Created by:
Shams Ahmed

Version:
1.0

Prerequisites:
| No. | Prerequisites |
|---|---|
| 1 | Patient has multiple symptom records. |

Test Data:
| No. | Test Data |
|---|---|
| 1 | Filter: "urgent" |
| 2 | Sort: "asc" |

Test Conditions:
Patient navigates to the history page and applies filters.

Steps:
| Step # | Step Details | Expected Result |
|---|---|---|
| 1 | Navigate to History page. | Shows all records by default. |
| 2 | Apply 'urgent' filter. | List updates to show only urgent records. |
| 3 | Apply ascending date sort. | Records are reordered oldest to newest. |

### 2.4 Test Cases for Module: Appointment Scheduling

#### 2.4.1 TC007_01: View available appointment slots for urgent case

Test Case ID:
TC007_01

Test Case Description:
Verify that urgent cases are offered slots starting from the next day.

Created by:
Shams Ahmed

Version:
1.0

Prerequisites:
| No. | Prerequisites |
|---|---|
| 1 | Patient has an urgent triage record. |

Test Data:
| No. | Test Data |
|---|---|
| 1 | Urgency: "urgent" |

Test Conditions:
System calculates available slots based on the "urgent" rule (starts tomorrow).

Steps:
| Step # | Step Details | Expected Result |
|---|---|---|
| 1 | Request available slots for a doctor with urgent status. | API returns slots. |
| 2 | Check the earliest available date. | The earliest slot date is tomorrow (T+1 day), excluding weekends. |

#### 2.4.2 TC007_02: View available appointment slots for non-urgent case

Test Case ID:
TC007_02

Test Case Description:
Verify that non-urgent cases are offered slots starting from 3 days ahead.

Created by:
Shams Ahmed

Version:
1.0

Prerequisites:
| No. | Prerequisites |
|---|---|
| 1 | Patient has a non-urgent triage record. |

Test Data:
| No. | Test Data |
|---|---|
| 1 | Urgency: "non-urgent" |

Test Conditions:
System calculates available slots based on the "non-urgent" rule (starts T+3 days).

Steps:
| Step # | Step Details | Expected Result |
|---|---|---|
| 1 | Request available slots for a doctor with non-urgent status. | API returns slots. |
| 2 | Check the earliest available date. | The earliest slot date is at least 3 days from today, excluding weekends. |

#### 2.4.3 TC007_03: Book appointment with an available slot

Test Case ID:
TC007_03

Test Case Description:
Verify that a patient can successfully book an available appointment slot.

Created by:
Shams Ahmed

Version:
1.0

Prerequisites:
| No. | Prerequisites |
|---|---|
| 1 | Patient has viewed available slots. |

Test Data:
| No. | Test Data |
|---|---|
| 1 | Valid Doctor ID, Date, and Time |

Test Conditions:
The patient selects an open slot and confirms booking.

Steps:
| Step # | Step Details | Expected Result |
|---|---|---|
| 1 | Select a valid time slot. | Slot is selected. |
| 2 | Confirm booking via API. | System creates appointment record, updates symptom case status to "in-review", and returns success. |

#### 2.4.4 TC007_04: Attempt to book an already booked slot

Test Case ID:
TC007_04

Test Case Description:
Verify that the system prevents booking a slot that has just been taken (conflict detection).

Created by:
Shams Ahmed

Version:
1.0

Prerequisites:
| No. | Prerequisites |
|---|---|
| 1 | A specific slot is already booked by another patient. |

Test Data:
| No. | Test Data |
|---|---|
| 1 | Booked Date and Time |

Test Conditions:
The patient attempts to book a slot that exists in the database as "requested" or "scheduled".

Steps:
| Step # | Step Details | Expected Result |
|---|---|---|
| 1 | Submit booking request for the already booked slot. | System checks for conflicts. |
| 2 | View system response. | System rejects booking and displays "This slot is no longer available. Please select another." |

#### 2.4.5 TC007_05: Cancel a scheduled appointment by patient

Test Case ID:
TC007_05

Test Case Description:
Verify that a patient can cancel their own scheduled appointment.

Created by:
Shams Ahmed

Version:
1.0

Prerequisites:
| No. | Prerequisites |
|---|---|
| 1 | Patient has a scheduled appointment. |

Test Data:
| No. | Test Data |
|---|---|
| 1 | Scheduled Appointment ID |

Test Conditions:
Patient triggers the cancellation action for a valid appointment.

Steps:
| Step # | Step Details | Expected Result |
|---|---|---|
| 1 | Send cancel request for the appointment. | System validates ownership and status. |
| 2 | System processes cancellation. | Appointment status changes to "cancelled" and success message is returned. |

#### 2.4.6 TC007_06: Attempt to cancel an appointment with invalid status

Test Case ID:
TC007_06

Test Case Description:
Verify that a patient cannot cancel an appointment that is already completed or cancelled.

Created by:
Shams Ahmed

Version:
1.0

Prerequisites:
| No. | Prerequisites |
|---|---|
| 1 | Patient has an appointment with status "completed" or "cancelled". |

Test Data:
| No. | Test Data |
|---|---|
| 1 | Cancelled Appointment ID |

Test Conditions:
Patient attempts to cancel an appointment that is not in a cancellable state.

Steps:
| Step # | Step Details | Expected Result |
|---|---|---|
| 1 | Send cancel request for the completed/cancelled appointment. | System validates status. |
| 2 | View system response. | System rejects request with "Cannot cancel appointment with status..." |

### 2.5 Test Cases for Module: Notifications and Workflow Automation

#### 2.5.1 TC008_01: Receive appointment confirmation notification

Test Case ID:
TC008_01

Test Case Description:
Verify that both patient and doctor receive automated notifications when an appointment is booked.

Created by:
Shams Ahmed

Version:
1.0

Prerequisites:
| No. | Prerequisites |
|---|---|
| 1 | Patient successfully books an appointment. |

Test Data:
| No. | Test Data |
|---|---|
| 1 | Booking details |

Test Conditions:
The system's notification service is triggered after a successful booking transaction.

Steps:
| Step # | Step Details | Expected Result |
|---|---|---|
| 1 | Complete appointment booking. | Booking succeeds. |
| 2 | Check patient notifications. | New unread notification exists for the patient confirming the schedule. |
| 3 | Check doctor notifications. | New unread notification exists for the doctor regarding the new appointment. |
| 4 | Check internal email log. | Email simulation logs show emails sent to both parties. |

#### 2.5.2 TC008_02: Receive case status update notification

Test Case ID:
TC008_02

Test Case Description:
Verify that a patient receives a notification when a doctor updates their case status.

Created by:
Shams Ahmed

Version:
1.0

Prerequisites:
| No. | Prerequisites |
|---|---|
| 1 | Doctor updates a patient's case status via dashboard. |

Test Data:
| No. | Test Data |
|---|---|
| 1 | New status: "consulted" |

Test Conditions:
The notification service is triggered upon status update.

Steps:
| Step # | Step Details | Expected Result |
|---|---|---|
| 1 | Doctor updates case status to "consulted". | Update succeeds. |
| 2 | Patient checks notifications. | New unread notification alerts patient of the status change. |

#### 2.5.3 TC008_03: Mark notification as read

Test Case ID:
TC008_03

Test Case Description:
Verify that a user can mark a specific notification as read.

Created by:
Shams Ahmed

Version:
1.0

Prerequisites:
| No. | Prerequisites |
|---|---|
| 1 | User has an unread notification. |

Test Data:
| No. | Test Data |
|---|---|
| 1 | Notification ID |

Test Conditions:
The user triggers the read action on a specific notification.

Steps:
| Step # | Step Details | Expected Result |
|---|---|---|
| 1 | Send request to mark notification as read. | System updates database record. |
| 2 | Retrieve notification status. | Notification `is_read` flag is True, and unread count decreases by 1. |

#### 2.5.4 TC008_04: Mark all notifications as read

Test Case ID:
TC008_04

Test Case Description:
Verify that a user can mark all their notifications as read simultaneously.

Created by:
Shams Ahmed

Version:
1.0

Prerequisites:
| No. | Prerequisites |
|---|---|
| 1 | User has multiple unread notifications. |

Test Data:
| No. | Test Data |
|---|---|
| 1 | None |

Test Conditions:
The user triggers the "mark all as read" action.

Steps:
| Step # | Step Details | Expected Result |
|---|---|---|
| 1 | Send request to mark all notifications as read. | System updates all records for the user. |
| 2 | Retrieve unread count. | Unread count is exactly 0. |

### 2.6 Test Cases for Module: Doctor Module

#### 2.6.1 TC009_01: Doctor views assigned cases sorted by urgency

Test Case ID:
TC009_01

Test Case Description:
Verify that the doctor dashboard displays assigned cases, prioritizing "urgent" cases at the top.

Created by:
Shams Ahmed

Version:
1.0

Prerequisites:
| No. | Prerequisites |
|---|---|
| 1 | Doctor is logged in. |
| 2 | Doctor has both urgent and non-urgent assigned cases. |

Test Data:
| No. | Test Data |
|---|---|
| 1 | Urgent and non-urgent records |

Test Conditions:
The system queries and sorts the symptom records based on urgency level and date.

Steps:
| Step # | Step Details | Expected Result |
|---|---|---|
| 1 | Navigate to Doctor Dashboard. | Dashboard loads. |
| 2 | Observe the assigned cases list. | The list displays all "urgent" cases before "non-urgent" cases. |

#### 2.6.2 TC009_02: Doctor views detailed case and AI triage results

Test Case ID:
TC009_02

Test Case Description:
Verify that a doctor can view the detailed symptoms, AI predictions, and patient info for an assigned case.

Created by:
Shams Ahmed

Version:
1.0

Prerequisites:
| No. | Prerequisites |
|---|---|
| 1 | Doctor is logged in. |
| 2 | Doctor clicks on a specific case. |

Test Data:
| No. | Test Data |
|---|---|
| 1 | Valid assigned Record ID |

Test Conditions:
The doctor accesses the detailed view of a symptom record assigned to them.

Steps:
| Step # | Step Details | Expected Result |
|---|---|---|
| 1 | Navigate to Case Details page. | Page loads successfully. |
| 2 | Verify displayed information. | Patient details, exact symptoms list, AI predicted condition, and urgency are clearly displayed. |

#### 2.6.3 TC010_01: Doctor updates patient case status successfully

Test Case ID:
TC010_01

Test Case Description:
Verify that a doctor can update the status of a patient's case.

Created by:
Shams Ahmed

Version:
1.0

Prerequisites:
| No. | Prerequisites |
|---|---|
| 1 | Doctor is on the Case Details page. |

Test Data:
| No. | Test Data |
|---|---|
| 1 | New Status: "closed" |

Test Conditions:
The doctor submits a valid status update request.

Steps:
| Step # | Step Details | Expected Result |
|---|---|---|
| 1 | Select "closed" from status dropdown and save. | System validates status and updates the database. |
| 2 | Verify record state. | Case status is updated to "closed" and success message is shown. |

#### 2.6.4 TC010_02: Doctor adds consultation notes successfully

Test Case ID:
TC010_02

Test Case Description:
Verify that a doctor can independently add or modify consultation notes without changing the overall status.

Created by:
Shams Ahmed

Version:
1.0

Prerequisites:
| No. | Prerequisites |
|---|---|
| 1 | Doctor is on the Case Details page. |

Test Data:
| No. | Test Data |
|---|---|
| 1 | Notes: "Patient advised to rest." |

Test Conditions:
The doctor saves notes via the dedicated notes API route.

Steps:
| Step # | Step Details | Expected Result |
|---|---|---|
| 1 | Enter text in the consultation notes field. | Text accepted. |
| 2 | Click "Save Notes". | System saves notes to the database and displays success message. |

#### 2.6.5 TC010_03: Attempt to update status with invalid state

Test Case ID:
TC010_03

Test Case Description:
Verify that the system rejects status updates that use undefined status strings.

Created by:
Shams Ahmed

Version:
1.0

Prerequisites:
| No. | Prerequisites |
|---|---|
| 1 | Doctor attempts to bypass UI and send invalid status via API. |

Test Data:
| No. | Test Data |
|---|---|
| 1 | Status: "unknown-status" |

Test Conditions:
The backend validates the provided status string against allowed states.

Steps:
| Step # | Step Details | Expected Result |
|---|---|---|
| 1 | Send PUT request with invalid status string. | System validates input. |
| 2 | Observe API response. | API returns 400 Error: "Invalid status. Must be one of: new, in-review, consulted, closed". |

### 2.7 Test Cases for Module: Admin Module

#### 2.7.1 TC011_01: Admin creates a new doctor account

Test Case ID:
TC011_01

Test Case Description:
Verify that an administrator can create a new doctor account with valid details.

Created by:
Shams Ahmed

Version:
1.0

Prerequisites:
| No. | Prerequisites |
|---|---|
| 1 | Admin is logged in. |

Test Data:
| No. | Test Data |
|---|---|
| 1 | Name, Email, Password, Specialization |

Test Conditions:
Admin provides all required data meeting validation rules to create a doctor.

Steps:
| Step # | Step Details | Expected Result |
|---|---|---|
| 1 | Navigate to Manage Users and select Add Doctor. | Form is displayed. |
| 2 | Fill in valid details and submit. | System creates doctor account, logs the action in the audit log, and returns success. |

#### 2.7.2 TC011_02: Admin updates existing user details

Test Case ID:
TC011_02

Test Case Description:
Verify that an admin can update basic information for a user.

Created by:
Shams Ahmed

Version:
1.0

Prerequisites:
| No. | Prerequisites |
|---|---|
| 1 | Admin is logged in. |
| 2 | Target user exists. |

Test Data:
| No. | Test Data |
|---|---|
| 1 | New Name: Dr. Updated Name |

Test Conditions:
Admin submits an update request for a specific user ID and role.

Steps:
| Step # | Step Details | Expected Result |
|---|---|---|
| 1 | Submit update request with new name. | System applies the change. |
| 2 | Check user record and audit log. | User's name is updated and action is recorded in the audit log. |

#### 2.7.3 TC011_03: Admin deactivates a user account

Test Case ID:
TC011_03

Test Case Description:
Verify that an admin can deactivate a user account, preventing their login.

Created by:
Shams Ahmed

Version:
1.0

Prerequisites:
| No. | Prerequisites |
|---|---|
| 1 | Admin is logged in. |
| 2 | Target user is active. |

Test Data:
| No. | Test Data |
|---|---|
| 1 | User ID to deactivate |

Test Conditions:
Admin clicks to deactivate an active user.

Steps:
| Step # | Step Details | Expected Result |
|---|---|---|
| 1 | Trigger deactivation for the user. | System changes `account_status` to "inactive". |
| 2 | Attempt to log in as the deactivated user. | Login fails because the account is not active. |

#### 2.7.4 TC012_01: Admin configures doctor availability status

Test Case ID:
TC012_01

Test Case Description:
Verify that an admin can toggle a doctor's overall availability (available/unavailable).

Created by:
Shams Ahmed

Version:
1.0

Prerequisites:
| No. | Prerequisites |
|---|---|
| 1 | Admin is logged in to Configure Schedules page. |

Test Data:
| No. | Test Data |
|---|---|
| 1 | Availability: "unavailable" |

Test Conditions:
Admin submits an availability update for a specific doctor.

Steps:
| Step # | Step Details | Expected Result |
|---|---|---|
| 1 | Send update request changing availability to "unavailable". | System saves change. |
| 2 | Verify doctor's record. | Doctor's status is "unavailable" and will not be auto-assigned new AI cases. |

#### 2.7.5 TC012_02: Admin configures doctor working hours with valid format

Test Case ID:
TC012_02

Test Case Description:
Verify that an admin can set specific start and end working hours for a doctor.

Created by:
Shams Ahmed

Version:
1.0

Prerequisites:
| No. | Prerequisites |
|---|---|
| 1 | Admin is logged in. |

Test Data:
| No. | Test Data |
|---|---|
| 1 | Start: 9, End: 15 |

Test Conditions:
Admin provides valid integer hours in 24h format where start < end.

Steps:
| Step # | Step Details | Expected Result |
|---|---|---|
| 1 | Send request with valid start and end hours. | System serializes hours to JSON and saves to the doctor's `schedule_hours` field. |
| 2 | Verify appointment slots for this doctor. | Available slots only generate between 09:00 and 15:00. |

#### 2.7.6 TC012_03: Admin configures doctor working hours with invalid format

Test Case ID:
TC012_03

Test Case Description:
Verify that the system rejects invalid working hour configurations.

Created by:
Shams Ahmed

Version:
1.0

Prerequisites:
| No. | Prerequisites |
|---|---|
| 1 | Admin is logged in. |

Test Data:
| No. | Test Data |
|---|---|
| 1 | Start: 18, End: 9 (start > end) |

Test Conditions:
Admin attempts to set an end time that occurs before the start time.

Steps:
| Step # | Step Details | Expected Result |
|---|---|---|
| 1 | Send request with invalid hours. | System validates logic. |
| 2 | Observe response. | System rejects request with error "Invalid hours. start must be < end". |

### 2.8 Test Cases for Module: Role-Based Access Control

#### 2.8.1 TC019_01: Patient restricted from accessing doctor dashboard

Test Case ID:
TC019_01

Test Case Description:
Verify that a patient account cannot access doctor-specific routes or APIs.

Created by:
Shams Ahmed

Version:
1.0

Prerequisites:
| No. | Prerequisites |
|---|---|
| 1 | User is logged in as a Patient. |

Test Data:
| No. | Test Data |
|---|---|
| 1 | URL: `/doctor/dashboard` |

Test Conditions:
Patient attempts to navigate directly to the doctor dashboard URL.

Steps:
| Step # | Step Details | Expected Result |
|---|---|---|
| 1 | Enter `/doctor/dashboard` into the browser URL. | The `@role_required` decorator intercepts the request. |
| 2 | Observe system behavior. | User is redirected to the login page and sees "You do not have permission to access this page." |

#### 2.8.2 TC019_02: Doctor restricted from accessing admin dashboard

Test Case ID:
TC019_02

Test Case Description:
Verify that a doctor account cannot access administrative routes or APIs.

Created by:
Shams Ahmed

Version:
1.0

Prerequisites:
| No. | Prerequisites |
|---|---|
| 1 | User is logged in as a Doctor. |

Test Data:
| No. | Test Data |
|---|---|
| 1 | URL: `/admin/dashboard` |

Test Conditions:
Doctor attempts to navigate directly to the admin dashboard URL.

Steps:
| Step # | Step Details | Expected Result |
|---|---|---|
| 1 | Enter `/admin/dashboard` into the browser URL. | System intercepts the request. |
| 2 | Observe system behavior. | User is redirected with a permission denied error. |

#### 2.8.3 TC019_03: Unauthenticated user redirected to login

Test Case ID:
TC019_03

Test Case Description:
Verify that an unauthenticated user cannot access any protected routes.

Created by:
Shams Ahmed

Version:
1.0

Prerequisites:
| No. | Prerequisites |
|---|---|
| 1 | User is not logged in. |

Test Data:
| No. | Test Data |
|---|---|
| 1 | URL: `/patient/dashboard` |

Test Conditions:
Anonymous user attempts to view a protected page.

Steps:
| Step # | Step Details | Expected Result |
|---|---|---|
| 1 | Attempt to navigate to a protected page. | The `@login_required` decorator intercepts the request. |
| 2 | Observe system behavior. | User is automatically redirected to the login page. |

## 3. Traceability Matrix

| Requirement / Use Case | Feature / Module | Test Case IDs | Coverage Type |
|---|---|---|---|
| UC001 – Register | Patient Account Management | TC001_01, TC001_02, TC001_03 | Positive/Negative |
| NFR-002 to NFR-005 | Form Validation | TC001_02, TC001_03 | Validation |
| Authentication (Login/Logout) | Patient Account Management | TC001_04, TC001_05, TC001_06 | Positive/Negative |
| UC002 – Submit Symptoms | Symptom Submission | TC002_01, TC002_02 | Positive/Negative |
| UC003 – Analyse Symptoms | AI Triage | TC003_06 | Exception |
| UC004 – Classify Urgency | AI Triage | TC003_01, TC003_02 | Core Logic |
| UC005 – Recommend Specialist | AI Triage | TC003_03, TC003_04, TC003_05 | Core Logic |
| UC006 – View Triage Result | Triage Result Display | TC006_01, TC006_02, TC006_03, TC006_04 | Display/Security |
| UC007 – Book Appointment | Appointment Scheduling | TC007_01, TC007_02, TC007_03, TC007_04, TC007_05, TC007_06 | Positive/Negative |
| UC008 – Receive Notifications | Notifications and Workflow | TC008_01, TC008_02, TC008_03, TC008_04 | Integration |
| UC009 – View Patient Cases | Doctor Module | TC009_01, TC009_02 | Display Logic |
| UC010 – Update Case Status | Doctor Module | TC010_01, TC010_02, TC010_03 | Positive/Negative |
| UC011 – Manage Users | Admin Module | TC011_01, TC011_02, TC011_03 | CRUD |
| UC012 – Configure Schedules | Admin Module | TC012_01, TC012_02, TC012_03 | Configuration |
| NFR-019 – Role Restrictions | Access Control | TC019_01, TC019_02, TC019_03 | Security |
