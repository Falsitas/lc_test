from services.agent import LangChainTest

agents = dict()

def get_agent(user):
    '''Get or create an agent for the given user. by its Group.'''
    if user.groups.filter(name='ALPHA').exists():
        group = "ALPHA"
    else:
        group = "BETA"

    if group not in agents:
        agents[group] = LangChainTest(group=group)
    return agents[group]