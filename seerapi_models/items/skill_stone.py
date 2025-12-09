from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from seerapi_models.build_model import (
    BaseCategoryModel,
    BaseResModel,
    ConvertToORM,
)
from seerapi_models.build_model.comment import APIComment
from seerapi_models.common import ResourceRef, SkillEffectInUse, SkillEffectInUseORM

from ._common import Item, ItemORM

if TYPE_CHECKING:
    from ..element_type import TypeCombination, TypeCombinationORM


class SkillStoneEffectLink(SQLModel, table=True):
    """技能石效果链接表"""

    skill_stone_effect_id: int | None = Field(
        default=None, foreign_key='skill_stone_effect.id', primary_key=True
    )
    effect_in_use_id: int | None = Field(
        default=None, foreign_key='skill_effect_in_use.id', primary_key=True
    )


class SkillStoneEffectBase(BaseResModelWithOptionalId):
    prob: float = Field(description='技能石效果激活概率，0到1之间')

    @classmethod
    def resource_name(cls) -> str:
        return 'skill_stone_effect'


class SkillStoneEffect(SkillStoneEffectBase):
    effect: list['SkillEffectInUse'] = Field(description='技能石效果列表')


class SkillStoneEffectORM(SkillStoneEffectBase, table=True):
    effect: list['SkillEffectInUseORM'] = Relationship(
        back_populates='skill_stone_effect',
        link_model=SkillStoneEffectLink,
    )
    skill_stone_id: int = Field(foreign_key='skill_stone.id')
    skill_stone: 'SkillStoneORM' = Relationship(back_populates='effect')


class SkillStoneBase(BaseResModel):
    id: int = Field(primary_key=True, description='技能石ID')
    name: str = Field(description='技能石名称')
    rank: int = Field(description='技能石等级，1到5分别对应D, C, B, A, S')
    power: int = Field(description='技能石威力')
    max_pp: int = Field(description='技能石最大PP')
    accuracy: int = Field(description='技能石命中率')

    @classmethod
    def resource_name(cls) -> str:
        return 'skill_stone'


class SkillStone(SkillStoneBase, ConvertToORM['SkillStoneORM']):
    category: ResourceRef['SkillStoneCategory'] = Field(description='技能石分类')
    item: ResourceRef['Item'] = Field(description='技能石物品资源引用')
    effect: list['SkillStoneEffect'] = Field(description='完美技能石效果列表')

    @classmethod
    def get_orm_model(cls) -> type['SkillStoneORM']:
        return SkillStoneORM

    def to_orm(self) -> 'SkillStoneORM':
        effect_orms = [
            SkillStoneEffectORM(
                id=effect.id,
                prob=effect.prob,
                skill_stone_id=self.id,
                effect=[e.to_orm() for e in effect.effect],
            )
            for effect in self.effect
        ]
        return SkillStoneORM(
            id=self.id,
            item_id=self.item.id,
            name=self.name,
            rank=self.rank,
            power=self.power,
            max_pp=self.max_pp,
            accuracy=self.accuracy,
            category_id=self.category.id,
            effect=effect_orms,
        )

    @classmethod
    def get_api_comment(cls) -> APIComment:
        return APIComment(
            name_en=cls.resource_name(),
            name_cn='技能石',
            examples=[
                {
                    'id': 102,
                    'name': 'C级虫系技能石',
                    'rank': 2,
                    'power': 60,
                    'max_pp': 25,
                    'accuracy': 100,
                    'category': {
                        'id': 225,
                        'url': 'https://api.seerapi.com/v1/skill_stone_category/225',
                    },
                    'item': {
                        'id': 1100102,
                        'url': 'https://api.seerapi.com/v1/item/1100102',
                    },
                    'effect': [
                        {
                            'prob': 0.15,
                            'effect': [
                                {
                                    'info': '10%降低对手所有技能1点PP值，然后若对手所选择的技能PP值为0则当回合对手无法行动',
                                    'args': [10, 1],
                                    'effect': {
                                        'id': 39,
                                        'url': 'https://api.seerapi.com/v1/skill_effect_type/39',
                                    },
                                }
                            ],
                        },
                        {
                            'prob': 0.06,
                            'effect': [
                                {
                                    'info': '技能使用成功时，15%改变自身攻击等级+1',
                                    'args': [0, 15, 1],
                                    'effect': {
                                        'id': 4,
                                        'url': 'https://api.seerapi.com/v1/skill_effect_type/4',
                                    },
                                }
                            ],
                        },
                        {
                            'prob': 0.06,
                            'effect': [
                                {
                                    'info': '技能使用成功时，15%改变自身防御等级+1',
                                    'args': [1, 15, 1],
                                    'effect': {
                                        'id': 4,
                                        'url': 'https://api.seerapi.com/v1/skill_effect_type/4',
                                    },
                                }
                            ],
                        },
                        {
                            'prob': 0.06,
                            'effect': [
                                {
                                    'info': '技能使用成功时，15%改变自身特攻等级+1',
                                    'args': [2, 15, 1],
                                    'effect': {
                                        'id': 4,
                                        'url': 'https://api.seerapi.com/v1/skill_effect_type/4',
                                    },
                                }
                            ],
                        },
                        {
                            'prob': 0.06,
                            'effect': [
                                {
                                    'info': '技能使用成功时，15%改变自身特防等级+1',
                                    'args': [3, 15, 1],
                                    'effect': {
                                        'id': 4,
                                        'url': 'https://api.seerapi.com/v1/skill_effect_type/4',
                                    },
                                }
                            ],
                        },
                        {
                            'prob': 0.06,
                            'effect': [
                                {
                                    'info': '技能使用成功时，15%改变自身速度等级+1',
                                    'args': [4, 15, 1],
                                    'effect': {
                                        'id': 4,
                                        'url': 'https://api.seerapi.com/v1/skill_effect_type/4',
                                    },
                                }
                            ],
                        },
                        {
                            'prob': 0.06,
                            'effect': [
                                {
                                    'info': '技能使用成功时，15%改变自身命中等级+1',
                                    'args': [5, 15, 1],
                                    'effect': {
                                        'id': 4,
                                        'url': 'https://api.seerapi.com/v1/skill_effect_type/4',
                                    },
                                }
                            ],
                        },
                    ],
                    'hash': '103a6f69',
                }
            ],
            tags=['技能石', '技能', '道具'],
            description='技能石资源，包含完美技能石的特殊效果和获得概率。',
        )


