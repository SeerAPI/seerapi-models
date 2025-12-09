from typing import TYPE_CHECKING

from sqlmodel import JSON, Field, Relationship, SQLModel

from seerapi_models.build_model.comment import APIComment

from .build_model import (
    BaseCategoryModel,
    BaseResModel,
    BaseResModelWithOptionalId,
    ConvertToORM,
)
from .common import ResourceRef, SkillEffectInUse, SkillEffectInUseORM

if TYPE_CHECKING:
    from .element_type import TypeCombination, TypeCombinationORM
    from .mintmark import MintmarkORM
    from .pet import Pet, SkillInPetORM


class SkillEffectLink(SQLModel, table=True):
    """技能效果链接表"""

    skill_id: int | None = Field(default=None, foreign_key='skill.id', primary_key=True)
    effect_in_use_id: int | None = Field(
        default=None, foreign_key='skill_effect_in_use.id', primary_key=True
    )


class SkillFriendSkillEffectLink(SQLModel, table=True):
    """伙伴系统强化技能效果链接表"""

    skill_id: int | None = Field(default=None, foreign_key='skill.id', primary_key=True)
    effect_in_use_id: int | None = Field(
        default=None, foreign_key='skill_effect_in_use.id', primary_key=True
    )


class EffectParamLink(SQLModel, table=True):
    """技能效果参数链接表"""

    effect_id: int | None = Field(
        default=None, foreign_key='skill_effect_type.id', primary_key=True
    )
    param_in_type_id: int | None = Field(
        default=None, foreign_key='skill_effect_param_in_type.id', primary_key=True
    )


class SkillEffectTypeTagLink(SQLModel, table=True):
    effect_id: int | None = Field(
        default=None, foreign_key='skill_effect_type.id', primary_key=True
    )
    tag_id: int | None = Field(
        default=None, foreign_key='skill_effect_type_tag.id', primary_key=True
    )


class SkillEffectParam(BaseResModel, ConvertToORM['SkillEffectParamORM']):
    infos: list[str] | None = Field(
        default=None,
        description='参数类型描述列表',
        sa_type=JSON,
    )

    @classmethod
    def resource_name(cls) -> str:
        return 'skill_effect_param'

    @classmethod
    def get_orm_model(cls) -> type['SkillEffectParamORM']:
        return SkillEffectParamORM

    def to_orm(self) -> 'SkillEffectParamORM':
        return SkillEffectParamORM(
            id=self.id,
            infos=self.infos,
        )

    @classmethod
    def get_api_comment(cls) -> APIComment:
        return APIComment(
            name_en=cls.resource_name(),
            name_cn='技能效果参数',
            examples=[
                {
                    'id': 1,
                    'infos': [
                        '麻痹',
                        '中毒',
                        '烧伤',
                        '',
                        '寄生',
                        '冻伤',
                        '害怕',
                        '疲惫',
                        '睡眠',
                        '石化',
                        '混乱',
                        '衰弱',
                        '山神守护',
                        '易燃',
                        '狂暴',
                        '冰封',
                        '流血',
                        'XX',
                        'XX',
                        '瘫痪',
                        '失明',
                        'XX',
                        '焚烬',
                        '诅咒',
                        '烈焰诅咒',
                        '致命诅咒',
                        '虚弱诅咒',
                        '感染',
                        '束缚',
                        '失神',
                        '沉默',
                        '臣服',
                        '凝滞',
                        '星赐',
                        '星哲',
                        '超频',
                        '沸涌',
                        '砥砺',
                        '星赎',
                        '神游',
                    ],
                    'hash': '50e3ccd1',
                }
            ],
            tags=['技能', '技能效果'],
            description='技能效果参数，该资源描述了用于格式化技能效果描述的内部参数。',
        )


class SkillEffectParamORM(SkillEffectParam, table=True):
    in_type: list['SkillEffectParamInTypeORM'] = Relationship(
        back_populates='param',
    )


