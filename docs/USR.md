# USR.md

| Field | Value |
|---|---|
| **Document Name** | Use Case and System Requirements Document – CLINK Smart Outpatient Triage and Scheduling System |
| **Version** | 1.0 |
| **Date** | January 2026 (SRS dated 15/12/2025) |
| **Status** | Initial Draft |
| **Source Reference** | CLINK – Smart Outpatient Triage and Scheduling System (FYP Report, UTM, January 2026); Appendix B: Software Requirements Specification (SRS) v1.0; Appendix D: Software Test Documentation (STD) v1.0 |
| **Description** | This USR is derived exclusively from the CLINK FYP thesis and its embedded SRS and STD appendices. It documents the system overview, actor definitions, all functional and non-functional requirements, complete use case specifications (including flows and original table reproductions), and traceability mapping. |

---

# 1. System Overview

## 1.1 System Purpose

CLINK – Smart Outpatient Triage and Scheduling System is a web-based healthcare support system designed to automate the outpatient triage and appointment scheduling process. The system analyses patient-submitted symptoms using artificial intelligence to determine urgency levels and recommend an appropriate specialist. It then generates suitable appointment slots and provides doctors with a prioritised case dashboard.

## 1.2 System Boundary

### External Entities

| Entity | Role |
|---|---|
| Patient | Registers account, submits symptoms, views triage results, books appointments, receives notifications |
| Doctor | Reviews prioritised patient cases, views AI triage results, updates case status and consultation notes |
| Admin (Administrative Staff) | Manages patient and doctor accounts, configures specialist schedules |
| AI Triage Service | External system that receives symptom data, analyses it, and returns urgency classification and specialist recommendation |

### Internal Subsystems

| Subsystem | Responsibility |
|---|---|
| Patient Management Subsystem | Handles patient registration, login, symptom submission, and case creation |
| AI Processing Subsystem | Classifies cases by urgency (urgent/non-urgent); recommends appropriate medical specialists |
| Doctor Dashboard Subsystem | Displays prioritised patient cases to doctors; supports case status updates |
| Notification Subsystem | Sends automated updates to patients and doctors via n8n workflow automation |
| Database Subsystem (CLINK_DB) | Stores all persistent data including patient records, appointments, symptom records, and notifications |

## 1.3 High-Level Interaction Diagram

```
+------------------+        HTTP/HTTPS REST API        +------------------------+
|   Patient (UI)   |<--------------------------------->|  Patient Management    |
+------------------+                                   |  Subsystem             |
                                                       |                        |
+------------------+        HTTP/HTTPS REST API        |  AI Processing         |
|   Doctor (UI)    |<--------------------------------->|  Subsystem             |
+------------------+                                   |                        |
                                                       |  Doctor Dashboard      |
+------------------+        HTTP/HTTPS REST API        |  Subsystem             |
|   Admin (UI)     |<--------------------------------->|                        |
+------------------+                                   |  Notification          |
                                                       |  Subsystem             |
                                                       |                        |
+-------------------+   Symptom Data / AI Result       |  Appointment           |
| AI Triage Service |<-------------------------------->|  Scheduler             |
| (External)        |                                  +----------+-------------+
+-------------------+                                             |
                                                                  v
+-------------------+   n8n API                       +----------+-------------+
|  n8n Workflow     |<--------------------------------|  CLINK_DB              |
|  (Notifications)  |                                 |  (Relational Database) |
+-------------------+                                 +------------------------+
```

---

# 2. Actor Definitions

## 2.1 Primary Actor — Patient

| Attribute | Description |
|---|---|
| Actor Name | Patient |
| Type | Primary (Human) |
| Description | A person who requires outpatient medical care and interacts with CLINK to submit symptoms, receive triage guidance, and book appointments. |
| User Need | A patient needs a way to receive accurate triage guidance, understand the urgency of their symptoms, and schedule an appropriate outpatient appointment efficiently. |
| Goal | Access the outpatient triage and scheduling services without manual intervention. |

**Capabilities:**
- Register an account in the system.
- Enter symptoms into the system.
- View urgency classification (urgent or non-urgent).
- View recommended specialist.
- View and select recommended appointment slots.
- Book an outpatient appointment.
- Receive notifications about appointment status changes.

## 2.2 Secondary Actor — Doctor

