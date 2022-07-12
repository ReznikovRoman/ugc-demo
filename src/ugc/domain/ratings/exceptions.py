from ugc.common.exceptions import BaseNetflixUGCError


class NoFilmRatingError(BaseNetflixUGCError):
    """У фильма нет рейтинга."""
