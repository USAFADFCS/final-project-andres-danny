from fairlib.core.base_agent import SimpleAgent

class ManagerAgent(SimpleAgent):
    pass


def route_to_nice(self, question):
    return self.nice_instructor.answer(question)

def route_to_mean(self, question):
    return self.mean_instructor.answer(question)
