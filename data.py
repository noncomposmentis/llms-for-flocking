import pickle
import os

from datetime import datetime


class Data:
    """
    A class to facilitate storage and retrieval of test data
    """
    def __init__(self, identifier, agents, config, results):
        self.identifier = identifier
        self.directory = f'./{results}/{identifier}'
        self.agents = agents
        self.config = config
        self.results = results

    @staticmethod
    def save(
            agents,
            config,
            identifier=datetime.now().strftime("%y%b%d%H%M%S").lower(),
            results="results"
    ) -> str:
        Data.check_for_results_directory(results)  # make sure we have a results directory

        if not os.path.isdir(f'./{results}/{identifier}'):
            os.makedirs(f'./{results}/{identifier}')  # create an empty test results directory

            file = open(f'./{results}/{identifier}/results', 'ab')

            agents_object = [
                {
                    "identifier": agent.identifier,
                    "position_history": agent.position_history,
                    "memory": agent.memory
                } for agent in agents
            ]

            pickle.dump(Data(identifier, agents_object, config, results), file)

            file.close()
            print(f'Success: Save test {identifier}!')
            return identifier
        else:
            print(f'Error: Test {identifier} already exists!')

    @staticmethod
    def load(identifier, results="results"):
        # todo: error handling
        file = open(f'./{results}/{identifier}/results', 'rb')
        data = pickle.load(file)
        print(f'Success: Load test {identifier}!')
        return data

    @staticmethod
    def check_for_results_directory(dirname):
        # Create our results directory
        if not os.path.exists(f'./{dirname}'):
            os.makedirs(f'./{dirname}')
