from typing import TYPE_CHECKING, Optional

from pydantic import AliasChoices
from sqlmodel import Field, Relationship, SQLModel

from seerapi_models.build_model import (
    BaseCategoryModel,
    BaseResModel,
    ConvertToORM,
)
from seerapi_models.build_model.comment import APIComment
from seerapi_models.common import EidEffectInUse, EidEffectInUseORM, ResourceRef

if TYPE_CHECKING:
    from .pet import Pet, PetORM


class PetSoulmarkLink(SQLModel, table=True):
    pet_id: int | None = Field(default=None, primary_key=True, foreign_key='pet.id')
    soulmark_id: int | None = Field(
        default=None, primary_key=True, foreign_key='soulmark.id'
    )


class SoulmarkTagLink(SQLModel, table=True):
    soulmark_id: int | None = Field(
        default=None, primary_key=True, foreign_key='soulmark.id'
    )
    tag_id: int | None = Field(
        default=None, primary_key=True, foreign_key='soulmark_tag.id'
    )


class SoulmarkBase(BaseResModel):
    desc: str = Field(description='魂印描述')
    desc_formatting_adjustment: str | None = Field(
        default=None,
        description='魂印描述的"可格式化版本"，用于呈现Unity端中的描述排版形式',
    )
    pve_effective: bool | None = Field(
        default=None,
        description='该魂印是否PVE生效，如果为null则表示无法通过数据层面推断其是否生效',
    )
    intensified: bool = Field(description='是否是强化的魂印')
    is_adv: bool = Field(description='是否是神谕觉醒魂印')

    @classmethod
    def resource_name(cls) -> str:
        return 'soulmark'


class Soulmark(SoulmarkBase, ConvertToORM['SoulmarkORM']):
    pet: list[ResourceRef['Pet']] = Field(description='可持有该魂印的精灵ID')
    effect: EidEffectInUse | None = Field(description='魂印效果')
    tag: list[ResourceRef['SoulmarkTagCategory']] = Field(
        description='魂印标签，例如强攻，断回合等'
    )
    intensified_to: ResourceRef['Soulmark'] | None = Field(
        description='强化后的魂印资源，该字段仅在该魂印有强化版时有效，否则为null'
    )
    from_: ResourceRef['Soulmark'] | None = Field(
        description='强化前的魂印资源，该字段仅在该魂印是强化/觉醒魂印时有效',
        schema_extra={
            'serialization_alias': 'from',
            'validation_alias': AliasChoices('from', 'from_'),
        },
    )

    @classmethod
    def get_orm_model(cls) -> type['SoulmarkORM']:
        return SoulmarkORM

    def to_orm(self) -> 'SoulmarkORM':
        return SoulmarkORM(
            id=self.id,
            desc=self.desc,
            intensified=self.intensified,
            is_adv=self.is_adv,
            effect_in_use=self.effect.to_orm() if self.effect else None,
            intensified_to_id=self.intensified_to.id if self.intensified_to else None,
            desc_formatting_adjustment=self.desc_formatting_adjustment,
            pve_effective=self.pve_effective,
        )

    @classmethod
    def get_api_comment(cls) -> APIComment:
        return APIComment(
            name_en=cls.resource_name(),
            name_cn='魂印',
            examples=[
                {
                    'id': 2001,
                    'desc': '自身登场之后首次受到攻击伤害时，记录此伤害；自身使用攻击技能后附加上述记录50%的百分比伤害，自身每携带一个攻击技能效果提升10%；自身使用属性技能后恢复上述记录50%的体力，自身每携带一个属性技能效果提升10%（boss无效）',
                    'desc_formatting_adjustment': '\u003cindent=0\u003e\u003csprite=0\u003e\u003cindent=16\u003e登场效果：\r\n\u003cindent=16\u003e\u003csprite=3\u003e\u003cindent=32\u003e自身登场之后首次受到攻击伤害时，记录此伤害\r\n\r\n\u003cindent=0\u003e\u003csprite=0\u003e\u003cindent=16\u003e技能额外效果：\r\n\u003cindent=16\u003e\u003csprite=3\u003e\u003cindent=32\u003e自身使用攻击技能后\u003ccolor=#64F9FA\u003e附加\u003c/color\u003e上述记录50%的\u003cb\u003e百分比伤害\u003c/b\u003e，自身每携带一个攻击技能效果提升10%\r\n\u003cindent=16\u003e\u003csprite=3\u003e\u003cindent=32\u003e自身使用属性技能后\u003ccolor=#64F9FA\u003e恢复\u003c/color\u003e上述记录50%的\u003cb\u003e体力\u003c/b\u003e，自身每携带一个属性技能效果提升10%',
                    'pve_effective': False,
                    'intensified': False,
                    'is_adv': False,
                    'pet': [{'id': 4810, 'url': 'https://api.seerapi.com/v1/pet/4810'}],
                    'effect': {
                        'effect_args': [1, 0],
                        'effect': {
                            'id': 2426,
                            'url': 'https://api.seerapi.com/v1/eid_effect/2426',
                        },
                    },
                    'tag': [
                        {'id': 6, 'url': 'https://api.seerapi.com/v1/soulmark_tag/6'},
                        {'id': 15, 'url': 'https://api.seerapi.com/v1/soulmark_tag/15'},
                    ],
                    'intensified_to': None,
                    'from': None,
                    'hash': '17abd989',
                }
            ],
            tags=['精灵', '魂印'],
            description='魂印资源，该资源还整理了魂印的强化关系。',
        )


