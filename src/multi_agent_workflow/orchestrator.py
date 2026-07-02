from __future__ import annotations

from multi_agent_workflow.agents import ExecutorAgent, PlannerAgent, ValidatorAgent
from multi_agent_workflow.models import StepResult, StepStatus, WorkflowRun


class WorkflowOrchestrator:
    def __init__(self, planner: PlannerAgent | None = None, executor: ExecutorAgent | None = None, validator: ValidatorAgent | None = None, max_retries: int = 2) -> None:
        self.planner = planner or PlannerAgent()
        self.executor = executor or ExecutorAgent()
        self.validator = validator or ValidatorAgent()
        self.max_retries = max_retries

    def run(self, task: str) -> WorkflowRun:
        event_log: list[str] = [f"workflow_started: {task}"]
        plan = self.planner.plan(task)
        event_log.append(f"planner_created_steps: {len(plan.steps)}")

        results = [self._execute_with_retry(step, event_log) for step in plan.steps]
        validation = self.validator.validate(plan, results)
        event_log.append(f"validator_approved: {validation.approved}")
        for issue in validation.issues:
            event_log.append(f"validation_issue: {issue}")

        return WorkflowRun(plan, results, validation, event_log)

    def _execute_with_retry(self, step, event_log: list[str]) -> StepResult:
        last_result: StepResult | None = None
        for attempt in range(1, self.max_retries + 2):
            result = self.executor.execute(step)
            last_result = result
            event_log.append(f"executor_{step.name}_attempt_{attempt}: {result.status.value}")
            if result.status == StepStatus.SUCCESS:
                return result
            if attempt <= self.max_retries:
                event_log.append(f"retry_scheduled: {step.name}")
        assert last_result is not None
        return last_result
