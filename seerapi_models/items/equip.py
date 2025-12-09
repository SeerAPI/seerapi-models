from typing import TYPE_CHECKING, Optional
from typing_extensions import Self

from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel

from seerapi_models.build_model import (
    BaseCategoryModel,
    BaseResModel,
    BaseResModelWithOptionalId,
    ConvertToORM,
)
from seerapi_models.build_model.comment import APIComment
from seerapi_models.common import (
    EidEffectInUse,
    EidEffectInUseORM,
    ResourceRef,
    SixAttributes,
    SixAttributesORM,
)
from seerapi_models.items._common import Item, ItemORM

if TYPE_CHECKING:
    from seerapi_models.pet import Pet, PetORM


class SuitBonusAttrORM(SixAttributesORM, table=True):
    suit_bonus: 'SuitBonusORM' = Relationship(
        back_populates='attribute',
    )

    @classmethod
    def resource_name(cls) -> str:
        return 'suit_bonus_attr'


class EquipBonusAttrORM(SixAttributesORM, table=True):
    equip_bonus: 'EquipBonusORM' = Relationship(
        back_populates='attribute',
    )

    @classmethod
    def resource_name(cls) -> str:
        return 'equip_bonus_attr'


class PkAttribute(BaseModel):
    """装备PK加成（战队保卫战等远古活动使用）"""

    pk_hp: int = Field(description='装备提供的血量加成')
    pk_atk: int = Field(description='装备提供的攻击力加成')
    pk_fire_range: int = Field(description='装备提供的射击范围加成')


class OtherAttribute(BaseModel):
    hit_rate: int = Field(default=0, description='命中加成')
    dodge_rate: int = Field(default=0, description='闪避加成')
    crit_rate: int = Field(default=0, description='暴击加成')

    @classmethod
    def from_list(cls, other_attr_args: list[int]) -> Self:
        return cls(
            hit_rate=other_attr_args[0],
            dodge_rate=other_attr_args[1],
            crit_rate=other_attr_args[2],
        )


class PetSuitLink(SQLModel, table=True):
    pet_id: int | None = Field(default=None, foreign_key='pet.id', primary_key=True)
    suit_id: int | None = Field(
        default=None, foreign_key='suit_bonus.id', primary_key=True
    )


class EquipEffect(SQLModel):
    newse_id: int | None = Field(
        default=None,
        description='部件特性ID，一部分套装使用该字段来表示效果',
    )
    eid_effect: EidEffectInUse | None = Field(
        default=None,
        description='部件效果，一部分套装使用该字段来表示效果',
    )


class EquipBonusBase(BaseResModelWithOptionalId):
    desc: str = Field(description='部件描述')

    @classmethod
    def resource_name(cls) -> str:
        return 'equip_bonus'


class EquipBonus(EquipBonusBase, EquipEffect, ConvertToORM['EquipBonusORM']):
    attribute: SixAttributes | None = Field(
        default=None, description='属性加成，仅在部件有属性加成时有效'
    )
    other_attribute: OtherAttribute | None = Field(
        default=None, description='其他属性加成，仅在部件有命中/闪避/暴击加成时有效'
    )

    @classmethod
    def get_orm_model(cls) -> type['EquipBonusORM']:
        return EquipBonusORM

    def to_orm(self) -> 'EquipBonusORM':
        other_attr_kwargs = (
            self.other_attribute.model_dump() if self.other_attribute else {}
        )
        effect_in_use_orm = None
        if self.eid_effect:
            effect_in_use_orm = self.eid_effect.to_orm()

        return EquipBonusORM(
            id=self.id,
            desc=self.desc,
            effect_in_use=effect_in_use_orm,
            newse_id=self.newse_id,
            attribute=EquipBonusAttrORM(**self.attribute.model_dump())
            if self.attribute
            else None,
            **other_attr_kwargs,
        )


class EquipBonusORM(EquipBonusBase, table=True):
    equip: 'EquipORM' = Relationship(
        back_populates='bonus',
    )

    effect_in_use_id: int | None = Field(foreign_key='eid_effect_in_use.id')
    effect_in_use: Optional['EidEffectInUseORM'] = Relationship(
        back_populates='equip_bonus',
    )
    newse_id: int | None = Field(default=None)
    attribute_id: int | None = Field(default=None, foreign_key='equip_bonus_attr.id')
    attribute: Optional['EquipBonusAttrORM'] = Relationship(
        back_populates='equip_bonus',
    )

    hit_rate: int | None = Field(default=None)
    dodge_rate: int | None = Field(default=None)
    crit_rate: int | None = Field(default=None)


