"""
Intake Agent — version 1 (no AI yet).

Walks you through three batches of questions, then turns your answers
into a structured brief, prints it, and saves it to the briefs/ folder.

Run it with:   python3 intake.py
"""

import os
from datetime import datetime

# ---------------------------------------------------------------------------
# 1. THE QUESTIONS
#
# Each field in the brief has a short key (used inside the program), a label
# (shown in the brief), and the question we ask. Questions are grouped into
# batches, matching the spec.
# ---------------------------------------------------------------------------

BATCHES = [
    {
        "title": "Batch 1 of 3: The ask and its use",
        "questions": [
            ("problem", "Problem or need",
             "What problem are you trying to solve? Why does this matter now?"),
            ("outcome", "Desired outcome",
             "What should be true once this is done?"),
            ("user_stories", "User stories",
             "Who will use this, and for what? Try the form: "
             "As a [role], I need [X] so that [Y]."),
            ("output_format", "Output format",
             "What form should the result take? (dashboard, report, CSV, alert, API...)"),
        ],
    },
    {
        "title": "Batch 2 of 3: The data",
        "questions": [
            ("data_sources", "Data sources required",
             "What data is needed? (e.g. web traffic logs, product usage events, billing tables)"),
            ("data_available", "Is the data available?",
             "Does this data exist and can we get to it today? (yes / no / partly)"),
            ("data_location", "Where it lives (system)",
             "Where does it live? (e.g. data warehouse, BigQuery, S3 bucket, spreadsheet)"),
            ("data_owner", "Data owner",
             "Who owns that data? (team or person)"),
        ],
    },
    {
        "title": "Batch 3 of 3: The frame",
        "questions": [
            ("scope_in", "In scope",
             "What is definitely IN scope?"),
            ("scope_out", "Out of scope",
             "What is explicitly OUT of scope?"),
            ("success", "Success measure",
             "How will we know it worked? (a number, a decision made, a time saved...)"),
            ("timing", "Timing",
             "Any deadline or time pressure?"),
            ("dependencies", "Dependencies",
             "Does this depend on other teams, launches, or approvals?"),
        ],
    },
]

# Answers that mean "I don't know". The guardrail: we never guess, so these
# (and blank answers) get marked OPEN instead.
UNKNOWN_ANSWERS = {"", "?", "idk", "unknown", "not sure", "n/a", "tbd"}

OPEN = "OPEN"


# ---------------------------------------------------------------------------
# 2. HELPER FUNCTIONS
# ---------------------------------------------------------------------------

def ask(question):
    """Ask one question and return the answer, or OPEN if it's unknown."""
    answer = input(f"  > {question}\n    ").strip()
    if answer.lower() in UNKNOWN_ANSWERS:
        return OPEN
    return answer


def run_batch(title, questions, answers):
    """Show a whole batch of questions up front, then collect the answers."""
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)
    print("In this batch I'll ask:")
    for _, label, _ in questions:
        print(f"  - {label}")
    print("(Leave blank or type '?' if you don't know — it'll be marked OPEN.)\n")

    for key, _, question in questions:
        answers[key] = ask(question)


def all_questions():
    """Every question from every batch, as one flat list."""
    return [q for batch in BATCHES for q in batch["questions"]]


def build_brief(answers):
    """Turn the answers dictionary into a Markdown brief (a string)."""
    def show(key):
        return answers.get(key, OPEN)

    labels = {key: label for key, label, _ in all_questions()}
    open_items = [labels[k] for k, v in answers.items() if v == OPEN and k in labels]
    if show("requester") == OPEN:
        open_items.insert(0, "Requester and team")

    lines = [
        "# Project Brief",
        "",
        f"_Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}_",
        "",
        f"**Original request:** {show('request')}",
        "",
        "## Requester and team",
        show("requester"),
        "",
        "## Problem or need",
        show("problem"),
        "",
        "## Desired outcome",
        show("outcome"),
        "",
        "## User stories",
        show("user_stories"),
        "",
        "## Data sources required",
        show("data_sources"),
        "",
        "## Data availability",
        f"- **Available:** {show('data_available')}",
        f"- **System:** {show('data_location')}",
        f"- **Owner:** {show('data_owner')}",
        "",
        "## Output format",
        show("output_format"),
        "",
        "## Scope",
        f"- **In:** {show('scope_in')}",
        f"- **Out:** {show('scope_out')}",
        "",
        "## Success measure",
        show("success"),
        "",
        "## Constraints",
        f"- **Timing:** {show('timing')}",
        f"- **Dependencies:** {show('dependencies')}",
        "",
        "## Open questions and assumptions",
    ]

    if open_items:
        lines.append("**Still open (not answered during intake):**")
        lines += [f"- {item}" for item in open_items]
    else:
        lines.append("**Still open:** none — all fields answered.")

    assumptions = show("assumptions")
    lines.append("")
    lines.append("**Assumptions stated by requester:** "
                 + ("none stated" if assumptions == OPEN else assumptions))

    return "\n".join(lines) + "\n"


def save_brief(text):
    """Save the brief to briefs/brief-<date-time>.md and return the path."""
    folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "briefs")
    os.makedirs(folder, exist_ok=True)  # create the folder if it's missing
    filename = f"brief-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
    path = os.path.join(folder, filename)
    with open(path, "w") as f:
        f.write(text)
    return path


# ---------------------------------------------------------------------------
# 3. THE MAIN LOOP
# ---------------------------------------------------------------------------

def main():
    answers = {}  # key -> answer, filled in as we go

    print("\nIntake Agent v1 — turn a rough request into a structured brief.")
    print("-" * 60)
    answers["request"] = ask("What's the request, in one line?")
    answers["requester"] = ask("Who is asking, and which team are they on?")

    # Walk through the three batches from the spec.
    for batch in BATCHES:
        run_batch(batch["title"], batch["questions"], answers)

    # "Stop asking once the fields are filled": if anything is still OPEN,
    # offer ONE follow-up batch covering just those fields.
    still_open = [q for q in all_questions() if answers[q[0]] == OPEN]
    if still_open:
        print(f"\n{len(still_open)} field(s) are still OPEN.")
        again = input("Want to take another pass at them now? (y/n) ").strip().lower()
        if again.startswith("y"):
            run_batch("Follow-up: open items", still_open, answers)

    answers["assumptions"] = ask(
        "\nLast one: any assumptions you're making that we should write down?")

    brief = build_brief(answers)
    print("\n" + "=" * 60)
    print(brief)
    path = save_brief(brief)
    print("=" * 60)
    print(f"Saved to: {path}")


if __name__ == "__main__":
    # Ctrl+C quits cleanly instead of printing a scary error.
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nIntake cancelled. Nothing was saved.")
