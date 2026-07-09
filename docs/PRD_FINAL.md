# PRD_FINAL.md

| Field | Value |
|---|---|
| **Document Name** | Product Requirements Document – CLINK Smart Outpatient Triage and Scheduling System |
| **Version** | 1.0 |
| **Date** | January 2026 (SRS dated 15/12/2025; SDS revision 01/01/2026) |
| **Status** | Initial Draft |
| **Source Reference** | CLINK – Smart Outpatient Triage and Scheduling System (FYP Report, UTM, January 2026); Appendix B: Software Requirements Specification (SRS) v1.0; Appendix C: Software Design Specification (SDS) v1.0; Appendix D: Software Test Documentation (STD) v1.0 |
| **Brief Explanation** | This PRD is derived exclusively from the CLINK FYP thesis and its embedded SRS, SDS, and STD appendices. It summarises product vision, problem, users, scope, features, constraints, technology, and hardware/software requirements as explicitly documented in the source. |

---

# 1. Product Vision

CLINK – Smart Outpatient Triage and Scheduling System is a web-based healthcare support system designed to improve patient management in outpatient departments (OPD). It applies artificial intelligence to examine patient symptoms, categorise the urgency of cases, automatically suggest the most suitable specialist, and perform automated appointment scheduling. CLINK aims to centralise and automate the triage and scheduling process, allow real-time tracking of patient flow and appointment updates, streamline outpatient service, reduce waiting times, enhance the accuracy of appointments, and improve overall patient satisfaction and staff efficiency.

---

# 2. Problem Statement

## 2.1 Core Problem

Many healthcare facilities continue to use manual processes for outpatient triage and appointment scheduling, causing:

- Long queues and excessive waiting times (patients at Al-Jahra Hospital, Kuwait, wait weeks or months for outpatient appointments).
- Uneven triage judgements and communication lapses due to manual, staff-dependent workflows.
- Patients frequently not knowing which specialist or department they require, leading to misdirected bookings.
- Overcrowding of emergency departments (EDs) with non-emergency patients seeking referrals or directions.
- High administrative burden on doctors and staff in triangulating referrals, resolving scheduling confusion, and manual follow-up.
- 61% of surveyed patients rated the appointment process as poor or very poor; 67% did not know the specialty they required; 56% visited the ED simply to determine which clinic to attend.
- 63% of surveyed doctors encountered 1–3 misdirected patients daily; 74% had difficulty determining case urgency; 58% felt administrative delays harmed timely patient care.

## 2.2 Identified Gap

Existing digital outpatient systems in the region (Al-Razi Hospital, Al-Orf Hospital, Qmed Asia, Pantai Hospital) offer only basic appointment booking. None provide:

- AI-based symptom analysis to guide patients to the correct specialist.
- Automatic urgency classification (urgent vs. non-urgent).
- Automated specialist recommendation based on symptoms.
- Doctor dashboard with AI-based prioritisation of cases.
- Workflow automation for notifications and scheduling updates.
- Integration with a simple AI diagnostic support feature.

---

# 3. Target Users

## 3.1 Primary Users

**Patients**
- Need accurate triage guidance, understanding of symptom urgency, and efficient outpatient appointment scheduling.
- User stories: register account, submit symptoms, view urgency classification, book appointment, receive notifications.

## 3.2 Secondary Users

**Doctors / Medical Staff**
- Need an easy-to-use interface for triage and scheduling, fast retrieval of patient information, and accurate AI recommendations.
- User stories: view prioritised patient cases, review AI triage results, update case status.

## 3.3 Administrative Staff (Admin)

- Need to manage users, configure schedules, and maintain smooth operation of outpatient workflows.
- User stories: manage patient and doctor accounts, configure specialist schedules.

**Supporting Actor: AI Triage Service (External Actor)**
- An external AI-based service that analyses patient symptom data and returns urgency classification and specialist recommendations. Human involvement is reduced given it addresses a straightforward classification issue.

---

# 4. Scope

## 4.1 In Scope

The scope of this project focuses on designing and developing a smart outpatient triage and scheduling system that includes:

- Registration and login option of a patient.
- Urgency analysis and symptom analysis with the help of AI.
- An easy diagnostic characteristic to identify the priority of the appointment (urgent or normal).
- Autonomous specialist and appointment slot suggestions.
- Doctor dashboard to see, administer and give priority to patients' cases.
- Simple automation tools used to automate notification and workflow.