class SuitBonusBase(BaseResModel):
    id: int = Field(
        description='套装效果ID',
        primary_key=True,
        foreign_key='suit.id',
    )
    desc: str = Field(description='套装描述')

    @classmethod
    def resource_name(cls) -> str:
        return 'suit_bonus'


class SuitBonus(SuitBonusBase, EquipEffect, ConvertToORM['SuitBonusORM']):
    effective_pets: list[ResourceRef['Pet']] | None = Field(
        default=None,
        description='表示套装效果仅在这些精灵上生效，null表示对所有精灵都生效',
    )
    attribute: SixAttributes | None = Field(
        default=None, description='属性加成，仅在套装效果为属性加成时有效'
    )

    @classmethod
    def get_orm_model(cls) -> type['SuitBonusORM']:
        return SuitBonusORM

    def to_orm(self) -> 'SuitBonusORM':
        effect_in_use_orm = None
        if self.eid_effect:
            effect_in_use_orm = self.eid_effect.to_orm()

        return SuitBonusORM(
            id=self.id,
            desc=self.desc,
            newse_id=self.newse_id,
            effect_in_use=effect_in_use_orm,
            attribute=SuitBonusAttrORM(**self.attribute.model_dump())
            if self.attribute
            else None,
        )


class SuitBonusORM(SuitBonusBase, table=True):
    suit: 'SuitORM' = Relationship(
        back_populates='bonus',
    )

    newse_id: int | None = Field(default=None)
    effect_in_use_id: int | None = Field(
        default=None, foreign_key='eid_effect_in_use.id'
    )
    effect_in_use: Optional['EidEffectInUseORM'] = Relationship(
        back_populates='suit_bonus',
    )
    attribute_id: int | None = Field(default=None, foreign_key='suit_bonus_attr.id')
    attribute: Optional['SuitBonusAttrORM'] = Relationship(
        back_populates='suit_bonus',
    )

    effective_pets: list['PetORM'] = Relationship(
        back_populates='exclusive_suit_bonus',
        link_model=PetSuitLink,
    )


class SuitBase(BaseResModel):
    name: str = Field(description='名称')
    transform: bool = Field(description='是否可变形')
    tran_speed: float | None = Field(
        default=None, description='变形速度，仅当该套装可变形时有效'
    )
    suit_desc: str = Field(description='套装描述')

    @classmethod
    def resource_name(cls) -> str:
        return 'suit'

    @classmethod
    def get_api_comment(cls) -> APIComment:
        return APIComment(
            name_en=cls.resource_name(),
            name_cn='套装',
            examples=[
                {
                    'id': 393,
                    'name': '笑傲巅峰套装',
                    'transform': False,
                    'tran_speed': 0,
                    'suit_desc': '赛尔们在冒险中获得的套装，能够改变外观或者增强力量',
                    'equips': [
                        {
                            'id': 1300794,
                            'url': 'https://api.seerapi.com/v1/equip/1300794',
                        },
                        {
                            'id': 1300795,
                            'url': 'https://api.seerapi.com/v1/equip/1300795',
                        },
                        {
                            'id': 1300796,
                            'url': 'https://api.seerapi.com/v1/equip/1300796',
                        },
                        {
                            'id': 1300797,
                            'url': 'https://api.seerapi.com/v1/equip/1300797',
                        },
                    ],
                    'bonus': {
                        'newse_id': 7745,
                        'eid_effect': {
                            'effect_args': [10, 15, 1, 1, 4, 13, 1],
                            'effect': {
                                'id': 1271,
                                'url': 'https://api.seerapi.com/v1/eid_effect/1271',
                            },
                        },
                        'id': 393,
                        'desc': '背包内精灵全属性+10%；己方精灵造成的致命一击伤害提升15%；攻击技能有1/16的几率打出致命一击，每次使用增加1/16，最高4/16，未打出致命一击则造成伤害前附加自身最大体力13%的百分比伤害（仅限赛尔与赛尔间对战）',
                        'effective_pets': [],
                        'attribute': {
                            'atk': 10,
                            'def': 10,
                            'sp_atk': 10,
                            'sp_def': 10,
                            'spd': 10,
                            'hp': 10,
                            'percent': False,
                            'total': 60,
                        },
                    },
                    'hash': 'c0fe9e5',
                }
            ],
            tags=['装备', '套装'],
            description='赛尔套装。',
        )