class SoulmarkORM(SoulmarkBase, table=True):
    pet: list['PetORM'] = Relationship(
        back_populates='soulmark', link_model=PetSoulmarkLink
    )
    tag: list['SoulmarkTagORM'] = Relationship(
        back_populates='soulmark', link_model=SoulmarkTagLink
    )
    effect_in_use_id: int | None = Field(
        default=None, foreign_key='eid_effect_in_use.id'
    )
    effect_in_use: EidEffectInUseORM | None = Relationship(
        back_populates='soulmark',
    )

    from_: Optional['SoulmarkORM'] = Relationship(
        back_populates='intensified_to',
        sa_relationship_kwargs={
            # "foreign_keys": "[SoulmarkORM.from_id]",
            # "primaryjoin": "SoulmarkORM.from_id == SoulmarkORM.id",
            # "remote_side": "SoulmarkORM.id",
            'uselist': False,
        },
    )
    intensified_to_id: int | None = Field(default=None, foreign_key='soulmark.id')
    intensified_to: Optional['SoulmarkORM'] = Relationship(
        back_populates='from_',
        sa_relationship_kwargs={
            'foreign_keys': '[SoulmarkORM.intensified_to_id]',
            'primaryjoin': 'SoulmarkORM.intensified_to_id == SoulmarkORM.id',
            'remote_side': 'SoulmarkORM.id',
            'uselist': False,
        },
    )


class SoulmarkTagBase(BaseCategoryModel):
    name: str = Field(description='魂印标签名称')

    @classmethod
    def resource_name(cls) -> str:
        return 'soulmark_tag'


class SoulmarkTagCategory(SoulmarkTagBase, ConvertToORM['SoulmarkTagORM']):
    soulmark: list[ResourceRef] = Field(default_factory=list, description='魂印列表')

    @classmethod
    def get_orm_model(cls) -> type['SoulmarkTagORM']:
        return SoulmarkTagORM

    def to_orm(self) -> 'SoulmarkTagORM':
        return SoulmarkTagORM(
            id=self.id,
            name=self.name,
        )

    @classmethod
    def get_api_comment(cls) -> APIComment:
        return APIComment(
            name_en=cls.resource_name(),
            name_cn='魂印标签',
            examples=[
                {
                    'id': 6,
                    'name': '恢复',
                    'soulmark': [
                        {'id': 6, 'url': 'https://api.seerapi.com/v1/soulmark/6'},
                        {'id': 7, 'url': 'https://api.seerapi.com/v1/soulmark/7'},
                    ],
                    'hash': '67yh89pk',
                },
            ],
            tags=['精灵', '魂印', '分类'],
            description='魂印标签，例如强攻，断回合等。',
        )


class SoulmarkTagORM(SoulmarkTagBase, table=True):
    soulmark: list['SoulmarkORM'] = Relationship(
        back_populates='tag', link_model=SoulmarkTagLink
    )
