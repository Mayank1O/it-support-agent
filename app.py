from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

from services.decision_engine import process_request


app = Flask(__name__)

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


# ==================================================
# JSON FILE HELPERS
# ==================================================

def load_json(filename):

    path = os.path.join(
        BASE_DIR,
        "data",
        filename
    )

    if not os.path.exists(path):
        return []

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def save_json(filename, data):

    path = os.path.join(
        BASE_DIR,
        "data",
        filename
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


# ==================================================
# AUDIT TRAIL
# ==================================================

def create_audit_event(
    event,
    details,
    request_id=None,
    ticket_id=None
):

    audit_log = load_json(
        "audit_log.json"
    )

    event_data = {

        "timestamp":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

        "event":
            event,

        "details":
            details
    }

    if request_id:
        event_data["request_id"] = request_id

    if ticket_id:
        event_data["ticket_id"] = ticket_id

    audit_log.append(
        event_data
    )

    save_json(
        "audit_log.json",
        audit_log
    )

    return event_data


# ==================================================
# REQUEST ID GENERATOR
# ==================================================

def generate_request_id(requests):

    highest_number = 0

    for item in requests:

        request_id = item.get(
            "id",
            ""
        )

        if request_id.startswith("REQ-"):

            try:

                number = int(
                    request_id.replace(
                        "REQ-",
                        ""
                    )
                )

                if number > highest_number:
                    highest_number = number

            except ValueError:
                pass

    return "REQ-" + str(
        highest_number + 1
    )


# ==================================================
# TICKET ID GENERATOR
# ==================================================

def generate_ticket_id(tickets):

    highest_number = 1051

    for ticket in tickets:

        ticket_id = ticket.get(
            "id",
            ""
        )

        if ticket_id.startswith("TK-"):

            try:

                number = int(
                    ticket_id.replace(
                        "TK-",
                        ""
                    )
                )

                if number > highest_number:
                    highest_number = number

            except ValueError:
                pass

    return "TK-" + str(
        highest_number + 1
    )


# ==================================================
# SHOULD CREATE TICKET
# ==================================================

def should_create_ticket(
    decision,
    needs_clarification=False
):

    # VERY IMPORTANT:
    # A request waiting for clarification
    # must NEVER create a ticket.
    if needs_clarification:
        return False

    ticket_decisions = [

        "ROUTE_TO_IT",

        "ROUTE_TO_IT_FINANCE",

        "ROUTE_TO_FINANCE",

        "SECURITY_REVIEW",

        "REQUIRES_APPROVAL",

        "TROUBLESHOOT",

        "ESCALATE",

        "HUMAN_REVIEW"
    ]

    return decision in ticket_decisions


# ==================================================
# HOME PAGE
# ==================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ==================================================
# PROCESS NEW REQUEST
# ==================================================

@app.route(
    "/api/process",
    methods=["POST"]
)
def process():

    data = request.get_json()

    # --------------------------------------------------
    # VALIDATE REQUEST
    # --------------------------------------------------

    if not data or "request" not in data:

        return jsonify({
            "error":
                "Request text is required"
        }), 400

    user_request = data[
        "request"
    ].strip()

    if not user_request:

        return jsonify({
            "error":
                "Request cannot be empty"
        }), 400

    employee = data.get(
        "employee",
        "Demo Employee"
    )

    # --------------------------------------------------
    # LOAD REQUEST HISTORY
    # --------------------------------------------------

    employee_requests = load_json(
        "employee_requests.json"
    )

    request_id = generate_request_id(
        employee_requests
    )

    # --------------------------------------------------
    # AUDIT: REQUEST RECEIVED
    # --------------------------------------------------

    create_audit_event(

        "Request received",

        "Employee submitted a new IT support request.",

        request_id=request_id
    )

    # --------------------------------------------------
    # ANALYZE REQUEST
    # --------------------------------------------------

    result = process_request(
        user_request
    )

    # ==================================================
    # CLARIFICATION SAFETY CHECK
    # ==================================================
    #
    # If decision_engine says that more information
    # is required, clarification ALWAYS wins.
    #
    # This prevents:
    #
    # needs_clarification = True
    # decision = ROUTE_TO_IT
    #
    # from accidentally creating a ticket.
    # ==================================================

    if result.get(
        "needs_clarification",
        False
    ):

        result["decision"] = "CLARIFICATION"

        result["status"] = (
            "More information required"
        )

        result["assigned_team"] = (
            "IT Support"
        )

        if not result.get(
            "follow_up_question"
        ):

            result["follow_up_question"] = (
                "Please provide more information "
                "about the issue."
            )

        if not result.get(
            "follow_up_options"
        ):

            result["follow_up_options"] = []

    # --------------------------------------------------
    # AUDIT: CLASSIFICATION
    # --------------------------------------------------

    create_audit_event(

        "Issue classified",

        (
            "Request classified as "
            + str(result["category"])
            + " with "
            + str(
                round(
                    result["confidence"] * 100,
                    1
                )
            )
            + "% confidence."
        ),

        request_id=request_id
    )

    # --------------------------------------------------
    # AUDIT: KNOWLEDGE BASE SEARCH
    # --------------------------------------------------

    if result.get("source"):

        source = result["source"]

        create_audit_event(

            "Knowledge base searched",

            (
                "Matched "
                + source["title"]
                + " ("
                + source["id"]
                + ")."
            ),

            request_id=request_id
        )

    else:

        create_audit_event(

            "Knowledge base searched",

            "No sufficiently relevant knowledge base article was found.",

            request_id=request_id
        )

    # --------------------------------------------------
    # AUDIT: DECISION
    # --------------------------------------------------

    create_audit_event(

        "Decision generated",

        (
            result["decision"]
            + " — "
            + result["status"]
        ),

        request_id=request_id
    )

    # --------------------------------------------------
    # CREATE EMPLOYEE REQUEST RECORD
    # --------------------------------------------------

    initial_action = result["status"]

    if result.get(
        "needs_clarification",
        False
    ):

        initial_action = (
            "Follow-up required — "
            + (
                result.get(
                    "follow_up_question"
                )
                or
                "More information required."
            )
        )

    elif result["decision"] == "SELF_SERVICE":

        initial_action = (
            "Resolved through self-service"
        )

    elif result["decision"] in [
        "ESCALATE",
        "HUMAN_REVIEW"
    ]:

        initial_action = (
            "Escalated — "
            + result["assigned_team"]
        )

    request_record = {

        "id":
            request_id,

        "employee":
            employee,

        "email":
            data.get(
                "email",
                ""
            ),

        "date":
            datetime.now().strftime(
                "%a %d %b"
            ),

        "request":
            user_request,

        "initial_action":
            initial_action
    }

    employee_requests.append(
        request_record
    )

    save_json(
        "employee_requests.json",
        employee_requests
    )

    # --------------------------------------------------
    # TICKET CREATION
    # --------------------------------------------------

    ticket_id = None

    ticket_status = None

    create_ticket = should_create_ticket(

        result["decision"],

        result.get(
            "needs_clarification",
            False
        )
    )

    if create_ticket:

        tickets = load_json(
            "tickets.json"
        )

        ticket_id = generate_ticket_id(
            tickets
        )

        ticket_status = "Open"

        new_ticket = {

            "id":
                ticket_id,

            "employee":
                employee,

            "issue":
                user_request,

            "status":
                ticket_status,

            "active":
                True,

            "priority":
                result["priority"],

            "assigned_team":
                result["assigned_team"],

            "category":
                result["category"],

            "decision":
                result["decision"],

            "request_id":
                request_id
        }

        tickets.append(
            new_ticket
        )

        save_json(
            "tickets.json",
            tickets
        )

        # ----------------------------------------------
        # AUDIT: TICKET CREATED
        # ----------------------------------------------

        create_audit_event(

            "Ticket created",

            (
                "Structured ticket created and assigned to "
                + result["assigned_team"]
                + "."
            ),

            request_id=request_id,

            ticket_id=ticket_id
        )

        # ----------------------------------------------
        # UPDATE REQUEST ACTION
        # ----------------------------------------------

        request_record[
            "initial_action"
        ] = (

            "Ticket created: "
            + ticket_id
            + " — "
            + result["assigned_team"]
        )

        if result["decision"] == "ESCALATE":

            request_record[
                "initial_action"
            ] = (

                "Escalated to Security — "
                + ticket_id
            )

        save_json(
            "employee_requests.json",
            employee_requests
        )

    else:

        # ------------------------------------------------
        # NO TICKET
        # ------------------------------------------------

        if result.get(
            "needs_clarification",
            False
        ):

            create_audit_event(

                "Follow-up requested",

                (
                    result.get(
                        "follow_up_question"
                    )
                    or
                    "Additional information required."
                ),

                request_id=request_id
            )

        elif result["decision"] == "SELF_SERVICE":

            create_audit_event(

                "Request resolved",

                "Request resolved through self-service guidance.",

                request_id=request_id
            )

    # --------------------------------------------------
    # ADD INFORMATION TO RESPONSE
    # --------------------------------------------------

    result["request_id"] = request_id

    result["ticket_id"] = ticket_id

    result["ticket_status"] = ticket_status

    # --------------------------------------------------
    # RETURN RESULT
    # --------------------------------------------------

    return jsonify(
        result
    )


# ==================================================
# GET EMPLOYEE REQUESTS
# ==================================================

@app.route(
    "/api/requests"
)
def get_requests():

    requests = load_json(
        "employee_requests.json"
    )

    return jsonify(
        requests
    )


# ==================================================
# GET ALL TICKETS
# ==================================================

@app.route(
    "/api/tickets"
)
def get_tickets():

    tickets = load_json(
        "tickets.json"
    )

    return jsonify(
        tickets
    )


# ==================================================
# GET AUDIT TRAIL
# ==================================================

@app.route(
    "/api/audit"
)
def get_audit():

    audit_log = load_json(
        "audit_log.json"
    )

    return jsonify(
        audit_log
    )


# ==================================================
# GET AUDIT TRAIL FOR REQUEST
# ==================================================

@app.route(
    "/api/audit/<request_id>"
)
def get_request_audit(request_id):

    audit_log = load_json(
        "audit_log.json"
    )

    request_events = []

    for event in audit_log:

        if event.get(
            "request_id"
        ) == request_id:

            request_events.append(
                event
            )

    return jsonify(
        request_events
    )


# ==================================================
# UPDATE TICKET STATUS
# ==================================================

@app.route(
    "/api/tickets/<ticket_id>/status",
    methods=["PUT"]
)
def update_ticket_status(
    ticket_id
):

    data = request.get_json()

    if not data or "status" not in data:

        return jsonify({
            "error":
                "Status is required"
        }), 400

    new_status = data[
        "status"
    ]

    allowed_statuses = [

        "Open",

        "In Progress",

        "Resolved"
    ]

    if new_status not in allowed_statuses:

        return jsonify({
            "error":
                "Invalid ticket status"
        }), 400

    tickets = load_json(
        "tickets.json"
    )

    for ticket in tickets:

        if ticket["id"] == ticket_id:

            old_status = ticket.get(
                "status",
                "Open"
            )

            ticket["status"] = new_status

            if new_status == "Resolved":

                ticket["active"] = False

            else:

                ticket["active"] = True

            save_json(
                "tickets.json",
                tickets
            )

            create_audit_event(

                "Ticket status updated",

                (
                    "Ticket status changed from "
                    + old_status
                    + " to "
                    + new_status
                    + "."
                ),

                request_id=ticket.get(
                    "request_id"
                ),

                ticket_id=ticket_id
            )

            return jsonify({

                "message":
                    "Ticket status updated successfully",

                "ticket":
                    ticket

            })

    return jsonify({
        "error":
            "Ticket not found"
    }), 404


# ==================================================
# DASHBOARD
# ==================================================

@app.route(
    "/api/dashboard"
)
def dashboard():

    requests = load_json(
        "employee_requests.json"
    )

    tickets = load_json(
        "tickets.json"
    )

    audit_log = load_json(
        "audit_log.json"
    )

    # --------------------------------------------------
    # ACTIVE TICKETS
    # --------------------------------------------------

    active_tickets = 0

    for ticket in tickets:

        if ticket.get(
            "active",
            False
        ):

            active_tickets += 1

    # --------------------------------------------------
    # SECURITY CASES
    # --------------------------------------------------

    security_cases = 0

    security_keywords = [

        "phishing",

        "malware",

        "unauthorized access",

        "security",

        "hacked"
    ]

    for item in requests:

        text = item.get(
            "request",
            ""
        ).lower()

        for keyword in security_keywords:

            if keyword in text:

                security_cases += 1

                break

    # --------------------------------------------------
    # ESCALATED CASES
    # --------------------------------------------------

    escalated_cases = 0

    for ticket in tickets:

        if ticket.get(
            "decision"
        ) in [
            "ESCALATE",
            "HUMAN_REVIEW"
        ]:

            escalated_cases += 1

    # --------------------------------------------------
    # SELF-SERVICE CASES
    # --------------------------------------------------

    self_service_cases = 0

    for event in audit_log:

        if event.get(
            "event"
        ) == "Request resolved":

            self_service_cases += 1

    return jsonify({

        "total_requests":
            len(requests),

        "total_tickets":
            len(tickets),

        "active_tickets":
            active_tickets,

        "security_cases":
            security_cases,

        "escalated_cases":
            escalated_cases,

        "self_service_cases":
            self_service_cases,

        "audit_events":
            len(audit_log),

        "requests":
            requests

    })


# ==================================================
# RUN APPLICATION
# ==================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )