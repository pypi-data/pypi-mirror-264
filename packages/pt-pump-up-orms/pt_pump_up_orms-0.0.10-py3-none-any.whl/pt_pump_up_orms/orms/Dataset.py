from pt_pump_up_orms import ORM
from pt_pump_up_orms.orms import Link
from pt_pump_up_orms.orms import ResourceStats


class Dataset(ORM):
    def __init__(self,
                 id: int = None,
                 short_name: str = None,
                 full_name: str = None,
                 description: str = None,
                 year: int = None,
                 link: Link = None,
                 resource_stats: ResourceStats = None,
                 authors: list = None,
                 nlp_tasks: list = None) -> None:

        super().__init__(id, "dataset")

        self._short_name = short_name
        self._full_name = full_name
        self._description = description
        self._year = year
        self._link = link
        self._resource_stats = resource_stats
        self._authors = authors
        self._nlp_tasks = nlp_tasks

    def serialize(self) -> dict:
        return {
            "id": self._id if self._id is not None else None,
            "short_name": self.short_name,
            "full_name": self.full_name,
            "description": self.description,
            "year": self.year,
            "link": self.link.serialize() if self.link else None,
            "resource_stats": [resource_stat.serialize() for resource_stat in self.resource_stats] if self.resource_stats else None,
            "authors": [author.serialize() for author in self.authors] if self.authors else None,
            "nlp_tasks": [nlp_task.serialize() for nlp_task in self.nlp_tasks] if self.nlp_tasks else None
        }

    """
    # TODO: Remove the Need for .index()
    @property
    def id(self):
        if self._id is None and self._json.get("short_name"):
            for dataset in self.index().json():
                if dataset.get("short_name") == self._json.get("short_name"):
                    self._id = dataset.get("id")
                    break

        return self._id
    """

    @property
    def short_name(self):
        if self._short_name is None:
            raise Exception("Short Name is not set")

        return self._short_name

    @short_name.setter
    def short_name(self, short_name):
        self._short_name = short_name

    @property
    def full_name(self):
        if self._full_name is None:
            raise Exception("Full Name is not set")

        return self._full_name

    @full_name.setter
    def full_name(self, full_name):
        self._full_name = full_name

    @property
    def description(self):
        if self._description is None:
            raise Exception("Description is not set")

        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def year(self):
        if self._year is None:
            raise Exception("Year is not set")

        return self._year

    @year.setter
    def year(self, year):
        self._year = year

    @property
    def resource_stats(self):
        if self._resource_stats is None:
            raise Exception("Resource Stats is not set")

        return self._resource_stats

    @resource_stats.setter
    def resource_stats(self, resource_stats):
        self._resource_stats = resource_stats

    @property
    def authors(self):
        if self._authors is None:
            raise Exception("Authors is not set")

        return self._authors

    @authors.setter
    def authors(self, authors):
        self._authors = authors

    @property
    def nlp_tasks(self):
        if self._nlp_tasks is None:
            raise Exception("NLP Tasks is not set")

        return self._nlp_tasks

    @nlp_tasks.setter
    def nlp_tasks(self, nlp_tasks):
        self._nlp_tasks = nlp_tasks

    @property
    def link(self):
        if self._link is None:
            raise Exception("Link is not set")

        return self._link

    @link.setter
    def link(self, link):
        self._link = link