| Attribute | Description |
|---|---|
| Actor Name | Doctor |
| Type | Secondary (Human) |
| Description | A licensed medical professional who reviews AI-assisted patient cases and manages consultation activities via the doctor dashboard. |
| User Need | A doctor needs a way to review patient cases, prioritise urgent cases, and manage consultation activities effectively. |
| Goal | Attend to urgent patients first and maintain accurate case records. |

**Capabilities:**
- View a prioritised list of assigned patient cases.
- View patient symptoms and AI-generated triage results.
- Update the status of patient cases.

## 2.3 Supporting Actors

### Actor: Administrative Staff (Admin)

| Attribute | Description |
|---|---|
| Actor Name | Administrative Staff (Admin) |
| Type | Supporting (Human) |
| Description | A hospital/clinic staff member responsible for system management, including user accounts and specialist schedules. |
| User Need | An administrative staff member needs a way to manage users, configure schedules, and maintain the smooth operation of outpatient workflows. |
| Goal | Ensure accurate and secure access control and valid appointment slot recommendations. |

**Capabilities:**
- Manage patient and doctor accounts.
- Configure specialist schedules and availability.

### Actor: AI Triage Service (External)

| Attribute | Description |
|---|---|
| Actor Name | AI Triage Service |
| Type | External System Actor |
| Description | An external AI-based service (using Python with scikit-learn Decision Tree, pandas, NumPy) that receives symptom data and returns urgency classification and specialist recommendations. Human involvement is reduced given it addresses a straightforward classification issue. |

---

# 3. Functional Requirements (FR)

Table derived from Table 4.2.1 (Exact):

| FR ID | Description | Priority | Related UC |
|---|---|---|---|
| FR-001 | The system enables patients to create an account to have access to the system. | [Not stated] | UC001 |
| FR-002 | The system enables patients to enter the information on the symptoms to be triaged. | [Not stated] | UC002 |
| FR-003 | The system forwards the symptom data uploaded to the AI Triage Service to be analysed. | [Not stated] | UC003 |
| FR-004 | The system categorises patient conditions as urgent or nonurgent according to the analysis of AI. | [Not stated] | UC004 |
| FR-005 | The system suggests a doctor specialist depending on the analysed symptoms. | [Not stated] | UC005 |
| FR-006 | The system enables the patients to see the result of the triage and specialist recommendations. | [Not stated] | UC006 |
| FR-007 | The system enables patients to make an outpatient appointment with slots recommended. | [Not stated] | UC007 |
| FR-008 | The system will provide automated messages concerning appointment and case updates. | [Not stated] | UC008 |
| FR-009 | The system enables the doctors to see and prioritise the assigned cases of patients. | [Not stated] | UC009 |
| FR-010 | The system enables doctors to update the status of the cases of patients and their consultations. | [Not stated] | UC010 |
| FR-011 | The system enables administrators to deal with patient and doctor user accounts. | [Not stated] | UC011 |
| FR-012 | The system enables administrators to set schedules and availability of specialists. | [Not stated] | UC012 |

---

# 4. Non-Functional Requirements (NFR)

Derived from Table 4.2.2 (Exact):

### Performance

| ID | Requirement |
|---|---|
| NFR-001 | The system shall authenticate users within 10 seconds. |
| NFR-002 | The system shall accept only valid email formats for registration and login. |
| NFR-003 | The system shall accept passwords containing at least one number, one special character, and a minimum length of 6 characters. |
| NFR-004 | The system shall accept name fields that are not blank and contain only alphabetic characters and non-consecutive spaces. |
| NFR-005 | The system shall accept phone numbers containing only numeric values with valid local formats. |
| NFR-006 | The system shall process AI-based triage results within an acceptable response time. |
| NFR-007 | All system ID fields shall be auto-generated and uniquely identifiable. |
| NFR-008 | The system shall retrieve data from the database within 10 seconds. |
| NFR-009 | The system shall update existing records in the database within 10 seconds. |
| NFR-010 | The system shall insert new records into the database within 10 seconds. |

### Design Constraint

| ID | Requirement |
|---|---|
| NFR-011 | The system user interfaces shall be displayed in English and Arabic. |
| NFR-012 | The system shall not display any content that is offensive to any race, religion, or culture. |
| NFR-013 | The system shall be developed as a web-based application accessible via a standard web browser. |
| NFR-014 | The development duration of the system shall not exceed the allocated project timeline. |

