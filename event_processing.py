# event_processing.py

from collections import defaultdict
from itertools import groupby

def process_events(events):
    # Step 1: Regroup events by email ID
    events_by_email = defaultdict(list)
    for event in events:
        events_by_email[event["email"]].append(event)

    # Step 2: Sort events within each email by position
    for email, email_events in events_by_email.items():
        email_events.sort(key=lambda x: x["position"])

    # Step 3: Identify common BD for successive events
    common_bd = defaultdict(list)
    for email, email_events in events_by_email.items():
        for i in range(len(email_events) - 1):
            event1 = email_events[i]
            event2 = email_events[i + 1]
            bd = f"{event1['activity']}_{event2['activity']}"
            common_bd[bd].append(email)

    # Step 4: Generate constraints
    constraints = []
    for bd, emails in common_bd.items():
        most_common_bd = max(set(emails), key=emails.count)
        activities = bd.split('_')
        constraint = {"activities": activities, "most_common_bd": most_common_bd}
        constraints.append(constraint)

    return constraints

if __name__ == "__main__":
    # Sample input data: list of events with email ID and activity
    events = [
        {"email": "email1@example.com", "activity": "activity_A", "position": 2},
        {"email": "email1@example.com", "activity": "activity_B", "position": 1},
        {"email": "email2@example.com", "activity": "activity_A", "position": 1},
        {"email": "email2@example.com", "activity": "activity_C", "position": 2},
        # ... add more events
    ]

    constraints = process_events(events)

    # Print generated constraints
    for constraint in constraints:
        print("Activities:", constraint["activities"])
        print("Most Common BD:", constraint["most_common_bd"])
        print()
