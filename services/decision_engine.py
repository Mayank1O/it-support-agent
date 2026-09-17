import re

from services.knowledge_search import search_knowledge_base


def detect_priority(text):
    text_lower = text.lower()

    high_words = [
        "security",
        "phishing",
        "malware",
        "hacked",
        "unauthorized",
        "admin access",
        "administrator access",
        "urgent",
        "critical"
    ]

    medium_words = [
        "vpn",
        "password",
        "locked",
        "laptop",
        "email",
        "printer",
        "software"
    ]

    for word in high_words:
        if word in text_lower:
            return "HIGH"

    for word in medium_words:
        if word in text_lower:
            return "MEDIUM"

    return "LOW"


def extract_failed_attempts(text):
    patterns = [
        r"(\d+)\s*(?:failed|unsuccessful)\s*(?:login|logins|attempt|attempts)",
        r"(\d+)\s*(?:wrong|incorrect)\s*(?:password|passwords|attempt|attempts)",
        r"after\s+(\d+)\s*(?:failed|unsuccessful)\s*(?:attempt|attempts)"
    ]

    for pattern in patterns:
        match = re.search(pattern, text.lower())

        if match:
            return int(match.group(1))

    return None


def get_follow_up_question(text):
    text_lower = text.lower()

    # ---------------------------------------------------------
    # LAPTOP
    # ---------------------------------------------------------
    laptop_words = [
        "laptop",
        "computer",
        "pc",
        "notebook"
    ]

    if any(word in text_lower for word in laptop_words):

        specific_laptop_words = [
            "not turning on",
            "won't turn on",
            "wont turn on",
            "doesn't turn on",
            "doesnt turn on",
            "dead",
            "flickering",
            "screen",
            "display",
            "battery",
            "charging",
            "charger",
            "overheating",
            "slow",
            "freezing",
            "hang",
            "hardware",
            "keyboard",
            "touchpad",
            "broken",
            "damaged",
            "blue screen",
            "crashing"
        ]

        if not any(word in text_lower for word in specific_laptop_words):
            return (
                "What problem are you experiencing with the laptop?",
                [
                    "Laptop is not turning on",
                    "Laptop is running slowly",
                    "Screen or display problem",
                    "Battery or charging problem",
                    "Other hardware problem"
                ]
            )

    # ---------------------------------------------------------
    # PRINTER
    # ---------------------------------------------------------
    printer_words = [
        "printer",
        "printing",
        "print"
    ]

    if any(word in text_lower for word in printer_words):

        specific_printer_words = [
            "paper jam",
            "jammed",
            "paper stuck",
            "not printing",
            "won't print",
            "wont print",
            "doesn't print",
            "doesnt print",
            "offline",
            "spooler",
            "queue",
            "error",
            "ink",
            "toner"
        ]

        if not any(word in text_lower for word in specific_printer_words):
            return (
                "What problem are you experiencing with the printer?",
                [
                    "Paper jam",
                    "Printer is not printing",
                    "Printer shows offline",
                    "Printer queue is stuck",
                    "Other printer problem"
                ]
            )

    # ---------------------------------------------------------
    # VPN
    # ---------------------------------------------------------
    vpn_words = [
        "vpn",
        "virtual private network"
    ]

    if any(word in text_lower for word in vpn_words):

        specific_vpn_words = [
            "credential",
            "credentials",
            "expired",
            "password expired",
            "access",
            "contractor",
            "connection failed",
            "connection failure",
            "cannot connect",
            "can't connect",
            "cant connect",
            "unable to connect",
            "login failed",
            "authentication",
            "approval"
        ]

        if not any(word in text_lower for word in specific_vpn_words):
            return (
                "What problem are you experiencing with VPN?",
                [
                    "VPN is not connecting",
                    "VPN credentials have expired",
                    "I need VPN access",
                    "I am a contractor and need VPN access",
                    "Other VPN problem"
                ]
            )

    # ---------------------------------------------------------
    # PASSWORD / ACCOUNT
    # ---------------------------------------------------------
    password_words = [
        "password",
        "login",
        "sign in",
        "signin",
        "account"
    ]

    if any(word in text_lower for word in password_words):

        specific_password_words = [
            "forgot",
            "forgotten",
            "reset",
            "locked",
            "lockout",
            "locked out",
            "failed attempt",
            "failed attempts",
            "wrong password",
            "incorrect password",
            "cannot login",
            "can't login",
            "cant login",
            "unable to login",
            "cannot sign in",
            "can't sign in",
            "cant sign in"
        ]

        if not any(
            word in text_lower
            for word in specific_password_words
        ):
            return (
                "What problem are you experiencing with your account or password?",
                [
                    "I forgot my password",
                    "My account is locked",
                    "My password is not working",
                    "I cannot sign in",
                    "Other account problem"
                ]
            )

    # ---------------------------------------------------------
    # EMAIL
    # ---------------------------------------------------------
    email_words = [
        "email",
        "mailbox",
        "outlook",
        "mail"
    ]

    if any(word in text_lower for word in email_words):

        specific_email_words = [
            "full",
            "quota",
            "storage",
            "space",
            "cannot send",
            "can't send",
            "cant send",
            "cannot receive",
            "can't receive",
            "cant receive",
            "not receiving",
            "not sending",
            "send email",
            "receive email"
        ]

        if not any(
            word in text_lower
            for word in specific_email_words
        ):
            return (
                "What problem are you experiencing with your email?",
                [
                    "My mailbox is full",
                    "I cannot send emails",
                    "I cannot receive emails",
                    "I have an email storage problem",
                    "Other email problem"
                ]
            )

    # ---------------------------------------------------------
    # SOFTWARE
    # ---------------------------------------------------------
    software_words = [
        "software",
        "application",
        "application",
        "program",
        "tool",
        "app",
        "install",
        "installation"
    ]

    if any(word in text_lower for word in software_words):

        specific_software_words = [
            "install",
            "installation",
            "uninstall",
            "not opening",
            "won't open",
            "wont open",
            "doesn't open",
            "doesnt open",
            "not working",
            "license",
            "licensed",
            "catalog",
            "non-catalog",
            "non catalog",
            "permission",
            "access"
        ]

        # Generic software/app problem
        if not any(
            word in text_lower
            for word in specific_software_words
        ):
            return (
                "What problem are you experiencing with the software?",
                [
                    "I need software installed",
                    "Software is not opening",
                    "Software is not working",
                    "I need access to software",
                    "Other software problem"
                ]
            )

    # ---------------------------------------------------------
    # SECURITY
    # ---------------------------------------------------------
    security_words = [
        "phishing",
        "malware",
        "virus",
        "hacked",
        "unauthorized access",
        "security incident",
        "suspicious email"
    ]

    if any(word in text_lower for word in security_words):
        return None

    return None


