from typing import Optional

from sqlmodel import Field, Relationship

from seerapi_models.build_model import BaseResModel, ConvertToORM
from seerapi_models.build_model.comment import APIComment
from seerapi_models.common import (
    EidEffectInUse,
    EidEffectInUseORM,
    ResourceRef,
    SixAttributes,
    SixAttributesORMBase,
)

from ._common import Item, ItemORM


class EnergyBeadBase(BaseResModel):
    id: int = Field(primary_key=True, foreign_key='item.id', description='能量珠ID')
    name: str = Field(description='能量珠名称')
    desc: str = Field(description='能量珠描述')
    idx: int = Field(description='能量珠效果ID')
    use_times: int = Field(description='使用次数')

    @classmethod
    def resource_name(cls) -> str:
        return 'energy_bead'


class EnergyBead(EnergyBeadBase, ConvertToORM['EnergyBeadORM']):
    item: ResourceRef['Item'] = Field(description='能量珠物品资源引用')
    effect: EidEffectInUse = Field(description='能量珠效果')
    ability_buff: SixAttributes | None = Field(
        default=None, description='能力加成数值，仅当能量珠效果为属性加成时有效'
    )

    @classmethod
    def get_api_comment(cls) -> APIComment:
        return APIComment(
            name_en=cls.resource_name(),
            name_cn='能量珠',
            examples=[
                {
                    'id': 300030,
                    'name': '防御能量珠',
                    'desc': '增加精灵防御能力20点（赛尔间对战无效）',
                    'idx': 1001,
                    'use_times': 20,
                    'item': {
                        'id': 300030,
                        'url': 'https://api.seerapi.com/v1/item/300030',
                    },
                    'effect': {
                        'effect_args': [1, 20],
                        'effect': {
                            'id': 26,
                            'url': 'https://api.seerapi.com/v1/eid_effect/26',
                        },
                    },
                    'ability_buff': {
                        'atk': 0,
                        'def': 20,
                        'sp_atk': 0,
                        'sp_def': 0,
                        'spd': 0,
                        'hp': 0,
                        'percent': False,
                        'total': 20,
                    },
                    'hash': 'b937afd',
                },
            ],
            tags=['道具', '能量珠'],
            description='能量珠资源，注意：这类资源中不包含非加成类战斗道具（例如学习力双倍器）。',
        )

    @classmethod
    def get_orm_model(cls) -> type['EnergyBeadORM']:
        return EnergyBeadORM

    def to_orm(self) -> 'EnergyBeadORM':
        return EnergyBeadORM(
            id=self.id,
            name=self.name,
            desc=self.desc,
            idx=self.idx,
            effect_in_use=self.effect.to_orm(),
            use_times=self.use_times,
            ability_buff=EnergyBeadBuffAttrORM(
                **self.ability_buff.model_dump(),
            )
            if self.ability_buff
            else None,
        )


class EnergyBeadORM(EnergyBeadBase, table=True):
    effect_in_use: 'EidEffectInUseORM' = Relationship(
        back_populates='energy_bead',
        sa_relationship_kwargs={
            'primaryjoin': 'EnergyBeadORM.effect_in_use_id == EidEffectInUseORM.id',
        },
    )
    effect_in_use_id: int | None = Field(
        default=None, foreign_key='eid_effect_in_use.id'
    )
    ability_buff: Optional['EnergyBeadBuffAttrORM'] = Relationship(
        back_populates='energy_bead',
        sa_relationship_kwargs={
            'uselist': False,
            'primaryjoin': 'EnergyBeadORM.id == EnergyBeadBuffAttrORM.id',
        },
    )
    item: 'ItemORM' = Relationship(back_populates='energy_bead')


class EnergyBeadBuffAttrORM(SixAttributesORMBase, table=True):
    id: int | None = Field(
        default=None,
        primary_key=True,
        foreign_key='energy_bead.id',
        description='能量珠能力加成ID',
    )
    energy_bead: 'EnergyBeadORM' = Relationship(
        back_populates='ability_buff',
        sa_relationship_kwargs={
            'uselist': False,
            'primaryjoin': 'EnergyBeadORM.id == EnergyBeadBuffAttrORM.id',
        },
    )

    @classmethod
    def resource_name(cls) -> str:
        return 'energy_bead_buff_attr'
