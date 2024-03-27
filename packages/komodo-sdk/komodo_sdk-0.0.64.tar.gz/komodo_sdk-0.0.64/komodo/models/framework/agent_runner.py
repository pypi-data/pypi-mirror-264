from komodo.framework.komodo_agent import KomodoAgent
from komodo.framework.komodo_user import KomodoUser
from komodo.models.framework.model_request import ModelRequest
from komodo.models.framework.model_response import ModelResponse
from komodo.models.framework.responder import get_model_response
from komodo.models.framework.runner import Runner
from komodo.models.openai.openai_api_streamed import openai_chat_response_streamed
from komodo.shared.utils.term_colors import print_gray


class AgentRunner(Runner):
    def __init__(self, agent: KomodoAgent, user: KomodoUser = None):
        self.user = KomodoUser.default() if user is None else user
        self.agent = agent

    def run(self, prompt, **kwargs) -> ModelResponse:
        request = ModelRequest(user=self.user, agent=self.agent, prompt=prompt, **kwargs)
        print_gray("Requesting response for: ", request)
        response = get_model_response(request)
        return response

    def run_streamed(self, prompt, **kwargs):
        request = ModelRequest(user=self.user, agent=self.agent, prompt=prompt, **kwargs)
        print_gray("Requesting streamed response for: ", request)
        for response in openai_chat_response_streamed(request):
            yield response
