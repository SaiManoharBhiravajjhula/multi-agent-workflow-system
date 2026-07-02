from __future__ import annotations

import argparse
import os

from multi_agent_workflow.orchestrator import WorkflowOrchestrator


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the multi-agent workflow demo.")
    parser.add_argument("--task", required=True)
    args = parser.parse_args()

    run = WorkflowOrchestrator(max_retries=int(os.getenv("MAX_RETRIES", "2"))).run(args.task)

    print(f"Task: {run.plan.task}")
    print(f"Planner created {len(run.plan.steps)} steps.")
    print(f"Validator approved workflow: {run.validation.approved}")

    print("\nStep results:")
    for result in run.results:
        print(f"- {result.step.name}: {result.status.value} after {result.attempts} attempt(s)")

    print("\nEvent log:")
    for event in run.event_log:
        print(f"- {event}")


if __name__ == "__main__":
    main()