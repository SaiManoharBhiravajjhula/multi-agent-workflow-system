from multi_agent_workflow.orchestrator import WorkflowOrchestrator


def test_workflow_retries_and_validates_success():
    run = WorkflowOrchestrator(max_retries=2).run("Prepare onboarding workflow")
    assert run.validation.approved is True
    assert any("retry_scheduled: api_notification" == event for event in run.event_log)
    assert all(result.output for result in run.results)