def detect_category(text):
    text_lower = text.lower()

    if any(
        word in text_lower
        for word in [
            "phishing",
            "malware",
            "virus",
            "hacked",
            "unauthorized access",
            "security incident",
            "suspicious email"
        ]
    ):
        return "Security"

    if any(
        word in text_lower
        for word in [
            "admin access",
            "administrator access",
            "admin privileges",
            "administrator privileges"
        ]
    ):
        return "Access"

    if any(
        word in text_lower
        for word in [
            "vpn",
            "virtual private network"
        ]
    ):
        return "VPN"

    if any(
        word in text_lower
        for word in [
            "password",
            "login",
            "sign in",
            "signin",
            "locked out",
            "account locked"
        ]
    ):
        return "Password"

    if any(
        word in text_lower
        for word in [
            "laptop",
            "computer",
            "pc",
            "notebook",
            "screen",
            "display",
            "battery"
        ]
    ):
        return "Laptop"

    if any(
        word in text_lower
        for word in [
            "printer",
            "printing",
            "print",
            "paper jam"
        ]
    ):
        return "Printer"

    if any(
        word in text_lower
        for word in [
            "email",
            "mailbox",
            "outlook",
            "mail"
        ]
    ):
        return "Email"

    if any(
        word in text_lower
        for word in [
            "software",
            "application",
            "program",
            "tool",
            "app",
            "install",
            "installation"
        ]
    ):
        return "Software"

    if any(
        word in text_lower
        for word in [
            "wifi",
            "wi-fi",
            "wireless",
            "guest network"
        ]
    ):
        return "Network"

    return "General IT"


