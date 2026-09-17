// ==================================================
// GLOBAL VARIABLES
// ==================================================

let lastRequestText = "";


// ==================================================
// SUBMIT REQUEST
// ==================================================

async function submitRequest(textOverride = null) {

    const requestText = document.getElementById("requestText");
    const submitBtn = document.getElementById("submitBtn");
    const loading = document.getElementById("loading");
    const result = document.getElementById("result");

    const text = textOverride !== null
        ? textOverride.trim()
        : requestText.value.trim();


    if (!text) {

        alert("Please describe your IT issue.");

        return;
    }


    lastRequestText = text;


    // Show loading state

    submitBtn.disabled = true;
    submitBtn.textContent = "Analyzing...";

    loading.classList.remove("hidden");
    result.classList.add("hidden");


    try {

        const response = await fetch(
            "/api/process",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    request: text,

                    employee: "Demo Employee",

                    email: ""
                })
            }
        );


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.error || "Unable to process request."
            );
        }


        displayResult(data);


        // Refresh data in the background

        loadRequests();
        loadTickets();
        loadAdminDashboard();

    }
    catch (error) {

        console.error(error);

        alert(
            error.message ||
            "Something went wrong while processing the request."
        );

    }
    finally {

        submitBtn.disabled = false;

        submitBtn.textContent =
            "Analyze Request";

        loading.classList.add("hidden");
    }
}


// ==================================================
// DISPLAY RESULT
// ==================================================

function displayResult(data) {

    const result = document.getElementById("result");

    result.classList.remove("hidden");


    // --------------------------------------------------
    // REQUEST ID
    // --------------------------------------------------

    setText(
        "requestId",
        data.request_id || "—"
    );


    // --------------------------------------------------
    // RESULT STATUS
    // --------------------------------------------------

    setText(
        "resultStatus",
        data.status || "Request analyzed"
    );


    // --------------------------------------------------
    // PRIORITY
    // --------------------------------------------------

    const priorityBadge =
        document.getElementById("priorityBadge");


    priorityBadge.textContent =
        data.priority || "MEDIUM";


    priorityBadge.className =
        "priority-badge " +
        getPriorityClass(data.priority);


    // --------------------------------------------------
    // MAIN RESULT INFORMATION
    // --------------------------------------------------

    setText(
        "category",
        data.category || "—"
    );


    setText(
        "confidence",
        formatConfidence(data.confidence)
    );


    setText(
        "decision",
        formatDecision(data.decision)
    );


    setText(
        "assignedTeam",
        data.assigned_team || "—"
    );


    setText(
        "status",
        data.status || "—"
    );


    setText(
        "resolutionType",
        formatResolutionType(data.resolution_type)
    );


    // --------------------------------------------------
    // REASON
    // --------------------------------------------------

    setText(
        "reason",
        data.reason || "No additional reason provided."
    );


    // --------------------------------------------------
    // RECOMMENDED ACTION
    // --------------------------------------------------

    setText(
        "recommendedAction",
        data.recommended_action ||
        "No recommended action available."
    );


    // --------------------------------------------------
    // FOLLOW-UP
    // --------------------------------------------------

    displayFollowUp(data);


    // --------------------------------------------------
    // ESCALATION
    // --------------------------------------------------

    displayEscalation(data);


    // --------------------------------------------------
    // SOURCE
    // --------------------------------------------------

    displaySource(data);


    // --------------------------------------------------
    // POLICY
    // --------------------------------------------------

    displayPolicy(data);


    // --------------------------------------------------
    // RELATED TICKETS
    // --------------------------------------------------

    displayRelatedTickets(
        data.related_tickets
    );


    // --------------------------------------------------
    // TICKET
    // --------------------------------------------------

    displayTicket(data);


    // --------------------------------------------------
    // AUDIT TRAIL
    // --------------------------------------------------

    if (data.request_id) {

        loadAuditTrail(
            data.request_id
        );
    }


    // Scroll to result

    result.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}


