from pt_pump_up_orms import ORM
from pt_pump_up_orms.orms import Link


class Author(ORM):
    def __init__(self,
                 id: int = None,
                 name: str = None,
                 institution: str = None,
                 link: Link = None) -> None:

        super().__init__(id, "author")

        self._name = name
        self._institution = institution
        self._link = link

    def serialize(self) -> dict:
        return {
            "id": self._id if self._id is not None else None,
            "name": self.name,
            "institution": self.institution,
            "link": self.link.serialize()
        }

    @property
    def name(self) -> str:
        if self._name is None:
            raise ValueError("Name is not set")

        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def institution(self) -> str:
        if self._institution is None:
            raise ValueError("Institution is not set")

        return self._institution

    @institution.setter
    def institution(self, institution: str) -> None:
        self._institution = institution

    @property
    def link(self) -> Link:
        if self._link is None:
            raise ValueError("Link is not set")

        return self._link

    @link.setter
    def link(self, link: Link) -> None:
        self._link = link
