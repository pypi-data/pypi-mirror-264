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

        self.short_name = short_name
        self.full_name = full_name
        self.description = description
        self.year = year
        self.link = link
        self.resource_stats = resource_stats
        self.authors = authors
        self.nlp_tasks = nlp_tasks

    def serialize(self) -> dict:
        return {
            "id": self._id,
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