### Usability

| ID | Requirement |
|---|---|
| NFR-015 | The system functionalities shall be accessible only to authenticated users. |
| NFR-016 | The system functionalities shall be accessible within five user interactions (clicks). |

### Compatibility

| ID | Requirement |
|---|---|
| NFR-017 | The system shall be compatible with modern web browsers with a stable internet connection. |

### Portability

| ID | Requirement |
|---|---|
| NFR-018 | The system shall be accessible on any device that supports a web browser and internet connectivity. |

### Security

| ID | Requirement |
|---|---|
| NFR-019 | The system shall restrict access to functionalities based on user roles (patient, doctor, admin). |

### Availability

| ID | Requirement |
|---|---|
| NFR-020 | The system shall be available 24 hours a day, except during scheduled maintenance. |

### Maintainability

| ID | Requirement |
|---|---|
| NFR-021 | System maintenance activities shall not exceed 24 hours per maintenance period. |

### Reliability

| ID | Requirement |
|---|---|
| NFR-022 | The system shall perform its core functionalities with at least 99% reliability. |

---

# 5. Detailed Use Case Specifications

---

## UC001 – Register

### Use Case Overview

| Field | Description |
|---|---|
| ID | UC001 |
| Name | Register |
| Actor | Patient |
| Related FR | FR-001 |

### Preconditions

1. Patient is not already registered.
2. CLINK system is available.

### Normal Flow

| Step | Actor/System | Action |
|---|---|---|
| 1 | Patient | Navigates to the registration page. |
| 2 | Patient | Enters details. |
| 3 | System | Validates input. |
| 4 | System | Creates account. |
| 5 | System | Confirms registration. |

### Alternative Flows

**AF1: Patient cancels registration**
1. Patient cancels registration.
2. System discards input and returns to home page.

### Exception Flows

**EF1: System fails to save**
1. System fails to save.
2. System displays error.
3. System prompts retry.

### Postconditions

1. Account created and active.

---

**Table 2.4.1: User Story Description for Patient Registration (Exact)**

| Field | Description |
|---|---|
| User Story ID | US001 |
| User Story Name | Patient Registration |
| User Story Description | As a patient, I want to register an account in the system, so that I can access the outpatient triage and scheduling services. |
| Acceptance Criteria(s) | Postcondition: Account created and active. Precondition: Patient not registered. |
| Normal Flow(s) – NF | 1. Patient navigates to the registration page. 2. Patient enters details. 3. System validates input. 4. System creates account. 5. System confirms registration. |
| Alternative Flow(s) – AF | AF1: Patient cancels registration → system discards input and returns to home page. |
| Exception Flow(s) – EF | EF1: System fails to save → display error, prompt retry. |

---

## UC002 – Submit Symptoms

### Use Case Overview

| Field | Description |
|---|---|
| ID | UC002 |
| Name | Submit Symptoms |
| Actor | Patient |
| Related FR | FR-002 |

### Preconditions

1. Patient is logged in.

### Normal Flow

| Step | Actor/System | Action |
|---|---|---|
| 1 | Patient | Navigates to submit symptoms page. |
| 2 | Patient | Enters symptoms. |
| 3 | System | Sends symptoms to AI Triage Service. |
| 4 | AI Triage Service | Analyses and returns result. |
| 5 | System | Displays triage outcome. |

### Alternative Flows

**AF1: Patient edits symptoms before submission**
1. Patient edits symptoms before submission.
2. System updates submission.

### Exception Flows

**EF1: AI service unavailable**
1. AI service is unavailable.
2. System displays error and prompts retry.

### Postconditions

1. Symptoms submitted and triage result available.

---

**Table 2.4.2: User Story Description for Submit Symptoms (Exact)**

| Field | Description |
|---|---|
| User Story ID | US002 |
| User Story Name | Submit Symptoms |
| User Story Description | As a patient, I want to enter my symptoms into the system, so that I can receive guidance on which specialist I should consult. |
| Acceptance Criteria(s) | Precondition: Patient logged in. Postcondition: Symptoms submitted and triage result available. |
| Normal Flow(s) – NF | 1. Patient navigates to submit symptoms page. 2. Patient enters symptoms. 3. System sends symptoms to AI Triage Service. 4. AI analyses and returns result. 5. System displays triage outcome. |
| Alternative Flow(s) – AF | AF1: Patient edits symptoms before submission → system updates submission. |
| Exception Flow(s) – EF | EF1: AI service unavailable → system displays error and prompts retry. |

