from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship

from seerapi_models.build_model import BaseResModel, ConvertToORM

if TYPE_CHECKING:
    from .enegry_bead import EnergyBeadORM
    from .skill_activation_item import SkillActivationItemORM
    from .skill_stone import SkillStoneORM


class ItemBase(BaseResModel):
    name: str = Field(description='物品名称')
    desc: str = Field(description='物品描述')
    max: int = Field(description='物品最大数量')

    @classmethod
    def resource_name(cls) -> str:
        return 'item'


class Item(ItemBase, ConvertToORM['ItemORM']):
    @classmethod
    def get_orm_model(cls) -> type['ItemORM']:
        return ItemORM

    def to_orm(self) -> 'ItemORM':
        return ItemORM(
            id=self.id,
            name=self.name,
            desc=self.desc,
            max=self.max,
        )


class ItemORM(ItemBase, table=True):
    skill_stone: Optional['SkillStoneORM'] = Relationship(
        back_populates='item',
    )
    energy_bead: Optional['EnergyBeadORM'] = Relationship(
        back_populates='item',
    )
    skill_activation_item: Optional['SkillActivationItemORM'] = Relationship(
        back_populates='item',
    )
