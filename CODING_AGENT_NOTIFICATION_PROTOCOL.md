# Coding Agent Notification Protocol for Documentation Updates

## Purpose

This protocol defines how Coding Agents should notify the Documentation Agent when code changes require documentation updates.

## When to Notify Documentation Agent

Notify the Documentation Agent whenever you make code changes that affect:

1. **Function/Class Signatures**
   - Added new functions or classes
   - Modified function parameters
   - Changed return types
   - Added or removed exceptions

2. **New Features**
   - Implemented new functionality
   - Added new modules or packages
   - Created new API endpoints
   - Added configuration options

3. **Breaking Changes**
   - Removed functions or classes
   - Changed function behavior
   - Modified API contracts
   - Updated dependency requirements

4. **Bug Fixes**
   - Fixed bugs that affect documented behavior
   - Corrected implementation that differs from documentation

5. **Project Status Changes**
   - Completed major features
   - Changed project development stage
   - Updated roadmap or upcoming features

## Notification Format

When notifying the Documentation Agent, use this format:

```
[DOCUMENTATION UPDATE REQUIRED]

**Change Type**: [NEW_FEATURE | MODIFICATION | BUG_FIX | REMOVAL | STATUS_UPDATE]

**Affected Files**:
- path/to/file1.py
- path/to/file2.py

**Summary of Changes**:
[Brief description of what changed]

**Specific Documentation Updates Needed**:
1. [Function/Class name] - [What needs updating]
2. [Documentation file] - [What needs updating]
3. README.md - [If applicable, what section needs updating]

**Code Changes**:
[Brief summary or relevant code snippets]

**Priority**: [HIGH | MEDIUM | LOW]

**Additional Context**:
[Any additional information the Documentation Agent might need]
```

## Example Notifications

### Example 1: New Function Added

```
[DOCUMENTATION UPDATE REQUIRED]

**Change Type**: NEW_FEATURE

**Affected Files**:
- src/utils/validator.py

**Summary of Changes**:
Added new function `validate_email()` to validate email addresses using regex.

**Specific Documentation Updates Needed**:
1. `validate_email()` - Add complete docstring with Args, Returns, Raises sections
2. README.md - Update usage examples section if applicable

**Code Changes**:
```python
def validate_email(email: str) -> bool:
    """Validates email format."""
    # Implementation here
```

**Priority**: MEDIUM

**Additional Context**:
Function is part of new validation module. Should be documented alongside other validation functions.
```

### Example 2: Function Signature Changed

```
[DOCUMENTATION UPDATE REQUIRED]

**Change Type**: MODIFICATION

**Affected Files**:
- src/api/client.py

**Summary of Changes**:
Modified `fetch_data()` function to accept optional `timeout` parameter.

**Specific Documentation Updates Needed**:
1. `fetch_data()` - Update docstring Args section to include new `timeout` parameter
2. API documentation - Update API endpoint documentation if this affects external API

**Code Changes**:
```python
def fetch_data(endpoint: str, timeout: int = 30) -> dict:
    # Previous: def fetch_data(endpoint: str) -> dict:
```

**Priority**: HIGH

**Additional Context**:
This is a breaking change for any code using the previous signature. Documentation must clearly indicate the new optional parameter.
```

### Example 3: Project Status Update

```
[DOCUMENTATION UPDATE REQUIRED]

**Change Type**: STATUS_UPDATE

**Affected Files**:
- README.md
- docs/PROJECT_STATUS.md

**Summary of Changes**:
Completed authentication module feature. Project is now in beta stage.

**Specific Documentation Updates Needed**:
1. README.md - Update development stage section to "Beta"
2. PROJECT_STATUS.md - Add check mark for authentication module completion
3. PROJECT_STATUS.md - Update roadmap section

**Code Changes**:
- Authentication module fully implemented and tested
- All tests passing

**Priority**: MEDIUM

**Additional Context**:
This is a milestone update. README should reflect current project maturity.
```

## Quick Notification Template

For minor changes, use this simplified format:

```
[DOCUMENTATION UPDATE REQUIRED]

**Change**: [Brief one-line description]
**Files**: [List of affected files]
**Action Needed**: [What documentation needs updating]
```

## Integration with Commit Messages

When committing code changes, include documentation update indicators:

- `[DOC]` - Documentation update required
- `[DOC-URGENT]` - Urgent documentation update required
- `[DOC-README]` - README.md update required

Example commit message:
```
feat(api): add user authentication endpoint [DOC]

Added POST /api/auth/login endpoint. Documentation Agent should update API docs.
```

## Automated Notification Checklist

After making code changes, verify:

- [ ] Are there new functions/classes that need docstrings?
- [ ] Did function signatures change requiring docstring updates?
- [ ] Are there new features that should be documented in README.md?
- [ ] Did project status change requiring README.md updates?
- [ ] Are there breaking changes that need documentation updates?
- [ ] Did I complete work that needs check marks in project documentation?

If any checkbox is checked, notify the Documentation Agent.

## Notification Timing

- **Immediate**: For breaking changes or high-priority updates
- **After Commit**: For regular feature additions or modifications
- **Batch Updates**: For multiple small changes, notify once with a summary

## Priority Guidelines

- **HIGH**: Breaking changes, critical bug fixes, major feature additions
- **MEDIUM**: New features, function signature changes, status updates
- **LOW**: Minor updates, typos, formatting improvements

---

**Remember**: Keeping documentation current is a shared responsibility. Notify the Documentation Agent proactively to maintain high-quality documentation standards.

