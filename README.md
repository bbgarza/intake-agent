# Intake Agent

A small terminal tool that turns a vague data request ("we need a report on support ticket volume") into a structured project brief that an analytics team can act on.

## Why this exists

On analytics teams, most requests arrive as one line in Slack or a ticket, with no context. Before work can start, someone has to go back and ask the same questions every time: What problem are you solving? Who will use this? What data does it need, and does that data exist? What's out of scope? How will we know it worked?

That back-and-forth is slow and easy to do unevenly. Some requests get a thorough intake and some get none, and work can start before anyone understands the ask. This tool runs the intake the same way every time:

1. Take the rough request.
2. Ask clarifying questions in grouped batches, not one at a time.
3. Fill every field, or mark it OPEN.
4. Produce a clean brief.

One rule holds throughout: **it never invents details.** Anything the requester doesn't know gets marked `OPEN` and listed in the brief, so gaps can be seen instead of guessed over.

## How to run it

You need Python 3. On a Mac, it comes with Apple's command line tools. No other installs or API keys.

```bash
python3 intake.py
```

The script asks for the request and the requester, then works through three batches of questions:

| Batch | Covers |
|---|---|
| 1. The ask and its use | Problem, desired outcome, user stories, output format |
| 2. The data | Data sources, availability, where the data lives, who owns it |
| 3. The frame | Scope in and out, success measure, timing, dependencies |

Leave an answer blank, or type `?`, `idk`, or `tbd`, and that field is marked `OPEN`. If anything is still open at the end, you get one chance to go back and fill it in.

The finished brief is printed in the terminal and saved as a Markdown file in `briefs/` (for example, `briefs/brief-20260929-160642.md`).

## The brief

Each brief has these sections:

- Requester and team
- Problem or need (the why)
- Desired outcome
- User stories (*As a [role], I need [X] so that [Y]*)
- Data sources required
- Data availability (available? which system? who owns it?)
- Output format
- Scope (in and out)
- Success measure
- Constraints (timing, dependencies)
- Open questions and assumptions

The full design is in [`spec.md`](spec.md).

## What version 1 can and can't do

**It can:**
- Run the same structured intake every time, so no field gets skipped
- Show each batch's topics before asking, so the requester knows what's coming
- Mark unknowns as `OPEN` instead of guessing, and list them in the brief
- Offer one follow-up pass over the open fields
- Save every brief with a timestamp as a Markdown file

**It can't:**
- Judge the quality of an answer. It accepts whatever is typed. "Out of scope: nothing" or "Success: fewer tickets" goes in as written, even though an experienced intake lead would push back.
- Catch contradictions between answers. For example, "the data isn't available" alongside "deadline: next week."
- Follow up after the session ends, or track what happens to the request next.

Version 1 is plain Python with no AI. I wanted the workflow and the brief format to work on their own before adding a model.

## Next versions

**v2: AI reasoning on the answers.** Add a language model that reads each answer and responds the way a good intake lead would. It will:
- catch **vague** answers ("a dashboard" for whom, showing what?)
- catch **incomplete** answers (a success measure with no number or baseline)
- catch **contradictory** answers (a tight deadline when the data owner is unknown)

It will then ask targeted follow-up questions. The no-invention rule stays: the model asks, and it doesn't fill in answers itself.

**Later versions:**
- **Reminders.** Nudge requesters and owners when open questions or handoffs sit untouched.
- **A neutral record of where requests stalled.** A factual timeline of each request (waiting on data access, an owner, or a decision), so teams can see where work gets stuck without blaming anyone.

## Project files

```
intake.py    # the intake script
spec.md      # design spec: purpose, loop, brief fields, guardrail
README.md    # this file
.gitignore   # files git leaves out (generated briefs, secrets, system files)
briefs/      # generated briefs (kept out of git)
```

## How this was built

Built with Claude Code as a hands-on project in AI-assisted development. I wrote the spec and made the design calls; Claude Code wrote most of the code.
