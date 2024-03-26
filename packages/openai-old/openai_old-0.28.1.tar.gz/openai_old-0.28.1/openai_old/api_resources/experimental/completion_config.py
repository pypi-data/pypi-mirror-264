from openai_old.api_resources.abstract import (
    CreateableAPIResource,
    DeletableAPIResource,
    ListableAPIResource,
)


class CompletionConfig(
    CreateableAPIResource, ListableAPIResource, DeletableAPIResource
):
    OBJECT_NAME = "experimental.completion_configs"