---

## UC003 – Analyse Symptoms

### Use Case Overview

| Field | Description |
|---|---|
| ID | UC003 |
| Name | Analyse Symptoms |
| Actor | System (AI Triage Service) |
| Related FR | FR-003 |

### Preconditions

1. Patient has submitted symptoms.
2. AI Triage Service is available.
3. CLINK system is operational.

### Normal Flow

| Step | Actor/System | Action |
|---|---|---|
| 1 | System | Retrieves submitted symptom data. |
| 2 | System | Sends data to AI triage service. |
| 3 | AI Triage Service | Analyses symptoms. |
| 4 | AI Triage Service | Returns analysis result. |
| 5 | System | Stores analysis result. |

### Alternative Flows

[Not explicitly stated in source for UC003 beyond TC003 test cases.]

### Exception Flows

**EF1: AI service times out**
1. System sends symptom data to AI service.
2. AI service fails to respond (timeout detected).
3. System handles timeout gracefully.
4. System displays error message: "Analysis failed, try again later."
5. No invalid data saved; system remains consistent.

### Postconditions

1. Analysis result stored in SymptomRecord.

---

**Table 2.1 Module Description for Analyse Symptoms (Exact)**

| Field | Description |
|---|---|
| Use Case ID | UC003 |
| Function | Analyse Symptoms |
| Description | Sends patient symptom data to the external AI Triage Service for analysis. |

---

## UC004 – Classify Urgency

### Use Case Overview

| Field | Description |
|---|---|
| ID | UC004 |
| Name | Classify Urgency |
| Actor | System (AI Triage Service) |
| Related FR | FR-004 |

### Preconditions

1. Symptoms have been submitted.
2. AI Triage Service is available.
3. CLINK system is operational.

### Normal Flow

| Step | Actor/System | Action |
|---|---|---|
| 1 | System | Sends symptom data to AI. |
| 2 | AI Triage Service | Returns urgency result. |
| 3 | System | Displays result to patient. |

### Alternative Flows

**AF1: Patient refreshes page**
1. Patient refreshes page.
2. System fetches updated urgency result.

### Exception Flows

**EF1: AI service unavailable**
1. AI service is unavailable.
2. System displays "Try Again Later."

**EF2: AI service fails to return urgency classification**
1. System attempts to retrieve urgency result.
2. AI result is unavailable.
3. Error detected; no urgency assigned.
4. System displays error message: "Unable to classify urgency."
5. Patient prompted to retry later; system remains stable.

### Postconditions

1. Urgency classification displayed.

---

**Table 2.4.3: User Story Description for Classify Urgency (Exact)**

| Field | Description |
|---|---|
| User Story ID | US003 |
| User Story Name | Classify Urgency |
| User Story Description | As a patient, I want the system to classify my condition as urgent or non-urgent, so that I can understand how quickly I need medical care. |
| Acceptance Criteria(s) | Precondition: Symptoms submitted. Postcondition: Urgency classification displayed. |
| Normal Flow(s) – NF | 1. System sends symptom data to AI. 2. AI returns urgency result. 3. System displays result to patient. |
| Alternative Flow(s) – AF | AF1: Patient refreshes page → system fetches updated urgency result. |
| Exception Flow(s) – EF | EF1: AI service unavailable → system displays "Try Again Later." |

---

## UC005 – Recommend Specialist

### Use Case Overview

| Field | Description |
|---|---|
| ID | UC005 |
| Name | Recommend Specialist |
| Actor | System |
| Related FR | FR-005 |

### Preconditions

1. Urgency classification is available.

### Normal Flow

| Step | Actor/System | Action |
|---|---|---|
| 1 | System | Evaluates symptom data and urgency level. |
| 2 | System | Identifies suitable specialist type. |
| 3 | System | Displays recommended specialist to patient. |

### Alternative Flows

**AF1: Multiple specialists available**
1. Multiple specialists are available.
2. System lists all suitable specialists.

### Exception Flows

**EF1: No specialist available**
1. No specialist available.
2. System displays notification to contact hospital support.

### Postconditions

1. Recommended specialist displayed.

---

