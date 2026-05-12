from agent import LangChainTest

agents = dict()

def get_agent(user):
    '''Get or create an agent for the given user. by its Group.'''
    if user.group not in agents:
        agents[user.group] = LangChainTest(group=user.group)
    return agents[user.group]