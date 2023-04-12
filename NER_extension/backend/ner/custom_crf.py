from sklearn_crfsuite import CRF


class CustomCRF(CRF):
    def feature_dict(self, x, y=None, state_features=None):
        features = super().feature_dict(x, y, state_features)
        return features