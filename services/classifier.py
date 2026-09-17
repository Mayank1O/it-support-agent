from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


# Training examples
training_texts = [
    # Password
    "I forgot my password",
    "I cannot log into my account",
    "my account is locked",
    "I tried my password too many times",
    "I need to reset my password",

    # VPN
    "my VPN is not working",
    "VPN connection failed",
    "my VPN credentials expired",
    "I cannot connect to VPN",
    "VPN stopped working",

    # Laptop
    "my laptop is not turning on",
    "my laptop is completely dead",
    "laptop screen is flickering",
    "my laptop has a hardware problem",
    "I need a laptop replacement",

    # Software
    "I want to install software",
    "I need a new application installed",
    "this software is not in the catalog",
    "I need approval for software",
    "can I install this application",

    # Printer
    "my printer is not working",
    "printer says paper jam",
    "I cannot print",
    "printer queue is stuck",
    "the printer has an error",

    # Email
    "my mailbox is full",
    "I cannot send emails",
    "my email storage is almost full",
    "I need more mailbox space",
    "email quota is full",

    # Guest Wi-Fi
    "I need Wi-Fi for a guest",
    "guest needs internet access",
    "how can I get guest Wi-Fi",
    "visitor needs Wi-Fi",
    "guest wireless access",

    # Expense Software
    "I cannot log into the expense tool",
    "expense software says invalid credentials",
    "expense application is not working",
    "I need help with the expense system",
    "I cannot access the expense software",

    # Security
    "I received a phishing email",
    "I think this email is malicious",
    "someone tried to access my account",
    "I think my computer has malware",
    "I received a suspicious email",

    # WFH Equipment
    "I need a monitor for working from home",
    "I work remotely and need equipment",
    "can I get a home office chair",
    "I need equipment for remote work",
    "I work from home four days a week"
]


training_labels = [
    "Password",
    "Password",
    "Password",
    "Password",
    "Password",

    "VPN",
    "VPN",
    "VPN",
    "VPN",
    "VPN",

    "Laptop",
    "Laptop",
    "Laptop",
    "Laptop",
    "Laptop",

    "Software",
    "Software",
    "Software",
    "Software",
    "Software",

    "Printer",
    "Printer",
    "Printer",
    "Printer",
    "Printer",

    "Email",
    "Email",
    "Email",
    "Email",
    "Email",

    "Guest Wi-Fi",
    "Guest Wi-Fi",
    "Guest Wi-Fi",
    "Guest Wi-Fi",
    "Guest Wi-Fi",

    "Expense Software",
    "Expense Software",
    "Expense Software",
    "Expense Software",
    "Expense Software",

    "Security",
    "Security",
    "Security",
    "Security",
    "Security",

    "WFH Equipment",
    "WFH Equipment",
    "WFH Equipment",
    "WFH Equipment",
    "WFH Equipment"
]


# Convert text into numerical features
vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english"
)

X = vectorizer.fit_transform(training_texts)


# Train classifier
model = LogisticRegression(
    max_iter=1000
)

model.fit(X, training_labels)


def predict_issue(text):

    text_vector = vectorizer.transform([text])

    prediction = model.predict(text_vector)[0]

    probabilities = model.predict_proba(text_vector)[0]

    confidence = max(probabilities)

    return prediction, confidence