// ==================================================
// FOLLOW-UP SECTION
// ==================================================

function displayFollowUp(data) {

    const section =
        document.getElementById("followUpSection");

    const question =
        document.getElementById("followUpQuestion");

    const optionsContainer =
        document.getElementById("followUpOptions");


    optionsContainer.innerHTML = "";


    if (
        !data.needs_clarification ||
        !data.follow_up_question
    ) {

        section.classList.add("hidden");

        return;
    }


    section.classList.remove("hidden");


    setText(
        "followUpQuestion",
        data.follow_up_question
    );


    const options =
        data.follow_up_options || [];


    for (let i = 0; i < options.length; i++) {

        const button =
            document.createElement("button");


        button.type = "button";

        button.className =
            "follow-up-option";


        button.textContent =
            options[i];


        button.addEventListener(
            "click",
            function () {

                continueWithFollowUp(
                    options[i]
                );

            }
        );


        optionsContainer.appendChild(
            button
        );
    }
}


// ==================================================
// CONTINUE WITH FOLLOW-UP OPTION
// ==================================================

function continueWithFollowUp(answer) {

    const combinedRequest =
        lastRequestText +
        " Additional information: " +
        answer;


    document.getElementById(
        "requestText"
    ).value = combinedRequest;


    submitRequest(
        combinedRequest
    );
}


// ==================================================
// CUSTOM FOLLOW-UP ANSWER
// ==================================================

function submitFollowUp() {

    const input =
        document.getElementById("followUpInput");


    const answer =
        input.value.trim();


    if (!answer) {

        alert(
            "Please provide the requested information."
        );

        return;
    }


    const combinedRequest =
        lastRequestText +
        " Additional information: " +
        answer;


    document.getElementById(
        "requestText"
    ).value = combinedRequest;


    input.value = "";


    submitRequest(
        combinedRequest
    );
}


// ==================================================
// ESCALATION
// ==================================================

function displayEscalation(data) {

    const section =
        document.getElementById(
            "escalationSection"
        );


    const reason =
        document.getElementById(
            "escalationReason"
        );


    if (
        data.escalation_reason &&
        (
            data.decision === "ESCALATE" ||
            data.decision === "HUMAN_REVIEW" ||
            data.decision === "SECURITY_REVIEW" ||
            data.decision === "REQUIRES_APPROVAL"
        )
    ) {

        section.classList.remove("hidden");


        setText(
            "escalationReason",
            data.escalation_reason
        );

    }
    else {

        section.classList.add("hidden");

        setText(
            "escalationReason",
            "—"
        );
    }
}


// ==================================================
// SOURCE
// ==================================================

function displaySource(data) {

    const source =
        data.source;


    const sourceCard =
        document.getElementById(
            "sourceUsed"
        );


    const noSource =
        document.getElementById(
            "noSource"
        );


    if (!source) {

        sourceCard.classList.add(
            "hidden"
        );

        noSource.classList.remove(
            "hidden"
        );

        setText(
            "sourceType",
            "—"
        );

        setText(
            "sourceTitle",
            "—"
        );

        setText(
            "sourceId",
            "—"
        );

        setText(
            "sourceCategory",
            "—"
        );

        setText(
            "sourceSimilarity",
            "—"
        );

        return;
    }


    sourceCard.classList.remove(
        "hidden"
    );

    noSource.classList.add(
        "hidden"
    );


    setText(
        "sourceType",
        source.type || "Knowledge Base"
    );


    setText(
        "sourceTitle",
        source.title || "—"
    );


    setText(
        "sourceId",
        source.id || "—"
    );


    setText(
        "sourceCategory",
        source.category || "—"
    );


    if (
        source.similarity !== undefined &&
        source.similarity !== null
    ) {

        setText(
            "sourceSimilarity",
            source.similarity
        );

    }
    else {

        setText(
            "sourceSimilarity",
            "—"
        );
    }
}


// ==================================================
// POLICY
// ==================================================

