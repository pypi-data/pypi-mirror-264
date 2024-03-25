from pt_pump_up_orms import ORM


class Link(ORM):
    def __init__(self,
                 id: int = None,
                 email: str = None,
                 website: str = None,
                 github_url: str = None,
                 hugging_face_url: str = None,
                 papers_with_code_url: str = None,
                 paper_url: str = None) -> None:

        super().__init__(id, "link")

        self._email = email
        self._website = website
        self._github_url = github_url
        self._hugging_face_url = hugging_face_url
        self._papers_with_code_url = papers_with_code_url
        self._paper_url = paper_url

    def serialize(self) -> dict:
        return {
            "id": self._id if self._id is not None else None,
            "email": self.email,
            "website": self.website,
            "github_url": self.github_url,
            "hugging_face_url": self.hugging_face_url,
            "papers_with_code_url": self.papers_with_code_url,
            "paper_url": self.paper_url
        }

    @property
    def email(self) -> str:
        if self._email is None:
            raise ValueError("Email is not set")

        return self._email

    @email.setter
    def email(self, email: str) -> None:
        self._email = email

    @property
    def website(self) -> str:
        if self._website is None:
            raise ValueError("Website is not set")

        return self._website

    @website.setter
    def website(self, website: str) -> None:
        self._website = website

    @property
    def github_url(self) -> str:
        if self._github_url is None:
            raise ValueError("GitHub URL is not set")

        return self._github_url

    @github_url.setter
    def github_url(self, github_url: str) -> None:
        self._github_url = github_url

    @property
    def hugging_face_url(self) -> str:
        if self._hugging_face_url is None:
            raise ValueError("Hugging Face URL is not set")

        return self._hugging_face_url

    @hugging_face_url.setter
    def hugging_face_url(self, hugging_face_url: str) -> None:
        self._hugging_face_url = hugging_face_url

    @property
    def papers_with_code_url(self) -> str:
        if self._papers_with_code_url is None:
            raise ValueError("Papers With Code URL is not set")

        return self._papers_with_code_url

    @papers_with_code_url.setter
    def papers_with_code_url(self, papers_with_code_url: str) -> None:
        self._papers_with_code_url = papers_with_code_url

    @property
    def paper_url(self) -> str:
        if self._paper_url is None:
            raise ValueError("Paper URL is not set")

        return self._paper_url

    @paper_url.setter
    def paper_url(self, paper_url: str) -> None:
        self._paper_url = paper_url
