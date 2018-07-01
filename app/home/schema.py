from app.ext import mar
from app.user.models import Movies, Cinemas


#转为json数据
class MoviesSchema(mar.ModelSchema):
    class Meta:
        model = Movies

movie_schmae = MoviesSchema
movies_schmae = MoviesSchema(many=True)


class CinemasSchema(mar.ModelSchema):
    class Meta:
        model = Cinemas

cinema_schmae = MoviesSchema
cinemas_schmae = MoviesSchema(many=True)