class Suit(SuitBase, ConvertToORM['SuitORM']):
    equips: list[ResourceRef['Equip']] = Field(
        default_factory=list, description='部件列表'
    )
    bonus: SuitBonus | None = Field(
        default=None, description='套装效果，仅当该套装为能力加成套装时有效'
    )

    @classmethod
    def get_orm_model(cls) -> type['SuitORM']:
        return SuitORM

    def to_orm(self) -> 'SuitORM':
        return SuitORM(
            id=self.id,
            name=self.name,
            transform=self.transform,
            tran_speed=self.tran_speed,
            suit_desc=self.suit_desc,
            bonus=self.bonus.to_orm() if self.bonus else None,
        )


class SuitORM(SuitBase, table=True):
    equips: list['EquipORM'] = Relationship(
        back_populates='suit',
    )
    bonus: Optional['SuitBonusORM'] = Relationship(
        back_populates='suit',
    )


class EquipBase(BaseResModel):
    id: int = Field(primary_key=True, foreign_key='item.id', description='部件ID')
    name: str = Field(description='部件名称')
    speed: float | None = Field(
        default=None, description='部件速度移动加成，一般只有脚部部件提供'
    )

    @classmethod
    def resource_name(cls) -> str:
        return 'equip'

    @classmethod
    def get_api_comment(cls) -> APIComment:
        return APIComment(
            name_en=cls.resource_name(),
            name_cn='部件',
            examples=[
                {
                    'id': 1300694,
                    'name': '典狱长头盔',
                    'speed': 0,
                    'item': {
                        'id': 1300694,
                        'url': 'https://api.seerapi.com/v1/item/1300694',
                    },
                    'bonus': {
                        'newse_id': None,
                        'eid_effect': None,
                        'desc': '背包内精灵命中+4%',
                        'attribute': {
                            'atk': 0,
                            'def': 0,
                            'sp_atk': 0,
                            'sp_def': 0,
                            'spd': 0,
                            'hp': 0,
                            'percent': True,
                            'total': 0,
                        },
                        'other_attribute': {
                            'hit_rate': 4,
                            'dodge_rate': 0,
                            'crit_rate': 0,
                        },
                    },
                    'occasion': {
                        'id': 0,
                        'url': 'https://api.seerapi.com/v1/equip_effective_occasion/0',
                    },
                    'suit': {'id': 370, 'url': 'https://api.seerapi.com/v1/suit/370'},
                    'part_type': {
                        'id': 0,
                        'url': 'https://api.seerapi.com/v1/equip_type/0',
                    },
                    'pk_attribute': {'pk_hp': 60, 'pk_atk': 25, 'pk_fire_range': 0},
                    'hash': '557fce0f',
                }
            ],
            tags=['装备', '部件'],
            description='赛尔装备部件。',
        )


class Equip(EquipBase, ConvertToORM['EquipORM']):
    item: ResourceRef['Item'] = Field(description='装备部件物品资源引用')
    bonus: EquipBonus | None = Field(
        default=None, description='部件效果，仅当该部件为能力加成部件时有效'
    )
    occasion: ResourceRef['EquipEffectiveOccasion'] | None = Field(
        default=None, description='部件生效场合，仅当该部件为能力加成部件时有效'
    )
    suit: ResourceRef[Suit] | None = Field(
        default=None, description='部件所属套装，仅当该部件有套装时有效'
    )
    part_type: ResourceRef['EquipType'] = Field(description='部件类型')
    pk_attribute: PkAttribute | None = Field(
        default=None,
        description='部件PK加成，战队保卫战等老玩法使用，当三个加成项都为0时为null',
    )

    @classmethod
    def get_orm_model(cls) -> type['EquipORM']:
        return EquipORM

    def to_orm(self) -> 'EquipORM':
        pk_kwargs = self.pk_attribute.model_dump() if self.pk_attribute else {}
        return EquipORM(
            id=self.id,
            name=self.name,
            speed=self.speed,
            part_type_id=self.part_type.id,
            suit_id=self.suit.id if self.suit else None,
            occasion_id=self.occasion.id if self.occasion else None,
            bonus=self.bonus.to_orm() if self.bonus else None,
            **pk_kwargs,
        )


