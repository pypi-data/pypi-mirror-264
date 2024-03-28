from komodo.framework.komodo_agent import KomodoAgent
from komodo.framework.komodo_context import KomodoContext
from komodo.framework.komodo_tool_registry import KomodoToolRegistry
from komodo.framework.komodo_user import KomodoUser
from komodo.models.framework.chat_message import ChatMessage
from komodo.models.framework.chat_metadata import ChatMetaData


class ModelRequest:
    def __init__(self, user: KomodoUser, agent: KomodoAgent, prompt: str, **kwargs):
        self.user = user
        self.agent = agent
        self.prompt = prompt
        self.kwargs = kwargs

    def __str__(self):
        template = "From: {} To: {} Name: {} (provider: {}, model: {})"
        return template.format(self.user.email,
                               self.agent.email,
                               self.agent.name,
                               self.agent.provider,
                               self.agent.model)

    def prepare_messages(self):
        instructions = ChatMessage.build("Instructions", self.agent.instructions)
        caution = ChatMessage.build("Caution", "Do not make up fake data or hallucinate information.")
        guidance = ChatMessage.build("Guidance", "Prioritize tools provided to you to answer the questions.")
        agent_messages = ChatMessage.convert_from_context(self.agent.generate_context(self.prompt))
        messages = [m.add_tag('Agent') for m in [instructions, caution, guidance] + agent_messages]

        workflow_context = self.kwargs.get('workflow_context', KomodoContext())
        workflow_messages = ChatMessage.convert_from_context(workflow_context)
        messages += [m.add_tag('Workflow') for m in workflow_messages]

        history = self.kwargs.get('history', [])
        messages += history

        workflow_inputs = self.kwargs.get('workflow_inputs', [])
        messages += [m.add_tag('Workflow Agent Outputs') for m in workflow_inputs]
        return messages

    def prepare_metadata(self):
        return ChatMetaData(self.user, self.agent)

    def build_openai_params(self, stream=False):
        params = {
            "model": self.agent.model,
            "messages": self.prepare_messages(),
            "stream": stream,
            "temperature": self.agent.temperature,
            "top_p": self.agent.top_p,
            "seed": self.agent.seed,
            "max_tokens": self.agent.max_tokens,
        }

        if self.agent.tools:
            params["tools"] = KomodoToolRegistry.get_definitions(self.agent.tools)

        if self.agent.provider == "openai" and self.agent.output_format and 'json' in self.agent.output_format:
            from openai.types.chat.completion_create_params import ResponseFormat
            params['response_format'] = ResponseFormat(type="json_object")

        return params

    def prepare_detailed_prompt(self):
        conversation = []
        messages = self.prepare_messages()
        for message in messages:
            conversation.append(message['role'] + ": " + message['content'])
        conversation.append("Prompt: " + self.prompt)
        return "\n".join(conversation)