function displayPolicy(data) {

    setText(
        "policy",
        data.policy?.title ||
        "No specific policy matched"
    );


    const governingPolicy =
        data.governing_policy;


    if (governingPolicy) {

        setText(
            "governingPolicy",
            governingPolicy.policy ||
            governingPolicy.title ||
            "—"
        );


        setText(
            "governingPolicySectionText",
            governingPolicy.title ||
            governingPolicy.id ||
            "—"
        );

    }
    else {

        setText(
            "governingPolicy",
            "No additional governing policy identified."
        );


        setText(
            "governingPolicySectionText",
            "—"
        );
    }
}


// ==================================================
// RELATED TICKETS
// ==================================================

function displayRelatedTickets(tickets) {

    const container =
        document.getElementById(
            "relatedTickets"
        );


    container.innerHTML = "";


    if (
        !tickets ||
        tickets.length === 0
    ) {

        const empty =
            document.createElement("div");


        empty.className =
            "related-empty";


        empty.textContent =
            "No related tickets found.";


        container.appendChild(
            empty
        );


        return;
    }


    for (
        let i = 0;
        i < tickets.length;
        i++
    ) {

        const ticket =
            tickets[i];


        const card =
            document.createElement("div");


        card.className =
            "related-ticket";


        const title =
            document.createElement("strong");


        title.textContent =
            ticket.id || "Ticket";


        const details =
            document.createElement("span");


        details.textContent =
            (
                ticket.status ||
                "Unknown status"
            ) +
            " — " +
            (
                ticket.issue ||
                "No issue description"
            );


        card.appendChild(title);

        card.appendChild(details);


        container.appendChild(card);
    }
}


// ==================================================
// DISPLAY CREATED TICKET
// ==================================================

function displayTicket(data) {

    const ticketInfo =
        document.getElementById(
            "ticketInfo"
        );


    if (data.ticket_id) {

        ticketInfo.classList.remove(
            "hidden"
        );


        setText(
            "ticketId",
            data.ticket_id
        );


        setText(
            "ticketStatus",
            data.ticket_status ||
            "Open"
        );

    }
    else {

        ticketInfo.classList.add(
            "hidden"
        );


        setText(
            "ticketId",
            "—"
        );


        setText(
            "ticketStatus",
            "—"
        );
    }
}


// ==================================================
// AUDIT TRAIL
// ==================================================

async function loadAuditTrail(requestId) {

    const container =
        document.getElementById(
            "auditTrail"
        );


    container.innerHTML = "";


    if (!requestId) {

        showAuditEmpty(
            "No request ID available."
        );

        return;
    }


    try {

        const response =
            await fetch(
                "/api/audit/" +
                encodeURIComponent(requestId)
            );


        const auditEvents =
            await response.json();


        if (
            !response.ok ||
            !Array.isArray(auditEvents) ||
            auditEvents.length === 0
        ) {

            showAuditEmpty(
                "No audit events available."
            );

            return;
        }


        for (
            let i = 0;
            i < auditEvents.length;
            i++
        ) {

            const event =
                auditEvents[i];


            const item =
                document.createElement("div");


            item.className =
                "audit-item";


            const marker =
                document.createElement("div");


            marker.className =
                "audit-marker";


            const content =
                document.createElement("div");


            content.className =
                "audit-content";


            const eventName =
                document.createElement("strong");


            eventName.textContent =
                event.event ||
                "System event";


            const details =
                document.createElement("p");


            details.textContent =
                event.details ||
                "No details available.";


            const timestamp =
                document.createElement("span");


            timestamp.className =
                "audit-time";


            timestamp.textContent =
                event.timestamp ||
                "Unknown time";


            content.appendChild(
                eventName
            );

            content.appendChild(
                details
            );

            content.appendChild(
                timestamp
            );


            item.appendChild(
                marker
            );

            item.appendChild(
                content
            );


            container.appendChild(
                item
            );
        }

    }
    catch (error) {

        console.error(
            "Audit trail error:",
            error
        );


        showAuditEmpty(
            "Unable to load audit trail."
        );
    }
}


