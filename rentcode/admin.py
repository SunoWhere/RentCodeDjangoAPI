from django.contrib import admin

from rentcode.models import Code, ProgrammingLanguage

# Register your models here.
@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    list_display = ["name", "execution_time"]
    autocomplete_fields = ["language"]


@admin.register(ProgrammingLanguage)
class ProgrammingLanguageAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]