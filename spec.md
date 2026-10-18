# Intake Agent — Spec

## Purpose
Take a vague one-line request and, through a short batched back-and-forth, turn it into a clean structured brief.

**Domain:** Analytics and data project requests.

## The loop
1. Read the rough request.
2. Ask clarifying questions in grouped batches (not one at a time).
3. Stop asking once the fields are filled.
4. Output the structured brief.

## Output brief fields
- Requester and team
- Problem or need (the why)
- Desired outcome
- User stories (as a [role], I need [X] so that [Y])
- Data sources required
- Data availability (is it available, and where: system and owner)
- Output format
- Scope in and out
- Success measure
- Constraints (timing, dependencies)
- Open questions and assumptions

## Question batches
1. **The ask and its use:** problem, desired outcome, user stories, output format
2. **The data:** sources, availability, location and owner
3. **The frame:** scope, success measure, constraints

## Guardrail
Never invent details. If unknown, ask or mark it open.

## Version 1
- Keep it simple, no API keys.
- A Python script run in the terminal that walks through the three question batches, then prints the finished brief and saves it to a file.
- AI reasoning to be added in a later version.