// ==================================================
// AUDIT EMPTY STATE
// ==================================================

function showAuditEmpty(message) {

    const container =
        document.getElementById(
            "auditTrail"
        );


    container.innerHTML = "";


    const empty =
        document.createElement("div");


    empty.className =
        "audit-empty";


    empty.textContent =
        message;


    container.appendChild(
        empty
    );
}


// ==================================================
// EXAMPLE REQUEST
// ==================================================

function setExample(text) {

    const requestText =
        document.getElementById(
            "requestText"
        );


    requestText.value =
        text;


    requestText.focus();
}


// ==================================================
// PAGE NAVIGATION
// ==================================================

function showPage(pageId, clickedButton) {

    const pages =
        document.querySelectorAll(
            ".page"
        );


    for (let i = 0; i < pages.length; i++) {

        pages[i].classList.add(
            "hidden"
        );

        pages[i].classList.remove(
            "active-page"
        );
    }


    const selectedPage =
        document.getElementById(
            pageId
        );


    if (selectedPage) {

        selectedPage.classList.remove(
            "hidden"
        );

        selectedPage.classList.add(
            "active-page"
        );
    }


    const navItems =
        document.querySelectorAll(
            ".nav-item"
        );


    for (
        let i = 0;
        i < navItems.length;
        i++
    ) {

        navItems[i].classList.remove(
            "active"
        );
    }


    if (clickedButton) {

        clickedButton.classList.add(
            "active"
        );
    }


    // Load relevant page data

    if (pageId === "requestsPage") {

        loadRequests();
    }


    if (pageId === "ticketsPage") {

        loadTickets();
    }


    if (pageId === "dashboardPage") {

        loadAdminDashboard();
    }
}


// ==================================================
// LOAD REQUESTS
// ==================================================

async function loadRequests() {

    const table =
        document.getElementById(
            "requestsTable"
        );


    try {

        const response =
            await fetch(
                "/api/requests"
            );


        const requests =
            await response.json();


        table.innerHTML = "";


        if (
            !Array.isArray(requests) ||
            requests.length === 0
        ) {

            addTableMessage(
                table,
                5,
                "No requests found."
            );

            return;
        }


        for (
            let i = requests.length - 1;
            i >= 0;
            i--
        ) {

            const item =
                requests[i];


            const row =
                document.createElement("tr");


            addCell(
                row,
                item.id || "—"
            );


            addCell(
                row,
                item.employee || "—"
            );


            addCell(
                row,
                item.date || "—"
            );


            addCell(
                row,
                item.request || "—"
            );


            addCell(
                row,
                item.initial_action || "—"
            );


            table.appendChild(row);
        }

    }
    catch (error) {

        console.error(error);

        addTableMessage(
            table,
            5,
            "Unable to load requests."
        );
    }
}


// ==================================================
// LOAD TICKETS
// ==================================================