def calculate_confidence(
    category,
    source_score,
    needs_clarification=False
):
    if needs_clarification:
        return round(
            min(0.60, 0.35 + source_score),
            2
        )

    base_scores = {
        "Security": 0.85,
        "Access": 0.80,
        "VPN": 0.75,
        "Password": 0.80,
        "Laptop": 0.75,
        "Printer": 0.75,
        "Email": 0.75,
        "Software": 0.70,
        "Network": 0.70,
        "General IT": 0.45
    }

    base = base_scores.get(category, 0.45)

    confidence = base + (source_score * 0.20)

    return round(min(confidence, 0.98), 2)


def process_request(text):
    text = text.strip()
    text_lower = text.lower()

    category = detect_category(text)

    priority = detect_priority(text)

    source, source_score = search_knowledge_base(text)

    source_title = None
    source_id = None
    policy = None
    recommended_action = None

    if source:
        source_title = source.get("title")
        source_id = source.get("id")
        policy = source.get("policy")
        recommended_action = source.get("action")

    # ---------------------------------------------------------
    # FOLLOW-UP CHECK
    # ---------------------------------------------------------
    initial_follow_up = get_follow_up_question(text)

    follow_up_question = None
    follow_up_options = []
    needs_clarification = False

    if initial_follow_up is not None:
        follow_up_question = initial_follow_up[0]
        follow_up_options = initial_follow_up[1]
        needs_clarification = True

    decision = "ROUTE_TO_IT"
    status = "Open"
    assigned_team = "IT Support"
    escalation_reason = None
    resolution_type = "Ticket"

    # ---------------------------------------------------------
    # SECURITY
    # ---------------------------------------------------------
    security_words = [
        "phishing",
        "malware",
        "virus",
        "hacked",
        "unauthorized access",
        "security incident",
        "suspicious email"
    ]

    if any(word in text_lower for word in security_words):

        decision = "SECURITY_REVIEW"
        status = "Escalated to Security"
        assigned_team = "IT Security"
        escalation_reason = (
            "The request may involve a security incident "
            "and requires immediate security review."
        )
        resolution_type = "Security Escalation"
        needs_clarification = False
        follow_up_question = None
        follow_up_options = []

    # ---------------------------------------------------------
    # ADMIN ACCESS
    # ---------------------------------------------------------
    elif any(
        word in text_lower
        for word in [
            "admin access",
            "administrator access",
            "admin privileges",
            "administrator privileges"
        ]
    ):

        decision = "REQUIRES_APPROVAL"
        status = "Administrative access approval required"
        assigned_team = "IT Security"
        escalation_reason = (
            "Administrative privileges require appropriate "
            "security and authorization review."
        )
        resolution_type = "Approval Required"
        needs_clarification = False
        follow_up_question = None
        follow_up_options = []

    # ---------------------------------------------------------
    # PASSWORD
    # ---------------------------------------------------------
    elif category == "Password":

        attempts = extract_failed_attempts(text)

        if attempts is not None and attempts >= 5:
            decision = "ROUTE_TO_IT"
            status = "Account unlock required"
            assigned_team = "IT Support"
            recommended_action = (
                "IT Support should manually unlock the account "
                "after verifying the employee."
            )
            resolution_type = "IT Intervention"

        elif (
            "locked" in text_lower
            or "locked out" in text_lower
            or "lockout" in text_lower
        ):
            decision = "ROUTE_TO_IT"
            status = "Account unlock required"
            assigned_team = "IT Support"
            recommended_action = (
                "IT Support should verify the employee and "
                "unlock the account."
            )
            resolution_type = "IT Intervention"

        elif (
            "forgot" in text_lower
            or "reset" in text_lower
        ):
            decision = "SELF_SERVICE"
            status = "Self-service password reset"
            assigned_team = "IT Support"
            recommended_action = (
                "Use the company's self-service password reset "
                "process."
            )
            resolution_type = "Self Service"

    # ---------------------------------------------------------
    # VPN
    # ---------------------------------------------------------
    elif category == "VPN":

        if "contractor" in text_lower:
            decision = "REQUIRES_APPROVAL"
            status = "VPN approval required"
            assigned_team = "IT Support"
            escalation_reason = (
                "Contractor VPN access requires manager approval."
            )
            recommended_action = (
                "Obtain manager approval before VPN access "
                "can be provisioned."
            )
            resolution_type = "Approval Required"

        elif (
            "expired" in text_lower
            or "credential" in text_lower
        ):
            decision = "ROUTE_TO_IT"
            status = "VPN credential support required"
            assigned_team = "IT Support"
            recommended_action = (
                "IT Support should verify the account and "
                "assist with VPN credential renewal."
            )
            resolution_type = "IT Intervention"

        elif "access" in text_lower:
            decision = "ROUTE_TO_IT"
            status = "VPN access request"
            assigned_team = "IT Support"
            recommended_action = (
                "IT Support should verify VPN eligibility "
                "and provision access if approved."
            )
            resolution_type = "Ticket"

        elif (
            "not connecting" in text_lower
            or "cannot connect" in text_lower
            or "can't connect" in text_lower
            or "cant connect" in text_lower
            or "connection failed" in text_lower
        ):
            decision = "TROUBLESHOOT"
            status = "VPN troubleshooting required"
            assigned_team = "IT Support"
            recommended_action = (
                "IT Support should troubleshoot the VPN "
                "connection."
            )
            resolution_type = "Troubleshooting"

    # ---------------------------------------------------------
    # LAPTOP
    # ---------------------------------------------------------
    elif category == "Laptop":

        if (
            "not turning on" in text_lower
            or "won't turn on" in text_lower
            or "wont turn on" in text_lower
            or "doesn't turn on" in text_lower
            or "doesnt turn on" in text_lower
            or "dead" in text_lower
        ):
            decision = "ROUTE_TO_IT"
            status = "Laptop hardware support required"
            assigned_team = "IT Support"
            recommended_action = (
                "IT Support should diagnose the laptop "
                "hardware issue and determine whether repair "
                "or replacement is required."
            )
            resolution_type = "IT Intervention"

        elif (
            "flickering" in text_lower
            or "screen" in text_lower
            or "display" in text_lower
        ):
            decision = "ROUTE_TO_IT"
            status = "Laptop display issue"
            assigned_team = "IT Support"
            recommended_action = (
                "IT Support should inspect the laptop display "
                "and determine whether hardware service is needed."
            )
            resolution_type = "IT Intervention"

        elif (
            "battery" in text_lower
            or "charging" in text_lower
            or "charger" in text_lower
        ):
            decision = "ROUTE_TO_IT"
            status = "Laptop battery support required"
            assigned_team = "IT Support"
            recommended_action = (
                "IT Support should inspect the battery and "
                "charging hardware."
            )
            resolution_type = "IT Intervention"

        elif "slow" in text_lower:
            decision = "TROUBLESHOOT"
            status = "Laptop performance troubleshooting"
            assigned_team = "IT Support"
            recommended_action = (
                "IT Support should perform basic performance "
                "troubleshooting."
            )
            resolution_type = "Troubleshooting"

    # ---------------------------------------------------------
    # PRINTER
    # ---------------------------------------------------------
    elif category == "Printer":

        if (
            "paper jam" in text_lower
            or "jammed" in text_lower
            or "paper stuck" in text_lower
        ):
            decision = "TROUBLESHOOT"
            status = "Printer troubleshooting"
            assigned_team = "IT Support"
            recommended_action = (
                "Clear the paper jam and restart the printer. "
                "If the issue continues, contact IT Support."
            )
            resolution_type = "Troubleshooting"

        elif (
            "not printing" in text_lower
            or "won't print" in text_lower
            or "wont print" in text_lower
        ):
            decision = "TROUBLESHOOT"
            status = "Printer troubleshooting"
            assigned_team = "IT Support"
            recommended_action = (
                "Check the print queue and restart the printer "
                "or print spooler."
            )
            resolution_type = "Troubleshooting"

        elif "offline" in text_lower:
            decision = "TROUBLESHOOT"
            status = "Printer offline"
            assigned_team = "IT Support"
            recommended_action = (
                "Check the printer connection and restart the "
                "printer."
            )
            resolution_type = "Troubleshooting"

    # ---------------------------------------------------------
    # EMAIL
    # ---------------------------------------------------------
    elif category == "Email":

        if (
            "full" in text_lower
            or "quota" in text_lower
            or "storage" in text_lower
            or "space" in text_lower
        ):
            decision = "TROUBLESHOOT"
            status = "Mailbox quota issue"
            assigned_team = "IT Support"
            recommended_action = (
                "Archive or delete unnecessary messages. "
                "Mailbox quota increases require manager approval."
            )
            resolution_type = "Troubleshooting"

        elif (
            "cannot send" in text_lower
            or "can't send" in text_lower
            or "cant send" in text_lower
        ):
            decision = "TROUBLESHOOT"
            status = "Email sending issue"
            assigned_team = "IT Support"
            recommended_action = (
                "IT Support should troubleshoot the email "
                "sending issue."
            )
            resolution_type = "Troubleshooting"

        elif (
            "cannot receive" in text_lower
            or "can't receive" in text_lower
            or "cant receive" in text_lower
        ):
            decision = "TROUBLESHOOT"
            status = "Email receiving issue"
            assigned_team = "IT Support"
            recommended_action = (
                "IT Support should troubleshoot the email "
                "receiving issue."
            )
            resolution_type = "Troubleshooting"

    # ---------------------------------------------------------
    # SOFTWARE
    # ---------------------------------------------------------
    elif category == "Software":

        if (
            "non-catalog" in text_lower
            or "non catalog" in text_lower
        ):
            decision = "SECURITY_REVIEW"
            status = "Non-catalog software requires review"
            assigned_team = "IT Security"
            escalation_reason = (
                "Non-catalog software requires IT Security review "
                "before installation."
            )
            recommended_action = (
                "Submit the software request for IT Security review."
            )
            resolution_type = "Security Review"

        elif (
            "install" in text_lower
            or "installation" in text_lower
        ):
            decision = "ROUTE_TO_IT"
            status = "Software installation request"
            assigned_team = "IT Support"
            recommended_action = (
                "Use the approved software catalog for "
                "self-service installation."
            )
            resolution_type = "Software Support"

        elif (
            "not opening" in text_lower
            or "won't open" in text_lower
            or "wont open" in text_lower
            or "doesn't open" in text_lower
            or "doesnt open" in text_lower
            or "not working" in text_lower
        ):
            decision = "TROUBLESHOOT"
            status = "Software troubleshooting"
            assigned_team = "IT Support"
            recommended_action = (
                "IT Support should troubleshoot the software "
                "application."
            )
            resolution_type = "Troubleshooting"

    # ---------------------------------------------------------
    # GENERAL IT
    # ---------------------------------------------------------
    else:

        decision = "HUMAN_REVIEW"
        status = "Human review required"
        assigned_team = "IT Support"
        escalation_reason = (
            "The request could not be confidently mapped to "
            "a specific IT resolution."
        )
        recommended_action = (
            "An IT Support representative should review "
            "the request."
        )
        resolution_type = "Human Review"

    # ---------------------------------------------------------
    # IMPORTANT:
    # Generic requests MUST ask for clarification.
    #
    # This runs AFTER category processing so that a generic
    # request cannot accidentally become ROUTE_TO_IT.
    # ---------------------------------------------------------
    if (
        initial_follow_up is not None
        and category != "Security"
        and not (
            "admin access" in text_lower
            or "administrator access" in text_lower
            or "admin privileges" in text_lower
            or "administrator privileges" in text_lower
        )
    ):
        decision = "CLARIFICATION"
        status = "More information required"
        assigned_team = "IT Support"

        reason = (
            "The initial request does not contain enough "
            "information to determine the correct IT resolution."
        )

        recommended_action = (
            "Please answer the follow-up question so the "
            "IT Support Agent can analyze the request further."
        )

        escalation_reason = None
        resolution_type = "Follow-up Required"
        needs_clarification = True

    confidence = calculate_confidence(
        category,
        source_score,
        needs_clarification
    )

    return {
        "category": category,
        "priority": priority,
        "confidence": confidence,
        "decision": decision,
        "status": status,
        "assigned_team": assigned_team,
        "resolution_type": resolution_type,
        "reason": (
            "The request was analyzed using the IT decision "
            "rules and available knowledge base."
        ),
        "recommended_action": recommended_action,
        "escalation_reason": escalation_reason,
        "source": {
            "id": source_id,
            "title": source_title,
            "similarity": round(source_score, 3)
        } if source else None,
        "policy": policy,
        "follow_up_question": follow_up_question,
        "follow_up_options": follow_up_options,
        "needs_clarification": needs_clarification,
        "related_tickets": []
    }