class SkillEffectParamInTypeBase(BaseResModelWithOptionalId):
    position: int = Field(description='参数位置')

    @classmethod
    def resource_name(cls) -> str:
        return 'skill_effect_param_in_type'


class SkillEffectParamInType(
    SkillEffectParamInTypeBase, ConvertToORM['SkillEffectParamInTypeORM']
):
    param: ResourceRef[SkillEffectParam] = Field(description='参数类型引用')

    @classmethod
    def get_orm_model(cls) -> type['SkillEffectParamInTypeORM']:
        return SkillEffectParamInTypeORM

    def to_orm(self) -> 'SkillEffectParamInTypeORM':
        return SkillEffectParamInTypeORM(
            id=self.id,
            param_id=self.param.id,
            position=self.position,
        )


class SkillEffectParamInTypeORM(SkillEffectParamInTypeBase, table=True):
    param_id: int = Field(foreign_key='skill_effect_param.id')
    param: 'SkillEffectParamORM' = Relationship(back_populates='in_type')
    effect: 'SkillEffectTypeORM' = Relationship(
        back_populates='param', link_model=EffectParamLink
    )


class SkillEffectTypeBase(BaseResModel):
    """描述一条技能效果类型"""

    args_num: int = Field(description='参数数量')
    info: str = Field(description='效果描述')
    info_formatting_adjustment: str | None = Field(
        default=None,
        description='效果描述的"可格式化版本"，用于呈现Unity端中的多行描述形式',
    )
    pve_effective: bool = Field(description='该效果是否PVE生效')

    @classmethod
    def resource_name(cls) -> str:
        return 'skill_effect_type'


class SkillEffectType(SkillEffectTypeBase, ConvertToORM['SkillEffectTypeORM']):
    param: list[SkillEffectParamInType] | None = Field(
        default=None, description='参数类型列表，描述参数类型和参数位置'
    )
    skill: list[ResourceRef['Skill']] = Field(
        default_factory=list, description='使用该效果的技能列表'
    )
    tag: list[ResourceRef['SkillEffectTypeTag']] = Field(
        default_factory=list, description='标签列表'
    )

    @classmethod
    def get_orm_model(cls) -> type['SkillEffectTypeORM']:
        return SkillEffectTypeORM

    def to_orm(self) -> 'SkillEffectTypeORM':
        return SkillEffectTypeORM(
            id=self.id,
            args_num=self.args_num,
            info=self.info,
            pve_effective=self.pve_effective,
            info_formatting_adjustment=self.info_formatting_adjustment,
        )

    @classmethod
    def get_api_comment(cls) -> APIComment:
        return APIComment(
            name_en=cls.resource_name(),
            name_cn='技能效果',
            examples=[
                {
                    'id': 1000,
                    'args_num': 3,
                    'info': '命中则{0}%使对手{1}，未触发则附加{2}点固定伤害',
                    'info_formatting_adjustment': '命中则{0}%使对手{1}\r\n--\u003e\u003ccondition\u003e未触发\u003c/condition\u003e则附加{2}点固定伤害',
                    'pve_effective': False,
                    'param': [
                        {
                            'position': 1,
                            'param': {
                                'id': 1,
                                'url': 'https://api.seerapi.com/v1/skill_effect_param/1',
                            },
                        }
                    ],
                    'skill': [
                        {'id': 25004, 'url': 'https://api.seerapi.com/v1/skill/25004'},
                        {'id': 25570, 'url': 'https://api.seerapi.com/v1/skill/25570'},
                        {'id': 30018, 'url': 'https://api.seerapi.com/v1/skill/30018'},
                        {'id': 32113, 'url': 'https://api.seerapi.com/v1/skill/32113'},
                        {'id': 32975, 'url': 'https://api.seerapi.com/v1/skill/32975'},
                        {'id': 33419, 'url': 'https://api.seerapi.com/v1/skill/33419'},
                        {'id': 33845, 'url': 'https://api.seerapi.com/v1/skill/33845'},
                        {'id': 36125, 'url': 'https://api.seerapi.com/v1/skill/36125'},
                        {'id': 37377, 'url': 'https://api.seerapi.com/v1/skill/37377'},
                        {'id': 37895, 'url': 'https://api.seerapi.com/v1/skill/37895'},
                    ],
                    'tag': [
                        {
                            'id': 813,
                            'url': 'https://api.seerapi.com/v1/skill_effect_type_tag/813',
                        },
                        {
                            'id': 60828,
                            'url': 'https://api.seerapi.com/v1/skill_effect_type_tag/60828',
                        },
                    ],
                    'hash': 'fbb4ef75',
                }
            ],
            tags=['技能', '技能效果'],
            description='技能效果。',
        )


