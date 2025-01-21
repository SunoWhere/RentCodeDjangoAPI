from django.shortcuts import get_object_or_404
from ninja import Query
from ninja_extra import ControllerBase, api_controller, route

from rentcode.models import Code, ProgrammingLanguage
from rentcode.schemas import CodeFilterSchema, CodeMinSchema, CodeSchema, ProgrammingLanguageSchema


@api_controller("/code")
class CodeController(ControllerBase):
    @route.get("", response=list[CodeSchema])
    def search_codes(self, filters: Query[CodeFilterSchema]):
        return filters.filter(Code.objects.select_related("language"))

    @route.get("/{code_id}", response=CodeSchema)
    def get_code(self, code_id: int):
        return get_object_or_404(Code, id=code_id)
    

@api_controller("/programming-language")
class ProgrammingLanguageController(ControllerBase):
    @route.get("", response=list[ProgrammingLanguageSchema])
    def search_programming_languages(self):
        return ProgrammingLanguage.objects.all()