import json
import numpy as np
from sklearn.linear_model import LinearRegression



class JournalModel:
    def __init__(self, root, leaf, mapper):
        # if root in gas_ved_dict:
        #     root = gas_ved_dict[root]
        # if root in new_dormitory_dict:
        #     root = new_dormitory_dict[root]
        self.root = root
        self.leaf = leaf
        self.mapper = mapper

    @staticmethod
    def get_journal():
        with open('D:/GPN_KIP/auxiliary_data/journal_mapped.json') as f:
            journal = json.load(f)
        return journal

    def fit(self, hours=11.0):
        pass

    def predict(self, data):
        pass


class WorkJournal(JournalModel):
    def __init__(self, root, leaf, mapper):
        root = root.split("_")[0]
        leaf = leaf.split("_")[0]
        super().__init__(root=root, leaf=leaf, mapper=mapper)
        self.model = None

    def fit(self, hours=11.0):
        journal = self.get_journal()
        coef = journal[self.mapper[self.root][0]]["resources"][self.leaf]["number"] / \
               journal[self.mapper[self.root][0]]["resources"][self.leaf]["productivity"]
        #coef /= hours
        regressor = LinearRegression(fit_intercept=False)
        regressor.coef_ = np.array([coef])
        regressor.intercept_ = np.array([0.0])
        self.model = regressor

    def predict(self, data):
        return self.model.predict(data)


class PerformanceJournal(JournalModel):
    def __init__(self, root, leaf, mapper):
        super().__init__(root=root, leaf=leaf, mapper=mapper)
        self.hours = None
        self.productivity = None
        self.numbers = None

    def fit(self, hours=11.0):
        journal = self.get_journal()

        numbers = {}
        for root in self.root:
            numbers[root] = journal[self.mapper[self.leaf][0]]["resources"][root]["number"]
        self.numbers = numbers
        self.productivity = journal[self.mapper[self.leaf][0]]["resources"][self.root[0]]["productivity"]
        self.hours = hours

    def predict(self, data):
        min_numbers = []
        for i, node in enumerate(self.root):
            min_number = data[0, i] / self.numbers[node]
            min_numbers.append(min_number)
        coef = min(min_numbers)
        performance = [coef * self.productivity]

        return performance
