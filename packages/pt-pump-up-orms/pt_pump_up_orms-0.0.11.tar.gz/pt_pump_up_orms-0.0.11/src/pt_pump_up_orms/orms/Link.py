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

        self.email = email
        self.website = website
        self.github_url = github_url
        self.hugging_face_url = hugging_face_url
        self.papers_with_code_url = papers_with_code_url
        self.paper_url = paper_url

    def serialize(self) -> dict:
        return {
            "id": self._id,
            "email": self.email,
            "website": self.website,
            "github_url": self.github_url,
            "hugging_face_url": self.hugging_face_url,
            "papers_with_code_url": self.papers_with_code_url,
            "paper_url": self.paper_url
        }
