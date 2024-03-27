from komodo.loaders.database.appliance_loader import ApplianceLoader
from komodo.models.framework.agent_runner import AgentRunner
from komodo.models.framework.appliance_runner import ApplianceRunner
from komodo.models.framework.appliance_runtime import ApplianceRuntime
from sample.appliance.appliance import SampleAppliance
from sample.appliance.config import LocalConfig

appliance = SampleAppliance(config=LocalConfig())


def build_and_run():
    prompt = '''
        Summarize the following text in 5 words and then translate into Spanish, Hindi and German:
        This is a sample application using the new Komodo SDK.
    '''
    runner = ApplianceRunner(appliance)
    response = runner.run(prompt)
    print(response.text)


def build_and_search():
    appliance.index()
    prompt = '''
        what is revenue breakdown of nvidia?
    '''
    runner = ApplianceRunner(appliance)
    response = runner.run(prompt)
    print(response.text)


def load_and_run():
    appliance = ApplianceLoader.load('sample')
    prompt = '''
        Summarize the following text in 5 words and translate into Spanish, Hindi and German:
        This is a sample application using the new Komodo 9 SDK.
    '''
    runner = ApplianceRunner(appliance)
    response = runner.run(prompt)
    print(response.text)


def build_and_search_with_agent():
    appliance.index()
    prompt = '''
        Any policy changes for nvidia?
    '''
    runtime = ApplianceRuntime(appliance)
    for a in runtime.get_all_agents():
        if 'docsearch' in a.shortcode:
            runner = AgentRunner(a)
            response = runner.run(prompt)
            print(response.text)

    agent = runtime.get_agent('librarian')
    runner = AgentRunner(agent)
    response = runner.run(prompt)
    print(response.text)


if __name__ == '__main__':
    email = "test@example.com"
    profile = next((x for x in appliance.users if x.email == email), None)
    print(profile.to_dict())