async function loadTickets() {

    const table =
        document.getElementById(
            "ticketsTable"
        );


    try {

        const response =
            await fetch(
                "/api/tickets"
            );


        const tickets =
            await response.json();


        table.innerHTML = "";


        if (
            !Array.isArray(tickets) ||
            tickets.length === 0
        ) {

            addTableMessage(
                table,
                7,
                "No tickets found."
            );

            return;
        }


        for (
            let i = tickets.length - 1;
            i >= 0;
            i--
        ) {

            const ticket =
                tickets[i];


            const row =
                document.createElement("tr");


            addCell(
                row,
                ticket.id || "—"
            );


            addCell(
                row,
                ticket.employee || "—"
            );


            addCell(
                row,
                ticket.category || "—"
            );


            const priorityCell =
                document.createElement("td");


            const priority =
                document.createElement("span");


            priority.className =
                "priority-badge " +
                getPriorityClass(
                    ticket.priority
                );


            priority.textContent =
                ticket.priority || "MEDIUM";


            priorityCell.appendChild(
                priority
            );


            row.appendChild(
                priorityCell
            );


            addCell(
                row,
                ticket.assigned_team || "—"
            );


            addCell(
                row,
                ticket.issue || "—"
            );


            // Status dropdown

            const statusCell =
                document.createElement("td");


            const select =
                document.createElement("select");


            select.className =
                "status-select";


            const allowedStatuses = [

                "Open",

                "In Progress",

                "Resolved"
            ];


            const currentStatus =
                ticket.status || "Open";


            // If old data contains a status that
            // is not in the current dropdown,
            // preserve it visually.

            if (
                !allowedStatuses.includes(
                    currentStatus
                )
            ) {

                const oldOption =
                    document.createElement(
                        "option"
                    );


                oldOption.value =
                    currentStatus;


                oldOption.textContent =
                    currentStatus;


                oldOption.selected =
                    true;


                select.appendChild(
                    oldOption
                );
            }


            for (
                let j = 0;
                j < allowedStatuses.length;
                j++
            ) {

                const option =
                    document.createElement(
                        "option"
                    );


                option.value =
                    allowedStatuses[j];


                option.textContent =
                    allowedStatuses[j];


                if (
                    allowedStatuses[j] ===
                    currentStatus
                ) {

                    option.selected =
                        true;
                }


                select.appendChild(
                    option
                );
            }


            select.addEventListener(
                "change",
                function () {

                    updateTicketStatus(
                        ticket.id,
                        select.value
                    );

                }
            );


            statusCell.appendChild(
                select
            );


            row.appendChild(
                statusCell
            );


            table.appendChild(row);
        }

    }
    catch (error) {

        console.error(error);

        addTableMessage(
            table,
            7,
            "Unable to load tickets."
        );
    }
}


// ==================================================
// UPDATE TICKET STATUS
// ==================================================

async function updateTicketStatus(
    ticketId,
    newStatus
) {

    try {

        const response =
            await fetch(
                "/api/tickets/" +
                encodeURIComponent(ticketId) +
                "/status",
                {
                    method: "PUT",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        status: newStatus
                    })
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.error ||
                "Unable to update ticket."
            );
        }


        loadTickets();

        loadAdminDashboard();


        // If this ticket belongs to the
        // currently displayed request,
        // refresh its audit trail.

        if (
            data.ticket &&
            data.ticket.request_id
        ) {

            loadAuditTrail(
                data.ticket.request_id
            );
        }

    }
    catch (error) {

        console.error(error);

        alert(
            error.message ||
            "Unable to update ticket status."
        );


        loadTickets();
    }
}


// ==================================================
// LOAD DASHBOARD
// ==================================================

async function loadAdminDashboard() {

    try {

        const response =
            await fetch(
                "/api/dashboard"
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.error ||
                "Unable to load dashboard."
            );
        }


        setText(
            "totalRequests",
            data.total_requests ?? 0
        );


        setText(
            "totalTickets",
            data.total_tickets ?? 0
        );


        setText(
            "activeTickets",
            data.active_tickets ?? 0
        );


        setText(
            "securityCases",
            data.security_cases ?? 0
        );


        setText(
            "escalatedCases",
            data.escalated_cases ?? 0
        );


        setText(
            "selfServiceCases",
            data.self_service_cases ?? 0
        );


        setText(
            "auditEvents",
            data.audit_events ?? 0
        );


        displayDashboardRequests(
            data.requests || []
        );

    }
    catch (error) {

        console.error(
            "Dashboard error:",
            error
        );
    }
}


// ==================================================
// DASHBOARD REQUEST TABLE
// ==================================================

function displayDashboardRequests(
    requests
) {

    const table =
        document.getElementById(
            "adminRequestsTable"
        );


    table.innerHTML = "";


    if (
        !Array.isArray(requests) ||
        requests.length === 0
    ) {

        addTableMessage(
            table,
            4,
            "No requests found."
        );

        return;
    }


    let start =
        requests.length - 1;


    let end =
        Math.max(
            -1,
            requests.length - 11
        );


    for (
        let i = start;
        i > end;
        i--
    ) {

        const item =
            requests[i];


        const row =
            document.createElement("tr");


        addCell(
            row,
            item.id || "—"
        );


        addCell(
            row,
            item.employee || "—"
        );


        addCell(
            row,
            item.request || "—"
        );


        addCell(
            row,
            item.initial_action || "—"
        );


        table.appendChild(row);
    }
}