class SkillStoneORM(SkillStoneBase, table=True):
    category_id: int = Field(
        description='技能石分类ID', foreign_key='skill_stone_category.id'
    )
    category: 'SkillStoneCategoryORM' = Relationship(
        back_populates='skill_stone',
    )
    item_id: int = Field(foreign_key='item.id')
    item: 'ItemORM' = Relationship(
        back_populates='skill_stone',
    )
    effect: list['SkillStoneEffectORM'] = Relationship(
        back_populates='skill_stone',
    )


class SkillStoneCategoryBase(BaseCategoryModel):
    name: str = Field(description='技能石分类名称')

    @classmethod
    def resource_name(cls) -> str:
        return 'skill_stone_category'


class SkillStoneCategory(SkillStoneCategoryBase, ConvertToORM['SkillStoneCategoryORM']):
    skill_stone: list[ResourceRef['SkillStone']] = Field(
        default_factory=list,
        description='技能石列表',
    )
    type: ResourceRef['TypeCombination'] = Field(description='技能石类型')

    @classmethod
    def get_api_comment(cls) -> APIComment:
        return APIComment(
            name_en=cls.resource_name(),
            name_cn='技能石分类',
            examples=[
                {
                    'id': 225,
                    'name': '虫系技能石',
                    'skill_stone': [
                        {
                            'id': 105,
                            'url': 'https://api.seerapi.com/v1/skill_stone/105',
                        },
                        {
                            'id': 104,
                            'url': 'https://api.seerapi.com/v1/skill_stone/104',
                        },
                        {
                            'id': 103,
                            'url': 'https://api.seerapi.com/v1/skill_stone/103',
                        },
                        {
                            'id': 102,
                            'url': 'https://api.seerapi.com/v1/skill_stone/102',
                        },
                        {
                            'id': 101,
                            'url': 'https://api.seerapi.com/v1/skill_stone/101',
                        },
                    ],
                    'type': {
                        'id': 225,
                        'url': 'https://api.seerapi.com/v1/element_type_combination/225',
                    },
                    'hash': '6c9c1de',
                }
            ],
            tags=['技能石', '技能', '道具', '分类'],
            description='技能石分类，用于分类不同属性的技能石。'
            '注意该资源的 ID 字段值为该技能石的属性的 ID',
        )

    @classmethod
    def get_orm_model(cls) -> 'type[SkillStoneCategoryORM]':
        return SkillStoneCategoryORM

    def to_orm(self) -> 'SkillStoneCategoryORM':
        return SkillStoneCategoryORM(
            id=self.id,
            name=self.name,
            type_id=self.type.id,
        )


class SkillStoneCategoryORM(SkillStoneCategoryBase, table=True):
    type_id: int = Field(
        description='技能石类型ID', foreign_key='element_type_combination.id'
    )
    type: 'TypeCombinationORM' = Relationship(
        back_populates='skill_stone_category',
    )
    skill_stone: list['SkillStoneORM'] = Relationship(
        back_populates='category',
    )
