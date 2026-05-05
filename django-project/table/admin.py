from django.contrib import admin
from .models import Table, Feature
from unfold.admin import ModelAdmin, TabularInline


@admin.register(Feature)
class FeatureAdmin(ModelAdmin):
    pass

class FeatureInline(TabularInline):
    model = Table.feature.through
    extra = 0

@admin.register(Table)
class TableAdmin(ModelAdmin):
    list_display = ["number","seats","description"]
    search_fields = ["number","description"]
    list_filter = ["seats"]
    inlines = [FeatureInline]
    fieldsets = [
        (
            None,{"fields":["number","description","image","seats"]},
        )
    ]

