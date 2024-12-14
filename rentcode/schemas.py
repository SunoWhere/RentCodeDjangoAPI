from datetime import timedelta
from ninja import Field, FilterSchema, ModelSchema

from rentcode.models import Code


class CodeSchema(ModelSchema):
    class Meta:
        model = Code
        fields = ["id", "name", "code", "price", "execution_time"]
    
    language: str

    @staticmethod
    def resolve_language(obj) -> str:
        return obj.language.name
    

class CodeMinSchema(ModelSchema):
    class Meta:
        model = Code
        fields = ["id", "name", "price"]

    language: str

    @staticmethod
    def resolve_language(obj) -> str:
        return obj.language.name
    

class CodeToCartSchema(ModelSchema):
    class Meta:
        model = Code
        fields = ["id"]


class CodeFilterSchema(FilterSchema):
    name: str | None = Field(None, q="name__icontains")
    language: set[int] | None = Field(None, q="language__in")
    execution_time_gt: timedelta | None = Field(None, q="execution_time__gt")


class ProgrammingLanguageSchema(FilterSchema):
    name: str
    logo: str