class EquipORM(EquipBase, table=True):
    part_type_id: int = Field(foreign_key='equip_type.id')
    part_type: 'EquipTypeORM' = Relationship(
        back_populates='equip',
    )
    suit_id: int | None = Field(default=None, foreign_key='suit.id')
    suit: 'SuitORM' = Relationship(
        back_populates='equips',
    )
    bonus_id: int | None = Field(default=None, foreign_key='equip_bonus.id')
    bonus: Optional['EquipBonusORM'] = Relationship(
        back_populates='equip',
    )
    occasion_id: int | None = Field(
        default=None, foreign_key='equip_effective_occasion.id'
    )
    occasion: 'EquipEffectiveOccasionORM' = Relationship(
        back_populates='equip',
    )

    pk_hp: int | None = Field(default=None)
    pk_atk: int | None = Field(default=None)
    pk_fire_range: int | None = Field(default=None)

    item: 'ItemORM' = Relationship(back_populates='equip')


class EquipTypeBase(BaseCategoryModel):
    name: str = Field(description='部件类型名称')

    @classmethod
    def resource_name(cls) -> str:
        return 'equip_type'

    @classmethod
    def get_api_comment(cls) -> APIComment:
        return APIComment(
            name_en=cls.resource_name(),
            name_cn='部件类型',
            examples=[
                {
                    'id': 4,
                    'name': 'foot',
                    'equip': [
                        {
                            'id': 100829,
                            'url': 'https://api.seerapi.com/v1/equip/100829',
                        },
                        {
                            'id': 100826,
                            'url': 'https://api.seerapi.com/v1/equip/100826',
                        },
                    ],
                    'hash': '557fce0f',
                }
            ],
            tags=['装备', '部件', '分类'],
            description='赛尔装备部件类型，分为头部，手部，腰部，脚部，背景，星际座驾。',
        )


class EquipType(EquipTypeBase, ConvertToORM['EquipTypeORM']):
    equip: list[ResourceRef] = Field(default_factory=list, description='部件列表')

    @classmethod
    def get_orm_model(cls) -> type['EquipTypeORM']:
        return EquipTypeORM

    def to_orm(self) -> 'EquipTypeORM':
        return EquipTypeORM(
            id=self.id,
            name=self.name,
        )


class EquipTypeORM(EquipTypeBase, table=True):
    equip: list['EquipORM'] = Relationship(
        back_populates='part_type',
    )


class EquipEffectiveOccasionBase(BaseCategoryModel):
    description: str = Field(description='部件生效场合描述')

    @classmethod
    def resource_name(cls) -> str:
        return 'equip_effective_occasion'

    @classmethod
    def get_api_comment(cls) -> APIComment:
        return APIComment(
            name_en=cls.resource_name(),
            name_cn='部件能力加成生效场合',
            examples=[
                {
                    'id': 0,
                    'description': '全部战斗有效',
                    'equip': [
                        {
                            'id': 100526,
                            'url': 'https://api.seerapi.com/v1/equip/100526',
                        },
                        {
                            'id': 100525,
                            'url': 'https://api.seerapi.com/v1/equip/100525',
                        },
                    ],
                    'hash': '557fce0f',
                }
            ],
            tags=['装备', '部件', '分类'],
            description='赛尔能力加成装备生效场合，分为全部，仅赛尔间对战（PVP），仅对Boss有效（PVE）。',
        )


class EquipEffectiveOccasion(
    EquipEffectiveOccasionBase, ConvertToORM['EquipEffectiveOccasionORM']
):
    equip: list[ResourceRef] = Field(default_factory=list, description='部件列表')

    @classmethod
    def get_orm_model(cls) -> type['EquipEffectiveOccasionORM']:
        return EquipEffectiveOccasionORM

    def to_orm(self) -> 'EquipEffectiveOccasionORM':
        return EquipEffectiveOccasionORM(
            id=self.id,
            description=self.description,
        )


class EquipEffectiveOccasionORM(EquipEffectiveOccasionBase, table=True):
    equip: list['EquipORM'] = Relationship(back_populates='occasion')
