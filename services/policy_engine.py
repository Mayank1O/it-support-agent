import json
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_json(filename):
    path = os.path.join(BASE_DIR, "data", filename)

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_knowledge_base():
    return load_json("knowledge_base.json")


def get_policies():
    return load_json("policies.json")


def get_tickets():
    return load_json("tickets.json")


def find_policy(category):
    knowledge_base = get_knowledge_base()

    for article in knowledge_base:
        if article["category"].lower() == category.lower():
            return article

    return None


def find_governing_policy(category):
    policies = get_policies()

    matching = []

    for policy in policies:
        if policy["category"].lower() == category.lower():
            matching.append(policy)

    if len(matching) == 0:
        return None

    matching.sort(key=lambda x: x["priority"])

    return matching[0]


def find_related_tickets(request):
    tickets = get_tickets()

    request_words = request.lower().split()

    related = []

    for ticket in tickets:
        ticket_text = (
            ticket["issue"] + " " +
            ticket["status"]
        ).lower()

        matches = 0

        for word in request_words:

            if len(word) < 4:
                continue

            if word in ticket_text:
                matches += 1

        if matches >= 1:
            related.append(ticket)

    return related