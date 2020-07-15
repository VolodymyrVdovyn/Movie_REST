from django.contrib import admin
from .models import Category, Actor, Genre, Movie, MovieShots, RatingStar, Rating, Review

from django.utils.safestring import mark_safe

from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms


class MovieAdminForm(forms.ModelForm):
    '''Форма с виджетом ckeditor'''
    description = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url')
    list_display_links = ('name',)


class ReviewInline(admin.StackedInline):
    model = Review
    extra = 1
    readonly_fields = ('name', 'email')


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url', 'get_image', 'draft')
    list_display_links = ('title', 'get_image', )

    list_filter = ('year', 'category',)
    search_fields = ('title', 'category__name')
    inlines = (ReviewInline,)
    save_on_top = True
    save_as = True
    list_editable = ('draft',)
    readonly_fields = ('get_image', )
    actions = ('publish', 'unpublish',)
    form = MovieAdminForm

    def get_image(self, model):
        return mark_safe(f'<img src={model.poster.url} width="50" height="60">')

    get_image.short_description = 'Изображение'

    def unpublish(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = f'{row_update} записи были обновлены'
        self.message_user(request, f'{message_bit}')

    def publish(self, request, queryset):
        """Опубликовать"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = f'{row_update} записи были обновлены'
        self.message_user(request, f'{message_bit}')

    unpublish.short_description = 'Снять с публикации'
    unpublish.allowed_permissions = ('change',)

    publish.short_description = 'Опубликовать'
    publish.allowed_permissions = ('change',)

    fieldsets = (
        (None, {
            "fields": (
                ('title', 'tagline'),    
            ),
        }),
        (None, {
            "fields": (
                'description', ('poster', 'get_image',),
            ),
        }),
        (None, {
            "fields": (
                ('year', 'world_premiere', 'country'),
            ),
        }),
        ('Actors', {
            "fields": (
                ('actors', 'directors'),
            ),
        }),
        (None, {
            "fields": (
                ('genres', 'category'),
            ),
        }),
        (None, {
            "fields": (
                ('budget', 'fees_in_usa', 'fees_in_world'),
            ),
        }),
        ('Options', {
            "fields": (
                ('url', 'draft'),
            ),
        }),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'movie', 'email')


@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):
    list_display = ('value', )



@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'url',)


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'get_image',)
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60">')

    get_image.short_description = 'Изображение'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('ip', 'star', 'movie')


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    list_display = ('title', 'movie', 'get_image',)
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60">')

    get_image.short_description = 'Изображение'


admin.site.site_title = 'Django Movies'
admin.site.site_header = 'Django Movies'

