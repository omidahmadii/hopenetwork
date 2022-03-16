from django.contrib import admin
from .models import Article, Category
from django.contrib import messages
from django.utils.translation import ngettext

admin.site.site_header = 'وبلاگ'


@admin.action(description='انتشار مقالات انتخاب شده ')
def make_published(modeladmin, request, queryset):
    updated = queryset.update(status='p')
    modeladmin.message_user(request, ngettext(
        '%d  مقاله با موفقیت منتشر شد.',
        '%d مقاله با موفقیت منتشر شدند .',
        updated,
    ) % updated, messages.SUCCESS)


@admin.action(description='پیش نویس کردن  مقالات انتخاب شده')
def make_draft(modeladmin, request, queryset):
    updated = queryset.update(status='d')
    modeladmin.message_user(request, ngettext(
        '%d  مقاله با موفقیت پیش نویس شد.',
        '%d مقاله با موفقیت پیش نویس شدند .',
        updated,
    ) % updated, messages.SUCCESS)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug','parent', 'position', 'status')
    list_filter = (['status'])
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    ordering = (['parent__id'])


admin.site.register(Category, CategoryAdmin)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'thumbnail_tag', 'slug', 'author', 'jpublish', 'status', 'category_to_str')
    list_filter = ('publish', 'status', 'author')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('status', '-publish')
    actions = [make_published, make_draft]

    def category_to_str(self, obj):
        return ", ".join([category.title for category in obj.category.active()])

    category_to_str.short_description = "دسته بندی"


admin.site.register(Article, ArticleAdmin)