class SkillEffectTypeORM(SkillEffectTypeBase, table=True):
    param: list['SkillEffectParamInTypeORM'] = Relationship(
        back_populates='effect', link_model=EffectParamLink
    )
    tag: list['SkillEffectTypeTagORM'] = Relationship(
        back_populates='effect', link_model=SkillEffectTypeTagLink
    )
    in_use: list['SkillEffectInUseORM'] = Relationship(back_populates='effect')


class SkillCategoryBase(BaseCategoryModel):
    name: str = Field(description='技能分类名称')

    @classmethod
    def resource_name(cls) -> str:
        return 'skill_category'


class SkillCategory(SkillCategoryBase, ConvertToORM['SkillCategoryORM']):
    skill: list[ResourceRef['Skill']] = Field(
        default_factory=list, description='使用该分类的技能列表'
    )

    @classmethod
    def get_orm_model(cls) -> type['SkillCategoryORM']:
        return SkillCategoryORM

    def to_orm(self) -> 'SkillCategoryORM':
        return SkillCategoryORM(
            id=self.id,
            name=self.name,
        )

    @classmethod
    def get_api_comment(cls) -> APIComment:
        return APIComment(
            name_en=cls.resource_name(),
            name_cn='技能分类',
            examples=[
                {
                    'id': 1,
                    'name': '物理攻击',
                    'skill': [
                        {'id': 10001, 'url': 'https://api.seerapi.com/v1/skill/10001'},
                        {'id': 10003, 'url': 'https://api.seerapi.com/v1/skill/10003'},
                        {'id': 10004, 'url': 'https://api.seerapi.com/v1/skill/10004'},
                    ],
                    'hash': '67in0p9v',
                },
            ],
            tags=['技能', '分类'],
            description='技能分类，用于分类物理/特殊/属性技能。',
        )


class SkillCategoryORM(SkillCategoryBase, table=True):
    skill: list['SkillORM'] = Relationship(back_populates='category')


class SkillHideEffectBase(BaseCategoryModel):
    name: str = Field(description='技能隐藏效果名称')
    description: str = Field(description='技能隐藏效果描述')

    @classmethod
    def resource_name(cls) -> str:
        return 'skill_hide_effect'


class SkillHideEffect(SkillHideEffectBase, ConvertToORM['SkillHideEffectORM']):
    skill: list[ResourceRef['Skill']] = Field(
        default_factory=list, description='使用该隐藏效果的技能列表'
    )

    @classmethod
    def get_orm_model(cls) -> type['SkillHideEffectORM']:
        return SkillHideEffectORM

    def to_orm(self) -> 'SkillHideEffectORM':
        return SkillHideEffectORM(
            id=self.id,
            name=self.name,
            description=self.description,
        )

    @classmethod
    def get_api_comment(cls) -> APIComment:
        return APIComment(
            name_en=cls.resource_name(),
            name_cn='技能隐藏效果',
            examples=[
                {
                    'id': 1,
                    'name': 'crit_atk_first',
                    'description': '先出手时必定暴击',
                    'skill': [
                        {'id': 10367, 'url': 'https://api.seerapi.com/v1/skill/10367'},
                        {'id': 15478, 'url': 'https://api.seerapi.com/v1/skill/15478'},
                        {'id': 15913, 'url': 'https://api.seerapi.com/v1/skill/15913'},
                        {'id': 16040, 'url': 'https://api.seerapi.com/v1/skill/16040'},
                    ],
                    'hash': '32045f52',
                }
            ],
            tags=['技能', '技能效果'],
            description='技能隐藏效果，该资源描述了技能的特殊隐藏效果，'
            '例如精灵“速度史莱姆”的技能“迅捷撞击”，效果为“若先出手则必定打出致命一击（CritAtkFirst）”。',
        )


