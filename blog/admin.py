from django.contrib import admin

from blog.models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_per_page = 25
    date_hierarchy = 'publish'
    list_display = ('title', 'author', 'created', 'updated', 'publish', 'status')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = (
        'status',
        'publish',
        'created',
        ('author', admin.RelatedOnlyFieldListFilter,),)
    search_fields = ('title', 'author__username',)
    fieldsets = (
        (None, {'fields': ('title', 'slug', 'author', 'category')}),
        ('Content', {'fields': ('body',)}),
        ('Publication information', {'fields': ('publish', 'status',)}),
        ('Image', {'fields': ('image_url',)}),
        ('Tags', {'fields': ('tags',)}),
    )
    ordering = ('-status', '-created',)
    actions = ["publish", 'cancel_publication']

    @admin.action(description="Publish")
    def publish(self, request, queryset):
        queryset.update(status='published')

    @admin.action(description="Cancel publication")
    def cancel_publication(self, request, queryset):
        queryset.update(status='draft')


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_per_page = 25
    list_select_related = ('post', 'user')
    list_display = ('post', 'user')
    search_fields = ('post', 'user')
    list_filter = ('created',)
    ordering = ('-created',)


@admin.register(PostDislike)
class PostDislikeAdmin(admin.ModelAdmin):
    list_per_page = 25
    list_select_related = ('post', 'user')
    list_display = ('post', 'user')
    search_fields = ('post', 'user')
    list_filter = ('created',)
    ordering = ('-created',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_per_page = 25
    list_select_related = ('post', 'author')
    list_display = ('post', 'author', 'active', 'created')
    list_filter = ('created', 'active')
    search_fields = ('post__title', 'body', 'author__username',)
    fieldsets = (
        (None, {'fields': ('author', )}),
        ('Post title', {'fields': ('post',)}),
        ('Comment', {'fields': ('body',)}),
        ('Status', {'fields': ('active',)}),
    )
    ordering = ('-created',)
    actions = ["make_active", 'make_deactivate']

    @admin.action(description="Activate comment")
    def make_active(self, request, queryset):
        queryset.update(active=True)

    @admin.action(description="Deactivate comment")
    def make_deactivate(self, request, queryset):
        queryset.update(active=False)


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_per_page = 25
    list_display = ('comment', 'user',)
    search_fields = ('comment__body', )
    list_filter = ('user',)


@admin.register(CommentDislike)
class CommentDislikeAdmin(admin.ModelAdmin):
    list_per_page = 25
    list_display = ('comment', 'user',)
    search_fields = ('comment__body', )
    list_filter = ('user',)

