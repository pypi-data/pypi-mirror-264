from pt_pump_up_orms import ORM


class NLPTask(ORM):
    def __init__(self,
                 id: int = None,
                 short_name: str = None,
                 full_name: str = None,
                 standard_format: str = None,
                 description: str = None,
                 papers_with_code_ids: list = None) -> None:

        super().__init__(id, "nlp-task")

        self._short_name = short_name
        self._full_name = full_name
        self._standard_format = standard_format
        self._description = description
        self._papers_with_code_ids = papers_with_code_ids

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "short_name": self.short_name,
            "full_name": self.full_name,
            "standard_format": self.standard_format,
            "description": self.description,
            "papers_with_code_ids": self.papers_with_code_ids
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
    def standard_format(self) -> str:
        if self._standard_format is None:
            raise ValueError("Standard Format is not set")

        return self._standard_format

    @standard_format.setter
    def standard_format(self, standard_format: str) -> None:
        self._standard_format = standard_format

    @property
    def description(self) -> str:
        if self._description is None:
            raise ValueError("Description is not set")

        return self._description

    @description.setter
    def description(self, description: str) -> None:
        self._description = description

    @property
    def papers_with_code_ids(self) -> list:
        if self._papers_with_code_ids is None:
            raise ValueError("Papers With Code IDs are not set")

        return self._papers_with_code_ids

    @papers_with_code_ids.setter
    def papers_with_code_ids(self, papers_with_code_ids: list) -> None:
        self._papers_with_code_ids = papers_with_code_ids

    @property
    def papers_with_code_ids(self) -> list:
        if self._papers_with_code_ids is None:
            raise ValueError("Papers With Code IDs are not set")

        return self._papers_with_code_ids

    @papers_with_code_ids.setter
    def papers_with_code_ids(self, papers_with_code_ids: list) -> None:
        self._papers_with_code_ids = papers_with_code_ids
