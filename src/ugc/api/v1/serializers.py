from marshmallow import Schema, fields
from marshmallow.validate import Range


class CursorPaginationQueryParams(Schema):
    """Параметры для `cursor-based` сортировки."""

    limit = fields.Integer()
    cursor = fields.String()


class CursorPaginationResultsMixin(Schema):
    """Миксин для результатов `cursor-based` пагинации."""

    cursor = fields.String()


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


class FilmReviewCreate(Schema):
    """Сериалайзер для создания рецензии на фильм."""

    title = fields.Str(required=True)
    review = fields.Str(required=True)


class FilmReviewDetail(Schema):
    """Сериалайзер рецензии на фильм."""

    id = fields.Str()  # noqa: VNE003
    user_id = fields.UUID()
    film_id = fields.UUID()
    title = fields.Str()
    review = fields.Str()
    created_at = fields.DateTime()


class FilmReviewList(CursorPaginationResultsMixin):
    """Список рецензий на фильм."""

    data = fields.Nested(FilmReviewDetail(many=True))
