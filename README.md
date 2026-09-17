# Veridian IT Support Agent

## Internal Service Agent for IT Support

A web-based internal IT support agent developed as an academic prototype. The system helps employees report IT issues, identifies the type of request, searches the relevant knowledge base, provides policy-based guidance, asks follow-up questions when information is insufficient, and escalates requests that require human intervention.

---

## Project Objective

The objective of this project is to develop an internal IT support system that can:

* Understand employee IT issues
* Classify IT support requests
* Find relevant IT policies and knowledge-base articles
* Provide appropriate resolutions for common issues
* Ask sensible follow-up questions when the request is unclear
* Escalate sensitive, risky, or approval-based requests
* Create structured IT support tickets
* Display the source used for the response
* Maintain an audit trail of requests and actions
* Provide an IT support dashboard

---

## Key Features

### 1. IT Request Analysis

Employees can enter their IT-related problem in natural language.

Example:

> My laptop is not turning on.

The system analyzes the request and identifies the relevant category and resolution.

### 2. Knowledge Base Search

The system searches the internal IT knowledge base using:

* TF-IDF
* Cosine similarity

The most relevant knowledge-base article is selected as the source for the response.

### 3. Follow-up Questions

If an employee provides insufficient information, the system asks a relevant follow-up question.

Example:

> My laptop has a problem.

The system asks what type of laptop problem the employee is experiencing.

### 4. Automated Resolution

Simple IT issues can receive direct guidance without requiring manual intervention.

Examples:

* Password reset
* Guest Wi-Fi access
* Printer troubleshooting
* Mailbox storage issues

### 5. Escalation

Requests involving security, administrative access, approval, or unclear situations can be escalated to the appropriate team.

Examples:

* Phishing/security incidents
* Administrative access requests
* Non-catalog software
* Contractor VPN access

### 6. Ticket Creation

Requests requiring IT intervention can automatically generate a structured support ticket containing information such as:

* Ticket ID
* Request ID
* Category
* Priority
* Status
* Assigned team
* Recommended action

### 7. Source Display

The system displays the knowledge-base source used to generate the recommendation, including the article title and similarity score.

### 8. Audit Trail

Important actions are recorded in an audit log so that the handling of requests can be reviewed.

### 9. IT Dashboard

The dashboard provides an overview of:

* Total requests
* Total tickets
* Active tickets
* Security cases
* Escalated cases
* Self-service cases
* Audit events
* Administrative access requests

---

## Technology Stack

### Backend

* Python
* Flask

### Machine Learning / NLP

* Scikit-learn
* TF-IDF Vectorization
* Cosine Similarity

### Frontend

* HTML
* CSS
* JavaScript

### Data Storage

* JSON

---

## Project Structure

```text
veridian-it-support/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── services/
│   ├── __init__.py
│   ├── decision_engine.py
│   ├── classifier.py
│   ├── knowledge_search.py
│   └── policy_engine.py
│
├── data/
│   ├── employee_requests.json
│   ├── knowledge_base.json
│   ├── policies.json
│   ├── tickets.json
│   └── audit_log.json
│
├── templates/
│   └── index.html
│
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── app.js
```

---

# Installation and Setup

## Prerequisites

Make sure the following are installed:

* Python 3.9 or higher
* Git
* A modern web browser

---

## 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Move into the project directory:

```bash
cd veridian-it-support
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run the Application

```bash
python app.py
```

The Flask server will start locally.

Open the following address in your browser:

```text
http://127.0.0.1:5000
```

---

# Example Test Cases

The following requests can be used to test the system.

### Password Issue

```text
I forgot my password.
```

Expected behavior:

* Identify password-related issue
* Provide password reset guidance
* Use the relevant knowledge-base article

---

### Account Lockout

```text
My account is locked after 6 failed attempts.
```

Expected behavior:

* Identify account lockout
* Recognize that manual IT intervention is required
* Create/escalate an IT ticket

---

### Laptop Issue

```text
My laptop has a problem.
```

Expected behavior:

* Ask a follow-up question
* Display laptop problem options
* Wait for additional information before creating a ticket

---

### VPN Issue

```text
My VPN is not connecting.
```

Expected behavior:

* Identify VPN issue
* Search the VPN knowledge base
* Provide the appropriate resolution or escalation

---

### Security Incident

```text
I received a phishing email.
```

Expected behavior:

* Identify the request as a security incident
* Escalate to the appropriate security team
* Provide the security reporting instructions
* Record the action in the audit trail

---

### Administrative Access

```text
I urgently need admin access to the finance reporting server.
```

Expected behavior:

* Identify the request as administrative access
* Require appropriate approval
* Route the request to the relevant security/approval team

---

# System Workflow

```text
Employee Request
       │
       ▼
Request Analysis
       │
       ▼
Category Detection
       │
       ▼
Knowledge Base Search
       │
       ▼
Policy / Resolution Analysis
       │
       ├───────────────┐
       │               │
       ▼               ▼
Simple Request     Unclear Request
       │               │
       ▼               ▼
Resolution       Follow-up Question
       │               │
       └───────┬───────┘
               ▼
        Decision Engine
               │
       ┌───────┼────────┐
       ▼       ▼        ▼
    Resolve  Ticket   Escalate
       │       │        │
       └───────┼────────┘
               ▼
          Audit Trail
```

---

# Main Components

### `app.py`

Flask application responsible for:

* Web routes
* API endpoints
* Request processing
* Ticket creation
* Audit logging
* Dashboard data

### `decision_engine.py`

Responsible for:

* Request analysis
* Category detection
* Priority detection
* Follow-up questions
* Resolution decisions
* Escalation decisions

### `knowledge_search.py`

Uses TF-IDF and cosine similarity to identify the most relevant knowledge-base article.

### `classifier.py`

Handles IT request classification.

### `policy_engine.py`

Handles policy-related decision logic.

### `data/`

Contains the prototype's knowledge base, policies, employee requests, tickets, and audit information.

### `templates/`

Contains the main web interface.

### `static/`

Contains frontend CSS and JavaScript.

---

# Academic Scope

This project is developed as a functional prototype for academic demonstration. It uses JSON files as the data layer rather than a production database and uses a local Flask server for deployment.

The system demonstrates the concepts of:

* Natural language request handling
* NLP-based knowledge retrieval
* Decision-based automation
* Human escalation
* IT ticket management
* Policy-aware support
* Audit logging

---

# Future Enhancements

Possible future improvements include:

* Integration with a relational database
* Authentication and role-based access
* Integration with enterprise ticketing systems
* More advanced NLP models
* Semantic/vector database search
* Email and notification integration
* Real-time administrator dashboard
* Deployment on a cloud platform
* Integration with enterprise identity management

---

## Author

**Mayank Dalal**

B.Tech – Artificial Intelligence & Machine Learning
The NorthCap University

---

## Project Status

**Functional Prototype – Academic Project**