**Table 2.4.5: User Story Description for Recommend Specialist (Exact)**

| Field | Description |
|---|---|
| User Story ID | US005 |
| User Story Name | Recommend Specialist |
| User Story Description | As a patient, I want the system to recommend an appropriate medical specialist based on my symptoms and urgency level, so that I can receive suitable medical care. |
| Acceptance Criteria(s) | Precondition: Urgency classification available. Postcondition: Recommended specialist displayed. |
| Normal Flow(s) – NF | 1. System evaluates symptom data and urgency level. 2. System identifies suitable specialist type. 3. System displays recommended specialist to patient. |
| Alternative Flow(s) – AF | AF1: Multiple specialists available → system lists all suitable specialists. |
| Exception Flow(s) – EF | EF1: No specialist available → system displays notification to contact hospital support. |

---

## UC006 – View Triage Result

### Use Case Overview

| Field | Description |
|---|---|
| ID | UC006 |
| Name | View Triage Result |
| Actor | Patient |
| Related FR | FR-006 |

### Preconditions

1. Symptoms submitted successfully.

### Normal Flow

| Step | Actor/System | Action |
|---|---|---|
| 1 | Patient | Submits symptoms. |
| 2 | System | Processes symptoms using AI triage service. |
| 3 | System | Retrieves urgency classification. |
| 4 | System | Displays urgency result to patient. |

### Alternative Flows

**AF1: Patient refreshes the page**
1. Patient refreshes the page.
2. System retrieves the latest urgency result.

### Exception Flows

**EF1: AI service unavailable**
1. AI service is unavailable.
2. System displays error message and prompts patient to retry later.

### Postconditions

1. Urgency level displayed to the patient.

---

**Table 2.4.6: User Story Description for View Triage Result (Exact)**

| Field | Description |
|---|---|
| User Story ID | US006 |
| User Story Name | View Triage Result |
| User Story Description | As a patient, I want to view the urgency level generated by the system, so that I can understand the seriousness of my condition and decide my next action. |
| Acceptance Criteria(s) | Precondition: Symptoms submitted successfully. Postcondition: Urgency level displayed to the patient. |
| Normal Flow(s) – NF | 1. Patient submits symptoms. 2. System processes symptoms using AI triage service. 3. System retrieves urgency classification. 4. System displays urgency result to patient. |
| Alternative Flow(s) – AF | AF1: Patient refreshes the page → system retrieves the latest urgency result. |
| Exception Flow(s) – EF | EF1: AI service unavailable → system displays error message and prompts patient to retry later. |

---

## UC007 – Book Appointment

### Use Case Overview

| Field | Description |
|---|---|
| ID | UC007 |
| Name | Book Appointment |
| Actor | Patient |
| Related FR | FR-007 |

### Preconditions

1. Triage completed.

### Normal Flow

| Step | Actor/System | Action |
|---|---|---|
| 1 | System | Displays recommended slots. |
| 2 | Patient | Selects slot. |
| 3 | System | Books appointment. |
| 4 | System | Confirms booking. |

### Alternative Flows

**AF1: Selected slot unavailable**
1. Selected slot is unavailable.
2. Patient chooses another slot.

### Exception Flows

**EF1: Database fails**
1. Database fails.
2. System prompts retry.

### Postconditions

1. Appointment booked.

---

**Table 2.4.4: User Story Description for Book Appointment (Exact)**

| Field | Description |
|---|---|
| User Story ID | US004 |
| User Story Name | Book Appointment |
| User Story Description | As a patient, I want to view and select recommended appointment slots provided by the system, so that I can book a suitable outpatient appointment. |
| Acceptance Criteria(s) | Precondition: Triage completed. Postcondition: Appointment booked. |
| Normal Flow(s) – NF | 1. System displays recommended slots. 2. Patient selects slot. 3. System books appointment. 4. System confirms booking. |
| Alternative Flow(s) – AF | AF1: Selected slot unavailable → patient chooses another slot. |
| Exception Flow(s) – EF | EF1: Database fails → system prompts retry. |

---

## UC008 – Receive Notifications

### Use Case Overview

| Field | Description |
|---|---|
| ID | UC008 |
| Name | Receive Notifications |
| Actor | Patient |
| Related FR | FR-008 |

### Preconditions

1. Appointment exists.

### Normal Flow

