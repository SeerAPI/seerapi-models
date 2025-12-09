from sqlmodel import Field, Relationship

from seerapi_models.build_model import BaseResModel, ConvertToORM
from seerapi_models.build_model.comment import APIComment
from seerapi_models.common import ResourceRef
from seerapi_models.pet import Pet, SkillInPetORM
from seerapi_models.skill import Skill

from ._common import Item, ItemORM


class SkillActivationItemBase(BaseResModel):
    id: int = Field(
        primary_key=True, foreign_key='item.id', description='技能激活道具ID'
    )
    name: str = Field(description='技能激活道具名称')
    item_number: int = Field(description='激活技能需要的该道具数量')

    @classmethod
    def resource_name(cls) -> str:
        return 'skill_activation_item'


class SkillActivationItem(
    SkillActivationItemBase, ConvertToORM['SkillActivationItemORM']
):
    item: ResourceRef['Item'] = Field(description='道具资源引用')
    skill: ResourceRef['Skill'] = Field(description='使用该道具激活的技能')
    pet: ResourceRef['Pet'] = Field(description='使用该道具的精灵')

    @classmethod
    def get_orm_model(cls) -> type['SkillActivationItemORM']:
        return SkillActivationItemORM

    @classmethod
    def get_api_comment(cls) -> APIComment:
        return APIComment(
            name_en=cls.resource_name(),
            name_cn='精灵技能激活道具',
            examples=[
                {
                    'id': 1725369,
                    'name': '龙吟咖啡',
                    'item_number': 3,
                    'item': {
                        'id': 1725369,
                        'url': 'https://api.seerapi.com/v1/item/1725369',
                    },
                    'skill': {
                        'id': 28355,
                        'url': 'https://api.seerapi.com/v1/skill/28355',
                    },
                    'pet': {'id': 4401, 'url': 'https://api.seerapi.com/v1/pet/4401'},
                    'hash': 'b7c9c4ef',
                }
            ],
            tags=['技能激活道具', '道具', '技能', '精灵'],
            description='精灵技能激活道具，返回的模型中包含技能和精灵相关的引用，以及激活该技能所需的道具数量。',
        )

    def to_orm(self) -> 'SkillActivationItemORM':
        return SkillActivationItemORM(
            id=self.id,
            name=self.name,
            item_number=self.item_number,
        )


class SkillActivationItemORM(SkillActivationItemBase, table=True):
    item: 'ItemORM' = Relationship(back_populates='skill_activation_item')
    skill_in_pet: 'SkillInPetORM' = Relationship(back_populates='skill_activation_item')
