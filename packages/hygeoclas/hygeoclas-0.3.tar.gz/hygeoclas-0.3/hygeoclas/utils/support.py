from numpy import inf

class EarlyStopper:
    def __init__(self, patience=1, minDelta=0):
        self.patience = patience
        self.minDelta = minDelta
        self.counter = 0
        self.minValidationLoss = inf
        self.bestWeights = None

    def early_stop(self, model, validationLoss):
        if validationLoss < self.minValidationLoss:
            self.minValidationLoss = validationLoss
            self.counter = 0
            self.bestWeights = model.state_dict()
        elif validationLoss > (self.minValidationLoss + self.minDelta):
            self.counter += 1
            if self.counter >= self.patience:
                model.load_state_dict(self.bestWeights)
                return True
        return False