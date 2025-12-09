from sqlmodel import Field, Relationship, SQLModel

from seerapi_models.build_model import BaseCategoryModel, BaseResModel, ConvertToORM
from seerapi_models.build_model.comment import APIComment
from seerapi_models.common import ResourceRef


class BattleEffectCategoryLink(SQLModel, table=True):
    battle_effect_id: int | None = Field(
        default=None, foreign_key='battle_effect.id', primary_key=True
    )
    type_id: int | None = Field(
        default=None, foreign_key='battle_effect_type.id', primary_key=True
    )


class BattleEffectBase(BaseResModel):
    name: str = Field(description='状态名称')
    desc: str = Field(description='状态描述')

    @classmethod
    def resource_name(cls) -> str:
        return 'battle_effect'


class BattleEffect(BattleEffectBase, ConvertToORM['BattleEffectORM']):
    type: list[ResourceRef['BattleEffectCategory']] = Field(
        default_factory=list,
        description='状态类型，可能同时属于多个类型，例如瘫痪同时属于控制类和限制类异常',
    )

    @classmethod
    def get_orm_model(cls) -> 'type[BattleEffectORM]':
        return BattleEffectORM

    def to_orm(self) -> 'BattleEffectORM':
        return BattleEffectORM(
            id=self.id,
            name=self.name,
            desc=self.desc,
        )

    @classmethod
    def get_api_comment(cls) -> APIComment:
        return APIComment(
            name_en=cls.resource_name(),
            name_cn='状态',
            examples=[
                {
                    'id': 20,
                    'name': '失明',
                    'desc': '弱化类异常状态，该状态下精灵使用攻击技能50%miss，若为必中技能则50%命中效果失效且无法造成攻击伤害',
                    'type': [
                        {
                            'id': 1,
                            'url': 'https://api.seerapi.com/v1/battle_effect_type/1',
                        }
                    ],
                    'hash': 'fa7cf7b',
                }
            ],
            tags=['战斗状态', '异常状态'],
            description='战斗状态资源，包含所有战斗状态（也就是异常状态）数据。',
        )


class BattleEffectORM(BattleEffectBase, table=True):
    type: list['BattleEffectCategoryORM'] = Relationship(
        back_populates='effect', link_model=BattleEffectCategoryLink
    )


class BattleEffectCategoryBase(BaseCategoryModel):
    name: str = Field(description='状态类型名称')

    @classmethod
    def resource_name(cls) -> str:
        return 'battle_effect_type'


class BattleEffectCategory(
    BattleEffectCategoryBase, ConvertToORM['BattleEffectCategoryORM']
):
    effect: list[ResourceRef['BattleEffect']] = Field(
        default_factory=list, description='异常状态列表'
    )

    @classmethod
    def get_orm_model(cls) -> type['BattleEffectCategoryORM']:
        return BattleEffectCategoryORM

    def to_orm(self) -> 'BattleEffectCategoryORM':
        return BattleEffectCategoryORM(
            id=self.id,
            name=self.name,
        )

    @classmethod
    def get_api_comment(cls) -> APIComment:
        return APIComment(
            name_en=cls.resource_name(),
            name_cn='状态类型',
            examples=[
                {
                    'id': 3,
                    'name': '限制类',
                    'effect': [
                        {
                            'id': 19,
                            'url': 'https://api.seerapi.com/v1/battle_effect/19',
                        },
                        {
                            'id': 32,
                            'url': 'https://api.seerapi.com/v1/battle_effect/32',
                        },
                        {
                            'id': 38,
                            'url': 'https://api.seerapi.com/v1/battle_effect/38',
                        },
                    ],
                    'hash': 'ad1a9de2',
                }
            ],
            tags=['战斗状态', '异常状态', '分类'],
            description='战斗状态分类，用于分类不同类型的战斗状态。',
        )


class BattleEffectCategoryORM(BattleEffectCategoryBase, table=True):
    effect: list['BattleEffectORM'] = Relationship(
        back_populates='type', link_model=BattleEffectCategoryLink
    )
