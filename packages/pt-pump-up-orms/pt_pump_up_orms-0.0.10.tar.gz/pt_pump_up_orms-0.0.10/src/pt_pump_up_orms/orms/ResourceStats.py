from pt_pump_up_orms import ORM


class ResourceStats(ORM):
    def __init__(self,
                 id: int = None,
                 standard_format: bool = None,
                 off_the_shelf: bool = None,
                 preservation_rating: str = None) -> None:

        super().__init__(id, "resource-stats")

        self._standard_format = standard_format
        self._off_the_shelf = off_the_shelf
        self._preservation_rating = preservation_rating.lower(
        ) if preservation_rating is not None else None

    def serialize(self) -> dict:
        return {
            "id": self._id if self._id is not None else None,
            "standard_format": self.standard_format,
            "off_the_shelf": self.off_the_shelf,
            "preservation_rating": self.preservation_rating
        }

    @property
    def standard_format(self) -> bool:
        if self._standard_format is None:
            raise ValueError("Standard Format is not set")

        return self._standard_format

    @standard_format.setter
    def standard_format(self, standard_format: bool) -> None:
        self._standard_format = standard_format

    @property
    def off_the_shelf(self) -> bool:
        if self._off_the_shelf is None:
            raise ValueError("Off The Shelf is not set")

        return self._off_the_shelf

    @off_the_shelf.setter
    def off_the_shelf(self, off_the_shelf: bool) -> None:
        self._off_the_shelf = off_the_shelf

    @property
    def preservation_rating(self) -> str:
        if self._preservation_rating is None:
            raise ValueError("Preservation Rating is not set")

        return self._preservation_rating

    @preservation_rating.setter
    def preservation_rating(self, preservation_rating: str) -> None:
        self._preservation_rating = preservation_rating.lower(
        ) if preservation_rating is not None else None
