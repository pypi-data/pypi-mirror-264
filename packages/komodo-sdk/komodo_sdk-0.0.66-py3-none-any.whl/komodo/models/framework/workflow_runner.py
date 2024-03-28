import threading
from time import sleep

from paradag import dag_run, SequentialProcessor, MultiThreadProcessor

from komodo.framework.komodo_agent import KomodoAgent
from komodo.framework.komodo_workflow import KomodoWorkflow
from komodo.models.framework.agent_runner import AgentRunner
from komodo.models.framework.model_response import ModelResponse
from komodo.models.framework.runner import Runner
from komodo.models.framework.workflow_executor import WorkflowExecutor
from komodo.models.framework.workflow_selector import WorkflowSelector


class WorkflowRunner(Runner):
    def __init__(self, workflow, user=None, parallel=False, max_workers=4):
        self.workflow: [KomodoWorkflow] = workflow
        self.user = user if user is not None else KomodoAgent.default()
        self.parallel = parallel
        self.max_workers = max_workers
        self.status = []
        self.outputs = None
        self.text = None

    def status_reporter(self, agent, status):
        # self.status.append(f"{agent.name}: {status}")
        pass

    def result_reporter(self, agent, result):
        prompt = self.workflow.prompts[agent] if agent in self.workflow.prompts else ""
        self.status.append(f"{agent.name}: {prompt} -> {result.text}")

    def run(self, prompt, **kwargs):
        history = kwargs.get('history', None)
        if history:
            explainer = self.workflow.explainer()
            runner = self.runner_factory(explainer, self.user)
            return runner.run(prompt, **kwargs)

        else:
            self.status = []
            self.outputs = None

            try:
                processor = SequentialProcessor() if not self.parallel else MultiThreadProcessor()
                selector = WorkflowSelector(max_workers=self.max_workers)
                executor = WorkflowExecutor(self.workflow, prompt, self.user,
                                            self.runner_factory, self.status_reporter, self.result_reporter,
                                            **kwargs)
                processed = dag_run(self.workflow.dag, processor=processor, executor=executor, selector=selector)
            finally:
                self.status.append("Completed")

            self.outputs = [{agent: executor.outputs[agent.shortcode]} for agent in processed]
            self.text = "\n".join([f"{agent.name}: {executor.outputs[agent.shortcode]}" for agent in processed])

            return ModelResponse(model="Workflow", status="Completed", output=self.outputs, text=self.text)

    def run_streamed(self, prompt, **kwargs):
        history = kwargs.get('history', None)
        if history:
            explainer = self.workflow.explainer()
            runner = self.runner_factory(explainer, self.user)
            for response in runner.run_streamed(prompt, **kwargs):
                yield response

        else:
            self.status = []
            self.outputs = None
            r = threading.Thread(target=self.run, args=(prompt,), kwargs=kwargs)
            r.start()

            yielded = 0
            done = False

            while not done:
                n = len(self.status)
                for i in range(yielded, n):
                    done = self.status[i] == "Completed"
                    if not done:
                        yield self.status[i] + "\n\n"

                yielded = n
                if not done:
                    sleep(0.1)

            r.join()

    @staticmethod
    def runner_factory(item, user=None):
        if isinstance(item, KomodoAgent):
            return AgentRunner(item, user=user)

        if isinstance(item, KomodoWorkflow):
            return WorkflowRunner(item, user=user)

        raise ValueError(f"Unsupported item type: {type(item)}")
