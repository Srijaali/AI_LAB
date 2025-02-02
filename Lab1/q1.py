import random

class Environment:
    def __init__(self):
        # Components of the system
        self.components = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        # State of each component: randomly assign 'safe' or 'vulnerable'
        self.state = {component: random.choice(['safe', 'vulnerable']) for component in self.components}

    def get_percept(self):
        # Return the state of all components
        return self.state

class SimpleReflexAgent:
    def __init__(self):
        self.patching = []

    def system_scan(self, environment):
        state = environment.get_percept()
        
        for component, component_state in state.items():
            if component_state == 'safe':
                print(f"Component {component} is secure and can be logged in.")
            elif component_state == 'vulnerable':
                print(f"Component {component} is not secure.. WARNING!!!")
                self.patching.append(component)
    
    def patching_vulnerabilities(self, environment):
        for component in self.patching:
            environment.state[component] = 'safe'
            print(f"{component} is now marked as safe.")

def run_agent(agent, environment):
    print("Scanning the system...")
    agent.system_scan(environment)
    print("\nPatching vulnerabilities...")
    agent.patching_vulnerabilities(environment)

agent = SimpleReflexAgent()
environment = Environment()

run_agent(agent, environment)

