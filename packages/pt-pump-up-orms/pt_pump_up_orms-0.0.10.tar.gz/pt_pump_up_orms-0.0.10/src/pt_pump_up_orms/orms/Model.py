from pt_pump_up_orms import ORM
from pt_pump_up_orms.orms import Link
from pt_pump_up_orms.orms import ResourceStats


class Model(ORM):
    def __init__(self,
                 id: int = None,
                 short_name: str = None,
                 full_name: str = None,
                 description: str = None,
                 year: int = None,
                 authors: list = None,
                 nlp_tasks: list = None,
                 link: Link = None,
                 resource_stats: ResourceStats = None,
                 results: list = None) -> None:

        super().__init__(id, 'machine-learning-model')

        self._short_name = short_name
        self._full_name = full_name
        self._description = description
        self._year = year
        self._authors = authors
        self._nlp_tasks = nlp_tasks
        self._link = link
        self._resource_stats = resource_stats
        self._results = results

    def serialize(self) -> dict:
        return {
            "id": self._id if self._id is not None else None,
            "short_name": self.short_name,
            "full_name": self.full_name,
            "description": self.description,
            "year": self.year,
            "authors": [author.serialize() for author in self.authors] if self.authors else None,
            "nlp_tasks": [nlp_task.serialize() for nlp_task in self.nlp_tasks] if self.nlp_tasks else None,
            "link": self.link.serialize() if self.link else None,
            "resource_stats": self.resource_stats.serialize() if self.resource_stats else None,
            "results": [result.serialize() for result in self.results] if self.results else None
        }

    @property
    def short_name(self) -> str:
        if self._short_name is None:
            raise ValueError("Short Name is not set")

        return self._short_name

    @short_name.setter
    def short_name(self, short_name: str) -> None:
        self._short_name = short_name

    @property
    def full_name(self) -> str:
        if self._full_name is None:
            raise ValueError("Full Name is not set")

        return self._full_name

    @full_name.setter
    def full_name(self, full_name: str) -> None:
        self._full_name = full_name

    @property
    def description(self) -> str:
        if self._description is None:
            raise ValueError("Description is not set")

        return self._description

    @description.setter
    def description(self, description: str) -> None:
        self._description = description

    @property
    def year(self) -> int:
        if self._year is None:
            raise ValueError("Year is not set")

        return self._year

    @year.setter
    def year(self, year: int) -> None:
        self._year = year

    @property
    def authors(self) -> list:
        if self._authors is None:
            raise ValueError("Authors are not set")

        return self._authors

    @authors.setter
    def authors(self, authors: list) -> None:
        self._authors = authors

    @property
    def nlp_tasks(self) -> list:
        if self._nlp_tasks is None:
            raise ValueError("NLP Tasks are not set")

        return self._nlp_tasks

    @nlp_tasks.setter
    def nlp_tasks(self, nlp_tasks: list) -> None:
        self._nlp_tasks = nlp_tasks

    @property
    def link(self) -> Link:
        if self._link is None:
            raise ValueError("Link is not set")

        return self._link

    @link.setter
    def link(self, link: Link) -> None:
        self._link = link

    @property
    def resource_stats(self) -> ResourceStats:
        if self._resource_stats is None:
            raise ValueError("Resource Stats are not set")

        return self._resource_stats

    @resource_stats.setter
    def resource_stats(self, resource_stats: ResourceStats) -> None:
        self._resource_stats = resource_stats

    @property
    def results(self) -> list:
        if self._results is None:
            raise ValueError("Results are not set")

        return self._results

    @results.setter
    def results(self, results: list) -> None:
        self._results = results
