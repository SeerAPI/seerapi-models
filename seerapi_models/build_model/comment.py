from pydantic import BaseModel, Field


class APIComment(BaseModel):
    """模型的 OpenAPI 说明注释"""

    name_en: str = Field(description='模型英文名称')
    name_cn: str = Field(description='模型中文名称，用于生成 summary 字段')
    examples: list = Field(
        description='模型对象示例，将被写入到 OpenAPI 模型中的 examples 字段中'
    )
    tags: list[str] = Field(
        description='模型所属的标签，将被写入到该模型相关请求操作 的 tags 字段中'
    )
    description: str = Field(
        description='模型描述，将被写入到该模型相关请求操作的 description 字段中'
    )
