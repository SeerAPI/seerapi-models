from sqlmodel import Field, Relationship

from seerapi_models.build_model import BaseResModel, ConvertToORM
from seerapi_models.build_model.comment import APIComment
from seerapi_models.common import SixAttributes, SixAttributesORMBase


class NatureAttrORM(SixAttributesORMBase, table=True):
    id: int | None = Field(
        default=None,
        primary_key=True,
        foreign_key='nature.id',
        description='性格修正属性ID',
    )
    nature: 'NatureORM' = Relationship(back_populates='attributes')

    @classmethod
    def resource_name(cls) -> str:
        return 'nature_attr'


class BaseNature(BaseResModel):
    name: str = Field(description='性格名称')
    des: str = Field(description='性格描述')
    des2: str = Field(description='性格描述2')

    @classmethod
    def resource_name(cls) -> str:
        return 'nature'


class Nature(BaseNature, ConvertToORM['NatureORM']):
    """精灵性格修正模型"""

    attributes: SixAttributes = Field(description='性格修正属性')

    @classmethod
    def get_orm_model(cls) -> type['NatureORM']:
        return NatureORM

    def to_orm(self) -> 'NatureORM':
        return NatureORM(
            id=self.id,
            name=self.name,
            des=self.des,
            des2=self.des2,
            attributes=NatureAttrORM(
                **self.attributes.model_dump(),
            ),
        )

    @classmethod
    def get_api_comment(cls) -> APIComment:
        return APIComment(
            name_en=cls.resource_name(),
            name_cn='性格',
            examples=[
                {
                    'id': 2,
                    'name': '调皮',
                    'des': '提升攻击 降低特防',
                    'des2': '攻击+10% ,特防-10%',
                    'attributes': {
                        'atk': 1,
                        'def': 0.9,
                        'sp_atk': 1.1,
                        'sp_def': 1,
                        'spd': 1,
                        'hp': 1,
                        'percent': True,
                        'total': 5,
                    },
                    'hash': 'c99d35ae',
                }
            ],
            tags=['性格'],
            description='性格修正资源。',
        )


class NatureORM(BaseNature, table=True):
    attributes: NatureAttrORM = Relationship(back_populates='nature')
