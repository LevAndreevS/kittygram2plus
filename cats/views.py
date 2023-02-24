
from rest_framework.throttling import AnonRateThrottle, ScopedRateThrottle
from rest_framework import filters
from rest_framework import viewsets

from .models import Achievement, Cat, User

from .serializers import AchievementSerializer, CatSerializer, UserSerializer
from .permissions import OwnerOrReadOnly
# from .permissions import ReadOnly
from .throttling import WorkingHoursRateThrottle
from django_filters.rest_framework import DjangoFilterBackend


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = (OwnerOrReadOnly,)
    throttle_classes = (AnonRateThrottle,)  # Подключили класс AnonRateThrottle
    # Если кастомный тротлинг-класс вернёт True - запросы будут обработаны
    # Если он вернёт False - все запросы будут отклонены
    throttle_classes = (WorkingHoursRateThrottle, ScopedRateThrottle)
    # А далее применится лимит low_request
    # Для любых пользователей установим кастомный лимит 1 запрос в минуту

    # throttle_scope = 'low_request'

    # Указываем фильтрующий бэкенд DjangoFilterBackend
    # Из библиотеки django-filter
    # Добавим в кортеж ещё один бэкенд
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )

    # Временно отключим пагинацию на уровне вьюсета,
    # так будет удобнее настраивать фильтрацию
    # pagination_class = None

    # Фильтровать будем по полям color и birth_year модели Cat
    filterset_fields = ('color', 'birth_year')
    search_fields = ('$__all__',)
    ordering_fields = ('$__all__',)

    # Сортировка по умолчанию
    # ordering = ('birth_year',)

    # Кроме того, результат выдачи можно отсортировать по нескольким полям,
    # например по имени и году рождения /cats?ordering=name,birth_year.

    # '^' Начинается с
    # '=' полное совпадение
    # '$' регулярное выражение


#   Поиск можно проводить и по содержимому полей связанных моделей.
#   Доступные для поиска поля связанной модели указываются через нотацию
#   с двойным подчёркиванием:
#   ForeignKey текущей модели__имя поля в связанной модели.

#   search_fields = ('achievements__name', 'owner__username')

#    def get_permissions(self):
#        # Если в GET-запросе требуется получить информацию об объекте
#        if self.action == 'retrieve':
#            # Вернем обновленный перечень используемых пермишенов
#            return (ReadOnly(),)
#        # Для остальных ситуаций оставим текущий перечень пермишенов без
#        # изменений
#        return super().get_permissions()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