| Step | Actor/System | Action |
|---|---|---|
| 1 | System | Detects appointment or schedule change. |
| 2 | System | Generates notification. |
| 3 | System | Patient receives updated notification. |

### Alternative Flows

**AF1: Patient opens notifications later**
1. Patient opens notifications later.
2. System marks notification as unread until viewed.

### Exception Flows

**EF1: Notification delivery fails**
1. Notification delivery fails.
2. System logs error and retries automatically.

### Postconditions

1. Notification delivered and updated in real-time.

---

**Table 2.4.8: User Story Description for Receive / Update Notification (Exact)**

| Field | Description |
|---|---|
| User Story ID | US008 |
| User Story Name | Receive / Update Notification |
| User Story Description | As a patient, I want to receive notifications when my appointment status changes, so that I stay informed without manually checking the system. |
| Acceptance Criteria(s) | Precondition: Appointment exists. Postcondition: Notification delivered and updated in real-time. |
| Normal Flow(s) – NF | 1. System detects appointment or schedule change. 2. System generates notification. 3. Patient receives updated notification. |
| Alternative Flow(s) – AF | AF1: Patient opens notifications later → system marks notification as unread until viewed. |
| Exception Flow(s) – EF | EF1: Notification delivery fails → system logs error and retries automatically. |

---

## UC009 – View Patient Cases

### Use Case Overview

| Field | Description |
|---|---|
| ID | UC009 |
| Name | View Patient Cases |
| Actor | Doctor |
| Related FR | FR-009 |

### Preconditions

1. Doctor is logged in.

### Normal Flow

| Step | Actor/System | Action |
|---|---|---|
| 1 | Doctor | Opens dashboard. |
| 2 | System | Retrieves assigned patient cases. |
| 3 | System | Sorts cases by urgency. |
| 4 | Doctor | Reviews patient details and triage results. |

### Alternative Flows

**AF1: No cases assigned**
1. No cases are assigned.
2. System shows empty dashboard message.

### Exception Flows

**EF1: Database or server error**
1. Database or server error occurs.
2. System displays error message.

### Postconditions

1. Cases displayed in priority order with relevant urgency and details.

---

**Table 2.4.9: User Story Description for View Patient Cases (Exact)**

| Field | Description |
|---|---|
| User Story ID | US009 |
| User Story Name | View Patient Cases |
| User Story Description | As a doctor, I want to view a prioritised list of my assigned patient cases, so that I can attend to urgent patients first. |
| Acceptance Criteria(s) | Precondition: Doctor logged in. Postcondition: Cases displayed in priority order with relevant urgency and details. |
| Normal Flow(s) – NF | 1. Doctor opens dashboard. 2. System retrieves assigned patient cases. 3. System sorts cases by urgency. 4. Doctor reviews patient details and triage results. |
| Alternative Flow(s) – AF | AF1: No cases assigned → system shows empty dashboard message. |
| Exception Flow(s) – EF | EF1: Database or server error → system displays error message. |

---

## UC010 – Update Case Status

### Use Case Overview

| Field | Description |
|---|---|
| ID | UC010 |
| Name | Update Case Status |
| Actor | Doctor |
| Related FR | FR-010 |

### Preconditions

1. Patient case selected.

### Normal Flow

| Step | Actor/System | Action |
|---|---|---|
| 1 | Doctor | Selects case. |
| 2 | Doctor | Updates status/notes. |
| 3 | System | Saves updates. |

### Alternative Flows

**AF1: Doctor cancels update**
1. Doctor cancels update.
2. System discards changes.

### Exception Flows

**EF1: Database fails**
1. Database fails.
2. System shows error.

### Postconditions

1. Case updated.

---

**Table 2.4.10: User Story Description for Update Case Status (Exact)**

| Field | Description |
|---|---|
| User Story ID | US010 |
| User Story Name | Update Case Status |
| User Story Description | As a doctor, I want to update the status of patient cases, so that the system reflects accurate progress. |
| Acceptance Criteria(s) | Precondition: Patient case selected. Postcondition: Case updated. |
| Normal Flow(s) – NF | 1. Doctor selects case. 2. Updates status/notes. 3. System saves updates. |
| Alternative Flow(s) – AF | AF1: Doctor cancels update → system discards changes. |
| Exception Flow(s) – EF | EF1: Database fails → show error. |

---