// ==================================================
// SIDEBAR TOGGLE
// ==================================================

function toggleSidebar() {

    const app =
        document.getElementById("app");


    const toggle =
        document.getElementById(
            "sidebarToggle"
        );


    app.classList.toggle(
        "sidebar-closed"
    );


    if (
        app.classList.contains(
            "sidebar-closed"
        )
    ) {

        toggle.textContent = "☰";

    }
    else {

        toggle.textContent = "×";
    }
}


// ==================================================
// HELPER: SET TEXT SAFELY
// ==================================================

function setText(
    elementId,
    value
) {

    const element =
        document.getElementById(
            elementId
        );


    if (!element) {

        return;
    }


    element.textContent =
        value === null ||
        value === undefined ||
        value === ""
            ? "—"
            : value;
}


// ==================================================
// HELPER: ADD TABLE CELL
// ==================================================

function addCell(
    row,
    value
) {

    const cell =
        document.createElement("td");


    cell.textContent =
        value === null ||
        value === undefined ||
        value === ""
            ? "—"
            : value;


    row.appendChild(
        cell
    );
}


// ==================================================
// HELPER: TABLE EMPTY MESSAGE
// ==================================================

function addTableMessage(
    table,
    colspan,
    message
) {

    const row =
        document.createElement("tr");


    const cell =
        document.createElement("td");


    cell.colSpan =
        colspan;


    cell.textContent =
        message;


    row.appendChild(
        cell
    );


    table.appendChild(
        row
    );
}


// ==================================================
// HELPER: CONFIDENCE
// ==================================================

function formatConfidence(
    confidence
) {

    if (
        confidence === null ||
        confidence === undefined
    ) {

        return "—";
    }


    const number =
        Number(confidence);


    if (Number.isNaN(number)) {

        return confidence;
    }


    return (
        number * 100
    ).toFixed(1) + "%";
}


// ==================================================
// HELPER: DECISION LABEL
// ==================================================

function formatDecision(
    decision
) {

    if (!decision) {

        return "—";
    }


    const labels = {

        "SELF_SERVICE":
            "Self Service",

        "ROUTE_TO_IT":
            "Route to IT",

        "ROUTE_TO_IT_FINANCE":
            "Route to IT + Finance",

        "ROUTE_TO_FINANCE":
            "Route to Finance",

        "SECURITY_REVIEW":
            "Security Review",

        "REQUIRES_APPROVAL":
            "Requires Approval",

        "TROUBLESHOOT":
            "Troubleshooting",

        "ESCALATE":
            "Escalate",

        "HUMAN_REVIEW":
            "Human Review",

        "CLARIFICATION":
            "Clarification Required"
    };


    return (
        labels[decision] ||
        decision
    );
}


// ==================================================
// HELPER: RESOLUTION TYPE
// ==================================================

function formatResolutionType(
    resolutionType
) {

    if (!resolutionType) {

        return "Pending";
    }


    const labels = {

        "SELF_SERVICE":
            "Self Service",

        "ROUTED":
            "Routed",

        "CLARIFICATION":
            "Clarification",

        "PENDING":
            "Pending"
    };


    return (
        labels[resolutionType] ||
        resolutionType
    );
}


// ==================================================
// HELPER: PRIORITY CLASS
// ==================================================

function getPriorityClass(
    priority
) {

    if (!priority) {

        return "";
    }


    return (
        "priority-" +
        priority.toLowerCase()
    );
}


// ==================================================
// INITIAL PAGE LOAD
// ==================================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        loadRequests();

        loadTickets();

        loadAdminDashboard();

    }
);