System capabilities (from SRS):
- Accept patient registration and login.
- Collect and process symptom descriptions.
- Use AI to classify symptoms and determine urgency.
- Recommend the appropriate specialist automatically.
- Suggest suitable appointment slots based on urgency.
- Provide doctors with a dashboard to review, manage, and prioritise cases.
- Automate notifications to patients and healthcare staff via workflow tools.

## 4.2 Out of Scope

The system will not:

- Provide medical diagnosis beyond urgency classification.
- Replace clinical decision-making by licensed healthcare professionals.
- Integrate with full Electronic Medical Record (EMR) systems at this stage.
- Support inpatient admissions or emergency care workflows.

STD additionally excludes from testing scope:
- Performance testing.
- Security penetration testing.
- Medical accuracy validation of AI models.
- Deployment or infrastructure testing.

## 4.3 Language / Platform Scope

- System user interfaces shall be displayed in English and Arabic (NFR-011).
- The system shall be developed as a web-based application accessible via a standard web browser (NFR-013).

---

# 5. Feature Breakdown (Mapped to FR)

## 5.1 Core Features

| Feature | FR ID | Use Case |
|---|---|---|
| Patient Registration | FR-001 | UC001 – Register |
| Submit Symptoms | FR-002 | UC002 – Submit Symptoms |
| AI Symptom Analysis | FR-003 | UC003 – Analyse Symptoms |
| Urgency Classification | FR-004 | UC004 – Classify Urgency |
| Specialist Recommendation | FR-005 | UC005 – Recommend Specialist |
| View Triage Result | FR-006 | UC006 – View Triage Result |
| Book Appointment | FR-007 | UC007 – Book Appointment |
| Automated Notifications | FR-008 | UC008 – Receive Notifications |
| View Patient Cases (Doctor) | FR-009 | UC009 – View Patient Cases |
| Update Case Status (Doctor) | FR-010 | UC010 – Update Case Status |
| Manage Users (Admin) | FR-011 | UC011 – Manage Users |
| Configure Schedules (Admin) | FR-012 | UC012 – Configure Schedules |

### Feature Descriptions (from Table 4.2.1 / SRS)

| FR ID | Description |
|---|---|
| FR-001 | The system enables patients to create an account to have access to the system. |
| FR-002 | The system enables patients to enter the information on the symptoms to be triaged. |
| FR-003 | The system forwards the symptom data uploaded to the AI Triage Service to be analysed. |
| FR-004 | The system categorises patient conditions as urgent or nonurgent according to the analysis of AI. |
| FR-005 | The system suggests a doctor specialist depending on the analysed symptoms. |
| FR-006 | The system enables the patients to see the result of the triage and specialist recommendations. |
| FR-007 | The system enables patients to make an outpatient appointment with slots recommended. |
| FR-008 | The system will provide automated messages concerning appointment and case updates. |
| FR-009 | The system enables the doctors to see and prioritise the assigned cases of patients. |
| FR-010 | The system enables doctors to update the status of the cases of patients and their consultations. |
| FR-011 | The system enables administrators to deal with patient and doctor user accounts. |
| FR-012 | The system enables administrators to set schedules and availability of specialists. |

## 5.2 Dashboard & Visualisation

- Doctor Dashboard: displays a prioritised list of assigned patient cases based on urgency level; allows viewing of symptom records and AI triage results; supports updating case status and adding consultation notes; provides visual indicators such as urgency labels and status tags.
- Admin Dashboard: supports user management (add, update, deactivate users); allows management of doctor schedules and system configurations; provides system summaries and logs.
- Patient Interface: allows registration and login; provides symptom submission forms with guided input fields; displays AI-generated urgency level and appointment status; allows appointment booking and viewing of notifications.

---

# 6. System Constraints

## 6.1 Design Constraints

- The system should be reliable in common hospital IT conditions (Environmental Constraints).
- The system shall not display any content that is offensive to any race, religion, or culture (NFR-012).
- The development duration of the system shall not exceed the allocated project timeline (NFR-014).
- The system is implemented as a web-based client–server application.
- AI-based triage supports decision-making but does not replace medical professionals.
- A single relational database is used for persistent data storage.
- External notification handling is performed through an automation workflow (Internal Simulated Email Notification).
- The system does not integrate directly with medical devices.

## 6.2 Capacity Constraints

- The system shall support multiple concurrent users without degradation (Throughput).
- The system shall handle increasing patient and doctor accounts (Capacity).
- The system should be able to accommodate a minimum of 1000 simultaneous users (Performance Constraint).
- A response time of less than 5 seconds (Performance Constraint).
- Hardware minimum: 8GB RAM in computers and normal web browsers (Hardware Constraint).

