from sqlmodel import Field, Relationship

from seerapi_models.build_model import BaseCategoryModel, BaseResModel, ConvertToORM
from seerapi_models.build_model.comment import APIComment
from seerapi_models.common import (
    EidEffectInUse,
    EidEffectInUseORM,
    ResourceRef,
)


class EffectSeDataBase(BaseResModel):
    name: str = Field(description='名称')
    desc: str = Field(description='描述')


class EffectSeData(EffectSeDataBase):
    effect: EidEffectInUse = Field(description='效果')


class EffectSeDataORM(EffectSeDataBase):
    effect_in_use_id: int | None = Field(
        default=None, foreign_key='eid_effect_in_use.id'
    )


class VariationEffectBase(BaseResModel):
    @classmethod
    def resource_name(cls) -> str:
        return 'pet_variation'


class VariationEffect(
    VariationEffectBase, EffectSeData, ConvertToORM['VariationEffectORM']
):
    """特质效果"""

    @classmethod
    def get_orm_model(cls) -> type['VariationEffectORM']:
        return VariationEffectORM

    def to_orm(self) -> 'VariationEffectORM':
        return VariationEffectORM(
            id=self.id,
            name=self.name,
            desc=self.desc,
            effect_in_use=self.effect.to_orm(),
        )

    @classmethod
    def get_api_comment(cls) -> APIComment:
        return APIComment(
            name_en=cls.resource_name(),
            name_cn='特质效果',
            examples=[
                {
                    'id': 1075,
                    'name': '守护',
                    'desc': '3%几率受到攻击伤害减半',
                    'effect': {
                        'effect_args': [3, 0],
                        'effect': {
                            'id': 404,
                            'url': 'https://api.seerapi.com/v1/eid_effect/404',
                        },
                    },
                    'hash': 'fd1200eb',
                }
            ],
            tags=['精灵', '特质', '特性'],
            description='异能精灵特质效果，该资源的ID字段是一段为特质分配的特性ID区段，从1072开始。',
        )


class VariationEffectORM(VariationEffectBase, EffectSeDataORM, table=True):
    effect_in_use: 'EidEffectInUseORM' = Relationship(
        back_populates='variation_effect',
    )


class PetEffectBase(EffectSeDataBase):
    star_level: int = Field(description='特性星级')

    @classmethod
    def resource_name(cls) -> str:
        return 'pet_effect'


class PetEffect(PetEffectBase, EffectSeData, ConvertToORM['PetEffectORM']):
    effect_group: ResourceRef['PetEffectGroup'] = Field(
        description='特性组资源引用，同特性的不同星级属于同一组'
    )

    @classmethod
    def get_orm_model(cls) -> type['PetEffectORM']:
        return PetEffectORM

    def to_orm(self) -> 'PetEffectORM':
        return PetEffectORM(
            id=self.id,
            name=self.name,
            desc=self.desc,
            effect_in_use=self.effect.to_orm(),
            star_level=self.star_level,
            effect_group_id=self.effect_group.id,
        )

    @classmethod
    def get_api_comment(cls) -> APIComment:
        return APIComment(
            name_en=cls.resource_name(),
            name_cn='特性',
            examples=[
                {
                    'id': 1009,
                    'name': '飞空',
                    'desc': '飞行属性技能威力增加5%',
                    'effect': {
                        'effect_args': [4, 5],
                        'effect': {
                            'id': 28,
                            'url': 'https://api.seerapi.com/v1/eid_effect/28',
                        },
                    },
                    'star_level': 0,
                    'effect_group': {
                        'id': 4,
                        'url': 'https://api.seerapi.com/v1/pet_effect_group/4',
                    },
                    'hash': 'd7952756',
                }
            ],
            tags=['精灵', '特性'],
            description='精灵特性，该资源的ID字段不一定连续。',
        )


class PetEffectORM(PetEffectBase, EffectSeDataORM, table=True):
    effect_in_use: 'EidEffectInUseORM' = Relationship(
        back_populates='pet_effect',
    )
    effect_group_id: int = Field(foreign_key='pet_effect_group.id')
    effect_group: 'PetEffectGroupORM' = Relationship(back_populates='effect')


class PetEffectGroupBase(BaseCategoryModel):
    name: str = Field(description='名称')

    @classmethod
    def resource_name(cls) -> str:
        return 'pet_effect_group'


class PetEffectGroup(PetEffectGroupBase, ConvertToORM['PetEffectGroupORM']):
    effect: list[ResourceRef[PetEffect]] = Field(
        default_factory=list, description='特性列表'
    )

    @classmethod
    def get_orm_model(cls) -> type['PetEffectGroupORM']:
        return PetEffectGroupORM

    def to_orm(self) -> 'PetEffectGroupORM':
        return PetEffectGroupORM(
            id=self.id,
            name=self.name,
        )

    @classmethod
    def get_api_comment(cls) -> APIComment:
        return APIComment(
            name_en=cls.resource_name(),
            name_cn='特性组',
            examples=[
                {
                    'id': 4,
                    'name': '飞空',
                    'effect': [
                        {
                            'id': 1009,
                            'url': 'https://api.seerapi.com/v1/pet_effect/1009',
                        },
                        {
                            'id': 1344,
                            'url': 'https://api.seerapi.com/v1/pet_effect/1344',
                        },
                        {
                            'id': 1345,
                            'url': 'https://api.seerapi.com/v1/pet_effect/1345',
                        },
                        {
                            'id': 1346,
                            'url': 'https://api.seerapi.com/v1/pet_effect/1346',
                        },
                        {
                            'id': 2075,
                            'url': 'https://api.seerapi.com/v1/pet_effect/2075',
                        },
                        {
                            'id': 2076,
                            'url': 'https://api.seerapi.com/v1/pet_effect/2076',
                        },
                    ],
                    'hash': 'da81f2c6',
                }
            ],
            tags=['精灵', '特性', '分类'],
            description='精灵特性组，不同等级的同一特性属于同一组。',
        )


class PetEffectGroupORM(PetEffectGroupBase, table=True):
    effect: list['PetEffectORM'] = Relationship(
        back_populates='effect_group',
    )