class SkillHideEffectORM(SkillHideEffectBase, table=True):
    skill: list['SkillORM'] = Relationship(back_populates='hide_effect')


class SkillEffectTypeTagBase(BaseCategoryModel):
    name: str = Field(description='标签名称')

    @classmethod
    def resource_name(cls) -> str:
        return 'skill_effect_type_tag'


class SkillEffectTypeTag(SkillEffectTypeTagBase, ConvertToORM['SkillEffectTypeTagORM']):
    effect: list[ResourceRef['SkillEffectType']] = Field(
        default_factory=list, description='技能效果类型列表'
    )

    @classmethod
    def get_orm_model(cls) -> type['SkillEffectTypeTagORM']:
        return SkillEffectTypeTagORM

    def to_orm(self) -> 'SkillEffectTypeTagORM':
        return SkillEffectTypeTagORM(id=self.id, name=self.name)

    @classmethod
    def get_api_comment(cls) -> APIComment:
        return APIComment(
            name_en=cls.resource_name(),
            name_cn='技能效果类型标签',
            examples=[
                {
                    'id': 5734,
                    'name': '消除护罩',
                    'effect': [
                        {
                            'id': 1828,
                            'url': 'https://api.seerapi.com/v1/skill_effect_type/1828',
                        },
                        {
                            'id': 1989,
                            'url': 'https://api.seerapi.com/v1/skill_effect_type/1989',
                        },
                        {
                            'id': 2311,
                            'url': 'https://api.seerapi.com/v1/skill_effect_type/2311',
                        },
                    ],
                    'hash': '1a4fb8eb',
                }
            ],
            tags=['技能', '技能效果', '分类'],
            description='技能效果类型标签，该资源的ID字段是分析器自行生成的，在数据中并不存在。',
        )


class SkillEffectTypeTagORM(SkillEffectTypeTagBase, table=True):
    effect: list['SkillEffectTypeORM'] = Relationship(
        back_populates='tag', link_model=SkillEffectTypeTagLink
    )


class SkillBase(BaseResModel):
    name: str = Field(description='技能名称')
    power: int = Field(description='技能威力')
    max_pp: int = Field(description='技能最大PP')
    accuracy: int = Field(description='技能命中率')
    crit_rate: float | None = Field(
        description='技能暴击率, 该技能无法暴击时为null（例如属性技能）'
    )
    priority: int = Field(description='技能优先级')
    must_hit: bool = Field(description='技能是否必定命中')
    atk_num: int = Field(default=1, description='组队对战中技能可作用目标数量，默认为1')
    info: str | None = Field(default=None, description='技能描述')

    @classmethod
    def resource_name(cls) -> str:
        return 'skill'


