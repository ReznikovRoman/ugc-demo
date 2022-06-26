from marshmallow import Schema, fields


class FilmBookmarkList(Schema):
    """Сериалайзер списка закладок фильмов."""

    id = fields.String()  # noqa: VNE003
    user_id = fields.UUID()
    film_id = fields.UUID()
    bookmarked = fields.Boolean(default=True)
    bookmarked_at = fields.DateTime(format="%Y-%m-%d %H:%M:%S")


class FilmProgressDetail(Schema):
    """Сериалайзер прогресса фильма."""

    user_id = fields.UUID()
    film_id = fields.UUID()
    viewed_frame = fields.Integer()
