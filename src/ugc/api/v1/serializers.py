from marshmallow import Schema, fields
from marshmallow.validate import Range


class FilmBookmarkList(Schema):
    """Сериалайзер списка закладок фильмов."""

    id = fields.String()  # noqa: VNE003
    user_id = fields.UUID()
    film_id = fields.UUID()
    bookmarked = fields.Boolean(dump_default=True)
    bookmarked_at = fields.DateTime(format="%Y-%m-%d %H:%M:%S")


class FilmProgressCreate(Schema):
    """Сериалайзер для трекинга прогресса фильма."""

    viewed_frame = fields.Integer(
        strict=True, required=True, validate=[Range(min=1, error="Viewed frame must be greater than 0")])


class FilmProgressDetail(Schema):
    """Сериалайзер прогресса фильма."""

    user_id = fields.UUID()
    film_id = fields.UUID()
    viewed_frame = fields.Integer()


class FilmRatingCreate(Schema):
    """Сериалайзер для создания оценки фильму."""

    rating = fields.Integer(
        strict=True, required=True, validate=[Range(min=1, max=10, error="Rating must be between 1 and 10")])


class FilmRating(Schema):
    """Сериалайзер средней оценки фильма."""

    film_id = fields.UUID()
    rating = fields.Float()
