# AGENTS

## Development Methodology: Spec-Driven Development Only

### Workflow

1. **Specify** → Define requirements in a spec document before any code is written.
2. **Plan** → Break the spec into actionable implementation steps.
3. **Tasks** → Create discrete, testable tasks from the plan.
4. **Implement** → Write code that directly fulfills spec requirements.

### Rules

- **No code without spec reference.** Every function, feature, and behavior must trace back to a documented specification.
- **No features beyond spec.** Do not add functionality, enhancements, or "nice-to-haves" that are not explicitly defined in the spec.
- **Spec is the single source of truth.** If there is ambiguity, resolve it in the spec first, then implement.
- **All spec changes are versioned.** Previous spec versions are archived in `specs_history/` for traceability.
