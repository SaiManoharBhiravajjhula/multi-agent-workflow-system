from __future__ import annotations

from multi_agent_workflow.models import StepResult, StepStatus, ValidationReport, WorkflowPlan, WorkflowStep


class PlannerAgent:
    """Breaks a business request into executable workflow steps."""

    def plan(self, task: str) -> WorkflowPlan:
        steps = [
            WorkflowStep("1", "data_collection", "Collect customer and project details.", "customer_profile"),
            WorkflowStep("2", "document_generation", "Create onboarding checklist and kickoff notes.", "onboarding_document"),
            WorkflowStep("3", "api_notification", "Notify CRM and support systems.", "notification_receipt"),
            WorkflowStep("4", "final_summary", "Summarize completed workflow and owners.", "summary"),
        ]
        return WorkflowPlan(task=task, steps=steps)


class ExecutorAgent:
    """Executes workflow steps; API calls would live here in production."""

    def __init__(self) -> None:
        self._attempts_by_step: dict[str, int] = {}

    def execute(self, step: WorkflowStep) -> StepResult:
        attempts = self._attempts_by_step.get(step.step_id, 0) + 1
        self._attempts_by_step[step.step_id] = attempts

        if step.name == "api_notification" and attempts == 1:
            return StepResult(step, StepStatus.FAILED, "", attempts, "CRM API timeout")

        output = f"{step.required_output}: completed for {step.name}"
        return StepResult(step, StepStatus.SUCCESS, output, attempts)


class ValidatorAgent:
    """Checks that every required output was produced."""

    def validate(self, plan: WorkflowPlan, results: list[StepResult]) -> ValidationReport:
        issues: list[str] = []
        successful_outputs = {result.step.required_output for result in results if result.status == StepStatus.SUCCESS}
        for step in plan.steps:
            if step.required_output not in successful_outputs:
                issues.append(f"Missing required output: {step.required_output}")
        return ValidationReport(approved=not issues, issues=issues)
