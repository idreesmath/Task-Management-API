---
name: code-quality-reviewer
description: Review code for quality, best practices, security issues, and improvements. Use this skill when reviewing pull requests, checking code before commits, refactoring existing code, or ensuring code follows best practices and security standards. Provides actionable feedback on code structure, patterns, and potential issues.
---

# Code Quality Reviewer

Systematic code review for quality, security, and best practices.

## Review Process

1. **Understand the code** - Read and comprehend what it does
2. **Check functionality** - Verify it works correctly
3. **Review quality** - Structure, readability, maintainability
4. **Security audit** - Identify vulnerabilities
5. **Performance** - Spot inefficiencies
6. **Best practices** - Language and framework conventions
7. **Provide feedback** - Actionable, specific suggestions

## Review Checklist

### Functionality

- [ ] Code does what it's intended to do
- [ ] Edge cases are handled
- [ ] Error handling is appropriate
- [ ] Return values are correct
- [ ] Logic is sound

### Code Quality

- [ ] Clear, descriptive names (variables, functions, classes)
- [ ] Functions are focused (single responsibility)
- [ ] No code duplication
- [ ] Proper code organization
- [ ] Consistent formatting
- [ ] Appropriate comments (why, not what)
- [ ] No commented-out code
- [ ] No unnecessary complexity

### Testing

- [ ] Tests exist and pass
- [ ] Test coverage is adequate
- [ ] Tests are meaningful
- [ ] Edge cases are tested
- [ ] Mock dependencies appropriately

### Security

- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] Input validation present
- [ ] No hardcoded secrets/credentials
- [ ] Proper authentication/authorization
- [ ] Secure data handling
- [ ] No sensitive data in logs

### Performance

- [ ] No N+1 query problems
- [ ] Efficient algorithms
- [ ] Appropriate data structures
- [ ] No unnecessary database calls
- [ ] Proper indexing
- [ ] Resource cleanup (connections, files)

### API Design (FastAPI)

- [ ] Proper HTTP methods (GET, POST, PUT, DELETE)
- [ ] Correct status codes
- [ ] Proper error responses
- [ ] Request/response validation
- [ ] Clear endpoint naming
- [ ] Consistent API patterns

### Database (SQLModel)

- [ ] Proper field types
- [ ] Appropriate constraints
- [ ] Indexes on queried fields
- [ ] Efficient queries
- [ ] Proper session handling
- [ ] Transaction management

## Common Issues

### Security Vulnerabilities

**SQL Injection (avoid raw SQL):**
```python
# BAD - SQL Injection vulnerable
query = f"SELECT * FROM tasks WHERE id = {task_id}"

# GOOD - Use SQLModel/SQLAlchemy
task = session.get(Task, task_id)
```

**Missing Input Validation:**
```python
# BAD - No validation
def create_task(title: str):
    task = Task(title=title)

# GOOD - Pydantic validation
class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)

def create_task(task: TaskCreate):
    db_task = Task(**task.model_dump())
```

**Hardcoded Secrets:**
```python
# BAD - Hardcoded secret
API_KEY = "sk-1234567890abcdef"

# GOOD - Environment variable
import os
API_KEY = os.getenv("API_KEY")
```

### Code Quality Issues

**Unclear Naming:**
```python
# BAD
def gt(t, s):
    return session.exec(select(Task).where(Task.status == s)).all()

# GOOD
def get_tasks_by_status(session: Session, status: str) -> List[Task]:
    statement = select(Task).where(Task.status == status)
    return session.exec(statement).all()
```

**Function Too Long:**
```python
# BAD - 50+ lines in one function
def process_task(task_id):
    # ... 50 lines of code

# GOOD - Split into focused functions
def validate_task(task_id):
    # validation logic

def update_task_status(task_id, status):
    # update logic

def notify_task_completion(task_id):
    # notification logic

def process_task(task_id):
    validate_task(task_id)
    update_task_status(task_id, "completed")
    notify_task_completion(task_id)
```

**Code Duplication:**
```python
# BAD - Repeated code
def create_user_task(user_id, title):
    task = Task(user_id=user_id, title=title)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def create_admin_task(admin_id, title):
    task = Task(admin_id=admin_id, title=title)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

# GOOD - Reuse logic
def create_task_for_entity(entity_id: int, title: str, entity_type: str) -> Task:
    task = Task(**{f"{entity_type}_id": entity_id, "title": title})
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def create_user_task(user_id, title):
    return create_task_for_entity(user_id, title, "user")
```

### Performance Issues

**N+1 Query Problem:**
```python
# BAD - N+1 queries
tasks = session.exec(select(Task)).all()
for task in tasks:
    user = session.get(User, task.user_id)  # N queries

# GOOD - Join or eager load
from sqlmodel import select
statement = select(Task).join(User)
tasks = session.exec(statement).all()
```

**Missing Indexes:**
```python
# BAD - No index on frequently queried field
class Task(SQLModel, table=True):
    status: str

# GOOD - Index on status
class Task(SQLModel, table=True):
    status: str = Field(index=True)
```

### Error Handling

**Generic Exceptions:**
```python
# BAD - Catch all exceptions
try:
    task = session.get(Task, task_id)
except:
    return None

# GOOD - Specific exceptions
try:
    task = session.get(Task, task_id)
except SQLAlchemyError as e:
    logger.error(f"Database error: {e}")
    raise HTTPException(status_code=500, detail="Database error")
```

**Missing Error Messages:**
```python
# BAD - No context
raise HTTPException(status_code=404)

# GOOD - Clear message
raise HTTPException(
    status_code=404,
    detail=f"Task with id {task_id} not found"
)
```

## Review Report Format

```markdown
## Code Review: [Feature/File Name]

### Summary
[Brief overview of what was reviewed]

### Strengths
- [What's done well]
- [Good patterns used]

### Issues Found

#### Critical (Security/Bugs)
1. [Issue description]
   - Location: [file:line]
   - Problem: [What's wrong]
   - Fix: [How to fix it]

#### High Priority (Quality/Performance)
1. [Issue description]
   - Location: [file:line]
   - Problem: [What's wrong]
   - Suggestion: [How to improve]

#### Low Priority (Style/Optimization)
1. [Minor improvement]
   - Location: [file:line]
   - Suggestion: [How to improve]

### Recommendations
- [Overall suggestions]
- [Best practices to follow]

### Approval Status
- [ ] Approved
- [ ] Approved with minor changes
- [ ] Needs changes before approval
```

## Best Practices

1. **Be constructive** - Focus on improving the code, not criticizing
2. **Be specific** - Point to exact lines and provide examples
3. **Explain why** - Don't just say what's wrong, explain the impact
4. **Suggest solutions** - Provide code examples when possible
5. **Prioritize issues** - Critical bugs first, style issues last
6. **Consider context** - Understand project constraints and deadlines
7. **Look for patterns** - Repeated issues suggest training opportunities
8. **Verify fixes** - If possible, test suggested changes
9. **Acknowledge good code** - Positive feedback motivates improvement
10. **Stay objective** - Focus on code quality, not personal preferences
