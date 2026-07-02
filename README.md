# Multi-Agent Workflow System

This project demonstrates a planner-executor-validator workflow where multiple agents collaborate to complete a business automation task.

The system is intentionally easy to read: each agent has one responsibility, communication happens through structured objects, and the orchestrator records retries and failures.

## What This Project Shows

- Planner, executor, and validator agents
- Task decomposition into structured workflow steps
- Retry logic and failure detection
- Workflow monitoring through an execution log
- Structured outputs suitable for enterprise automation

## Architecture

```text
Business request -> PlannerAgent -> ExecutorAgent -> ValidatorAgent -> Retry if needed -> Final summary
```

## Quick Start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
$env:PYTHONPATH="src"
python -m multi_agent_workflow.main --task "Prepare onboarding workflow for a new enterprise customer"
pytest
```

## Production Extensions

- Use OpenAI function calling for planning and validation.
- Add external API clients for CRM, ticketing, email, and document systems.
- Persist workflow runs in Postgres or DynamoDB.
- Emit metrics to Datadog, Azure Monitor, or CloudWatch.
