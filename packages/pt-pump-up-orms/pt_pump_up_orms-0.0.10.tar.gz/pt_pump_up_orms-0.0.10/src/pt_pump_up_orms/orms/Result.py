from pt_pump_up_orms.ORM import ORM
from pt_pump_up_orms.orms import Dataset


class Result(ORM):
    def __init__(self,
                 id: int = None,
                 metric: str = None,
                 value: float = None,
                 train_dataset: Dataset = None,
                 validation_dataset: Dataset = None,
                 test_dataset: Dataset = None,
                 ) -> None:

        super().__init__(id, "result")

        self._metric = metric
        self._value = value
        self._train_dataset = train_dataset
        self._validation_dataset = validation_dataset
        self._test_dataset = test_dataset

    def serialize(self) -> dict:
        return {
            "id": self._id if self._id is not None else None,
            "metric": self.metric,
            "value": self.value,
            "train_dataset": self.train_dataset.serialize(),
            "validation_dataset": self.validation_dataset.serialize(),
            "test_dataset": self.test_dataset.serialize()
        }

    @property
    def metric(self) -> str:
        if self._metric is None:
            raise ValueError("Metric is not set")

        return self._metric

    @metric.setter
    def metric(self, metric: str) -> None:
        self._metric = metric

    @property
    def value(self) -> float:
        if self._value is None:
            raise ValueError("Value is not set")

        return self._value

    @value.setter
    def value(self, value: float) -> None:
        self._value = value

    @property
    def train_dataset(self) -> Dataset:
        if self._train_dataset is None:
            raise ValueError("Train Dataset is not set")

        return self._train_dataset

    @train_dataset.setter
    def train_dataset(self, train_dataset: Dataset) -> None:
        self._train_dataset = train_dataset

    @property
    def validation_dataset(self) -> Dataset:
        if self._validation_dataset is None:
            raise ValueError("Validation Dataset is not set")

        return self._validation_dataset

    @validation_dataset.setter
    def validation_dataset(self, validation_dataset: Dataset) -> None:
        self._validation_dataset = validation_dataset

    @property
    def test_dataset(self) -> Dataset:
        if self._test_dataset is None:
            raise ValueError("Test Dataset is not set")

        return self._test_dataset

    @test_dataset.setter
    def test_dataset(self, test_dataset: Dataset) -> None:
        self._test_dataset = test_dataset