class Skill(SkillBase, ConvertToORM['SkillORM']):
    category: ResourceRef[SkillCategory] = Field(description='技能分类')
    type: ResourceRef['TypeCombination'] = Field(description='技能属性')
    learned_by_pet: list[ResourceRef['Pet']] = Field(
        default_factory=list, description='可学习该技能的精灵列表'
    )
    skill_effect: list[SkillEffectInUse] = Field(
        default_factory=list, description='技能效果列表'
    )
    friend_skill_effect: list[SkillEffectInUse] = Field(
        default_factory=list,
        description='旧版伙伴系统强化后的技能效果',
    )
    hide_effect: ResourceRef[SkillHideEffect] | None = Field(
        default=None, description='技能隐藏效果'
    )
    # mintmark: list[ResourceRef['SkillMintmark']] = Field(
    # 	default_factory=list, description='技能刻印列表'
    # )

    @classmethod
    def get_orm_model(cls) -> 'type[SkillORM]':
        return SkillORM

    def to_orm(self) -> 'SkillORM':
        return SkillORM(
            id=self.id,
            name=self.name,
            power=self.power,
            max_pp=self.max_pp,
            accuracy=self.accuracy,
            crit_rate=self.crit_rate,
            priority=self.priority,
            must_hit=self.must_hit,
            info=self.info,
            category_id=self.category.id,
            type_id=self.type.id,
            hide_effect_id=self.hide_effect.id if self.hide_effect else None,
            atk_num=self.atk_num,
        )

    @classmethod
    def get_api_comment(cls) -> APIComment:
        return APIComment(
            name_en=cls.resource_name(),
            name_cn='技能',
            examples=[
                {
                    'id': 38088,
                    'name': '圣武·虚极拓世',
                    'power': 160,
                    'max_pp': 5,
                    'accuracy': 95,
                    'crit_rate': 6.25,
                    'priority': 0,
                    'must_hit': True,
                    'atk_num': 1,
                    'info': None,
                    'category': {
                        'id': 1,
                        'url': 'https://api.seerapi.com/v1/skill_category/1',
                    },
                    'type': {
                        'id': 129,
                        'url': 'https://api.seerapi.com/v1/element_type_combination/129',
                    },
                    'learned_by_pet': [],
                    'skill_effect': [
                        {
                            'info': '若先出手则必定打出致命一击',
                            'args': [],
                            'effect': {
                                'id': 1395,
                                'url': 'https://api.seerapi.com/v1/skill_effect_type/1395',
                            },
                        },
                        {
                            'info': '对手每处于1回合的威怯1回合内令对手技能无效',
                            'args': [],
                            'effect': {
                                'id': 2343,
                                'url': 'https://api.seerapi.com/v1/skill_effect_type/2343',
                            },
                        },
                        {
                            'info': '下1回合自身造成的攻击伤害翻倍',
                            'args': [1],
                            'effect': {
                                'id': 776,
                                'url': 'https://api.seerapi.com/v1/skill_effect_type/776',
                            },
                        },
                        {
                            'info': '附加对手最大体力1/3的百分比伤害，未击败对手则恢复自身等量体力值',
                            'args': [3],
                            'effect': {
                                'id': 1709,
                                'url': 'https://api.seerapi.com/v1/skill_effect_type/1709',
                            },
                        },
                        {
                            'info': '击败对手后自身免疫下2次受到的异常状态',
                            'args': [2],
                            'effect': {
                                'id': 2252,
                                'url': 'https://api.seerapi.com/v1/skill_effect_type/2252',
                            },
                        },
                    ],
                    'friend_skill_effect': [],
                    'hide_effect': None,
                    'hash': '5254529c',
                }
            ],
            tags=['技能'],
            description='技能资源，包含所有技能数据。',
        )


class SkillORM(SkillBase, table=True):
    category_id: int = Field(foreign_key='skill_category.id')
    category: SkillCategoryORM = Relationship(back_populates='skill')
    type_id: int = Field(foreign_key='element_type_combination.id')
    type: 'TypeCombinationORM' = Relationship(
        back_populates='skill',
    )
    mintmark: list['MintmarkORM'] = Relationship(
        back_populates='skill',
        sa_relationship_kwargs={
            'secondary': 'skillmintmarklink',
        },
    )
    skill_effect: list[SkillEffectInUseORM] = Relationship(
        back_populates='skill', link_model=SkillEffectLink
    )
    friend_skill_effect: list[SkillEffectInUseORM] = Relationship(
        back_populates='skill', link_model=SkillFriendSkillEffectLink
    )
    hide_effect_id: int | None = Field(default=None, foreign_key='skill_hide_effect.id')
    hide_effect: SkillHideEffectORM | None = Relationship(back_populates='skill')

    pet_links: list['SkillInPetORM'] = Relationship(
        back_populates='skill',
    )
