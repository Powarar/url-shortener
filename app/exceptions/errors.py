class ShortenerBaseError(Exception):
    pass


class NoLongUrlFoundError(Exception):
    def __init__(self, slug: str = None):
        self.slug = slug
        super().__init__(f"Long URL not found for slug: {slug}")



class SlugAlreadyExistsError(ShortenerBaseError):
    pass