## 6.3 Security Expectations

- Any sensitive information should be encrypted (Security Constraint).
- Role-based access control shall be implemented.
- The system shall restrict access to functionalities based on user roles (patient, doctor, admin) (NFR-019).
- The system functionalities shall be accessible only to authenticated users (NFR-015).
- The system should be able to run with Windows 10 and more recent browsers (Compatibility Constraint).
- Compliance with healthcare data protection regulations required.

---

# 7. Technology Stack

## 7.1 System Technologies

| Component | Technology | Purpose |
|---|---|---|
| Backend Language | Python | AI-based symptom analysis, urgency classifier, server-side code, data processing |
| Front-end | HTML, CSS, JavaScript | Web-based user interface, responsive designs, interactive features |
| AI Classification | Python with scikit-learn (Decision Tree), pandas, NumPy | AI Triage analyzes dynamic symptoms, clinical descriptions, precautions, and assigns dynamic urgency based on severity weights from CSV datasets. |
| Workflow Automation | Internal Database-backed Notification System | Internal notifications and simulated email delivery for appointments and schedule updates |
| Version Control | GitHub | Code management, secure storage, version control |
| IDE | Visual Studio Code | Write, debug, and maintain backend and frontend code |
| UI Design Tool | Figma | User interface prototyping for patient and doctor dashboards |
| Architecture Pattern | Client–Server with Clean Architecture and CQRS (Command and Query Responsibility Segregation) | Scalability, maintainability, separation of concerns |
| Data Management | CRUD (Create, Read, Update, Delete) | Managing patient records, appointments, and doctor schedules |
| Network | Local server (localhost) with API links between backend and Internal Simulated Email Notification | Secure communication and automated workflow execution |
| Authentication | Role-based access control with user authentication | Patient data security and healthcare compliance |

## 7.2 External Software Interfaces (Exact from SDS)

| Name | Mnemonic | Version | Source |
|---|---|---|---|
| Web Browser | N/A | Latest | Chrome, Firefox, Edge |
| Relational Database System | RDBMS | MySQL / PostgreSQL | Open-source |
| Workflow Automation Tool | Internal Simulated Email Notification | Latest stable | Open-source |
| Operating System | OS | Platform-independent | Windows / Linux |

---

# 8. Hardware Requirements (Exact Table)

| Hardware | Specification | Justification |
|---|---|---|
| Laptop / PC | Standard laptop | Used in system development, testing, AI processing, frontend design, backend development, and workflow automation. |

*Note: The system requires a minimum of 8GB of RAM in computers and standard web browsers (from SRS Design Constraints). Supported hardware includes desktop and laptop computers, tablets and smartphones, and standard input devices (keyboard, mouse, touch screen).*

---

# 9. Software Requirements (Exact Table)

| Software Type | Software Name | Description |
|---|---|---|
| IDE | Visual Studio Code | Used to write, debug, and maintain backend and frontend code such as Python and HTML and CSS and JavaScript. |
| Programming Language | Python | The primary high-level programming language to be used as a backend in AI-based symptom analysis, urgency classifier, server-side code, and data processing. |
| Web Technologies | HTML, CSS, JavaScript | Utilised in the creation of the web-based user interface, organisation of application pages, development of responsive designs, and interactive features. |
| Version Control | GitHub | Code management, secure storage of project repository, version control. |
| Workflow Automation | Internal Simulated Email Notification | Used to automate workflows to notify about appointments, urgency notifications, and updates on schedules. |
| UI Design Tool | Figma | Experience in creating user interface prototypes on patient and doctor dashboard implemented. |

---

# 10. Risks

[Not explicitly stated in source document as a dedicated Risks section. Survey findings suggest implementation risk factors including: AI triage service unavailability, database failures, and ED overcrowding as operational precursors to the need for the system. Future improvements noted include EMR integration, patient flow analytics, and mobile application support.]

---

# 11. Success Criteria

[Not explicitly stated in source document as a dedicated Success Criteria section. Project objectives from Chapter 1 imply the following success measures:]

- Functional and non-functional requirements of an AI-based outpatient triage and scheduling system are identified and defined.
- System architecture, database structure, and workflow for a web-based outpatient triage and scheduling application are designed.
- A web-based outpatient triage and scheduling system is developed, integrated with an AI-based model for symptom analysis, urgency classification, basic diagnostic assistance, and automated appointment scheduling with appropriate specialists.
- The system's accuracy, usability, and effectiveness in reducing patient waiting time and improving appointment management are evaluated.
