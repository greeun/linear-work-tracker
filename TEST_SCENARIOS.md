# Test Scenarios for linear-work-tracker

Generated test scenarios to validate skill triggering behavior.

---

## Happy Path Tests

These requests should trigger the skill and complete successfully.

### Test 1: Direct Request with Keywords

- **Request**: "Please automatic the linear from this file"
- **Expected**: Skill triggers and completes the primary task
- **Keywords matched**: automatic, linear

### Test 2: Multi-keyword Request

- **Request**: "I need to automatic and issue the linear"
- **Expected**: Skill triggers and handles compound request
- **Keywords matched**: automatic, linear, issue

### Test 3: Simple Command

- **Request**: "Automatic this"
- **Expected**: Skill triggers with minimal context
- **Keywords matched**: automatic

---

## Edge Case Tests

These requests should trigger the skill but may require extra handling.

### Test 1: Indirect Phrasing

- **Request**: "I'm having trouble with this, can you help?"
- **Expected**: Skill may trigger with clarifying question
- **Challenge**: No explicit keywords, relies on context

### Test 2: Partial Context

- **Request**: "Just do the linear thing"
- **Expected**: Skill triggers and asks for clarification
- **Challenge**: Incomplete request, missing details

### Test 3: Minor Typo

- **Request**: "Please automatie this document"
- **Expected**: Skill triggers despite typo
- **Challenge**: Typo in keyword: "automatie" vs "automatic"

---

## Out of Scope Tests

These requests should NOT trigger the skill.

### Test 1: Edit/modify instead of extract

- **Request**: "Edit the text in this PDF"
- **Expected**: Skill does NOT trigger
- **Reason**: Edit/modify instead of extract

### Test 2: Different file format

- **Request**: "Work with this Excel file"
- **Expected**: Skill does NOT trigger
- **Reason**: Different file format

### Test 3: Create instead of process

- **Request**: "Create a new PDF from scratch"
- **Expected**: Skill does NOT trigger
- **Reason**: Create instead of process

### Test 4: Similar Keywords, Wrong Intent

- **Request**: "Tell me about automatic best practices"
- **Expected**: Skill does NOT trigger
- **Reason**: Asking for information, not performing action

---

## Running These Tests

1. Start a new Claude conversation
2. Enter each request exactly as shown
3. Verify skill triggers (or doesn't) as expected
4. Note any failures for description refinement

### If Tests Fail

| Issue | Fix |
|-------|-----|
| Happy path doesn't trigger | Add missing keywords to description |
| Edge case doesn't trigger | Add synonyms to description |
| Out of scope triggers | Narrow description scope |