## UC010b – Review AI Triage Results

### Use Case Overview

| Field | Description |
|---|---|
| ID | US007 (mapped to UC010 review function) |
| Name | Review AI Triage Results |
| Actor | Doctor |
| Related FR | FR-009, FR-010 |

### Preconditions

1. Patient cases assigned.

### Normal Flow

| Step | Actor/System | Action |
|---|---|---|
| 1 | Doctor | Selects patient case. |
| 2 | System | Displays symptoms and AI result. |
| 3 | Doctor | Reviews. |

### Alternative Flows

**AF1: AI results pending**
1. AI results are pending.
2. System shows "Pending."

### Exception Flows

**EF1: System fails**
1. System fails.
2. System shows error.

### Postconditions

1. AI results visible to doctor.

---

**Table 2.4.7: User Story Description for Review AI Triage Results (Exact)**

| Field | Description |
|---|---|
| User Story ID | US007 |
| User Story Name | Review AI Triage Results |
| User Story Description | As a doctor, I want to view patient symptoms and AI-generated triage results, so that I understand the patient's condition before consultation. |
| Acceptance Criteria(s) | Precondition: Patient cases assigned. Postcondition: AI results visible. |
| Normal Flow(s) – NF | 1. Doctor selects patient case. 2. System displays symptoms and AI result. 3. Doctor reviews. |
| Alternative Flow(s) – AF | AF1: AI results pending → system shows "Pending." |
| Exception Flow(s) – EF | System fails → show error. |

---

## UC011 – Manage Users

### Use Case Overview

| Field | Description |
|---|---|
| ID | UC011 |
| Name | Manage Users |
| Actor | Admin |
| Related FR | FR-011 |

### Preconditions

1. Admin is logged in.

### Normal Flow

| Step | Actor/System | Action |
|---|---|---|
| 1 | Admin | Opens user management module. |
| 2 | Admin | Selects add/update/delete. |
| 3 | System | Saves changes. |

### Alternative Flows

**AF1: Admin cancels**
1. Admin cancels.
2. System discards changes.

### Exception Flows

**EF1: Database error**
1. Database error occurs.
2. System shows error.

### Postconditions

1. Accounts updated.

---

**Table 2.4.11: User Story Description for Manage Users (Exact)**

| Field | Description |
|---|---|
| User Story ID | US011 |
| User Story Name | Manage Users |
| User Story Description | As an admin, I want to manage patient and doctor accounts, so that the system maintains accurate and secure access control. |
| Acceptance Criteria(s) | Precondition: Admin logged in. Postcondition: Accounts updated. |
| Normal Flow(s) – NF | 1. Admin opens user management module. 2. Admin selects add/update/delete. 3. System saves changes. |
| Alternative Flow(s) – AF | AF1: Admin cancels → system discards changes. |
| Exception Flow(s) – EF | EF1: Database error → show error. |

---

## UC012 – Configure Schedules

### Use Case Overview

| Field | Description |
|---|---|
| ID | UC012 |
| Name | Configure Schedules |
| Actor | Admin |
| Related FR | FR-012 |

### Preconditions

1. Admin is logged in.

### Normal Flow

| Step | Actor/System | Action |
|---|---|---|
| 1 | Admin | Opens schedule configuration. |
| 2 | Admin | Enters/updates availability. |
| 3 | System | Saves schedule. |

### Alternative Flows

**AF1: Admin cancels**
1. Admin cancels.
2. System discards changes.

### Exception Flows

**EF1: Database fails**
1. Database fails.
2. System shows error.

### Postconditions

1. Schedules saved.

---

**Table 2.4.12: User Story Description for Configure Schedules (Exact)**

| Field | Description |
|---|---|
| User Story ID | US012 |
| User Story Name | Configure Schedules |
| User Story Description | As an admin, I want to configure specialist schedules, so that the system can generate valid appointment slot recommendations. |
| Acceptance Criteria(s) | Precondition: Admin logged in. Postcondition: Schedules saved. |
| Normal Flow(s) – NF | 1. Admin opens schedule configuration. 2. Enters/updates availability. 3. System saves schedule. |
| Alternative Flow(s) – AF | AF1: Admin cancels → system discards changes. |
| Exception Flow(s) – EF | EF1: Database fails → show error. |

---

# 6. Traceability Matrix

## 6.1 FR → UC → TC Mapping (Exact — from STD Appendix A)

| FR ID | UC | TC | TC Sub-cases |
|---|---|---|---|
| FR-001 | UC001 – Register | TC001 | TC001_01, TC001_02 |
| FR-002 | UC002 – Submit Symptoms | TC002 | TC002_01, TC002_02 |
| FR-003 | UC003 – Analyse Symptoms | TC003 | TC003_01, TC003_02 |
| FR-004 | UC004 – Classify Urgency | TC004 | TC004_01, TC004_02 |
| FR-005 | UC005 – Recommend Specialist | TC005 | TC005_01 |
| FR-006 | UC006 – View Triage Result | TC006 | TC006_01 |
| FR-007 | UC007 – Book Appointment | TC007 | TC007_01, TC007_02 |
| FR-008 | UC008 – Receive Notifications | TC008 | TC008_01 |
| FR-009 | UC009 – View Patient Cases | TC009 | TC009_01, TC009_02 |
| FR-010 | UC010 – Update Case Status | TC010 | TC010_01, TC010_02 |
| FR-011 | UC011 – Manage Users | TC011 | TC011_01 |
| FR-012 | UC012 – Configure Schedules | TC012 | TC012_01 |

## 6.2 UC → Package Mapping (Exact — from STD Appendix A Traceability Matrix)

| UC | Subsystem Package | Sequence Diagram ID | Package ID |
|---|---|---|---|
| UC001 – Register | Patient Account Management Subsystem | SD001 | P001 |
| UC002 – Submit Symptoms | Patient Symptom Management Subsystem | SD002 | P002 |
| UC003 – Analyse Symptoms | Patient Symptom Management Subsystem | SD003 | P002 |
| UC004 – Classify Urgency | Patient Symptom Management Subsystem | SD004 | P002 |
| UC005 – Recommend Specialist | Patient Symptom Management Subsystem | SD005 | P002 |
| UC006 – View Triage Result | Patient Symptom Management Subsystem | SD006 | P002 |
| UC007 – Book Appointment | Appointment Management Subsystem | SD007 | P003 |
| UC008 – Receive Notifications | Notification Management Subsystem | SD008 | P004 |
| UC009 – View Patient Cases | Doctor Case Management Subsystem | SD009 | P005 |
| UC010 – Update Case Status | Doctor Case Management Subsystem | SD010 | P005 |
| UC011 – Manage Users | Administration Management Subsystem | SD011 | P006 |
| UC012 – Configure Schedules | Administration Management Subsystem | SD012 | P006 |

---

# 7. Constraints

- The system shall not provide medical diagnosis beyond urgency classification.
- The system shall not replace clinical decision-making by licensed healthcare professionals.
- The system shall not integrate with full Electronic Medical Record (EMR) systems at this stage.
- The system shall not support inpatient admissions or emergency care workflows.
- The system shall not integrate directly with medical devices.
- The system shall be compatible with Windows 10 and more recent browsers (Compatibility Constraint).
- The system shall require a minimum 8GB of RAM in computers and standard web browsers (Hardware Constraint).
- Any sensitive information shall be encrypted (Security Constraint).
- Role-based access control shall be implemented (Security Constraint).
- The system shall accommodate a minimum of 1000 simultaneous users with a response time of less than 5 seconds (Performance Constraint).
- The system shall be reliable in common hospital IT conditions (Environmental Constraint).
- The development duration of the system shall not exceed the allocated project timeline (NFR-014).
- The system shall not display any content that is offensive to any race, religion, or culture (NFR-012).

---

# 8. Assumptions

- The system is implemented as a web-based client–server application.
- AI-based triage supports decision-making but does not replace medical professionals.
- A single relational database is used for persistent data storage.
- External notification handling is performed through an automation workflow (n8n).
- The system does not integrate directly with medical devices.
- The AI model is trained using a publicly available healthcare dataset related to patient symptoms and clinical conditions, ensuring realistic symptom-based classification without using real patient data.
- The system is deployed initially on a local server (localhost) as a demonstration and testing system.
- Users will access the system through a standard modern web browser with a stable internet connection.
- Stakeholders (patients, doctors, and administrative staff) participated in survey-based requirements elicitation at Al-Jahra Hospital, Kuwait, in 2025, confirming the need for the system and expressing strong support for an AI-assisted solution.
