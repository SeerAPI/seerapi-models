from typing import TYPE_CHECKING

from pydantic import computed_field
from sqlmodel import Boolean, Column, Computed, Field, Relationship

from seerapi_models.build_model import BaseResModel, ConvertToORM
from seerapi_models.build_model.comment import APIComment
from seerapi_models.common import ResourceRef

if TYPE_CHECKING:
    from .items.skill_stone import SkillStoneCategoryORM
    from .pet import PetORM
    from .skill import SkillORM


class ElementType(BaseResModel, ConvertToORM['ElementTypeORM']):
    name: str = Field(description='属性中文名')
    name_en: str = Field(description='属性英文名')

    @classmethod
    def resource_name(cls) -> str:
        return 'element_type'

    @classmethod
    def get_orm_model(cls) -> type['ElementTypeORM']:
        return ElementTypeORM

    def to_orm(self) -> 'ElementTypeORM':
        return ElementTypeORM(
            id=self.id,
            name=self.name,
            name_en=self.name_en,
        )

    @classmethod
    def get_api_comment(cls) -> APIComment:
        return APIComment(
            name_en=cls.resource_name(),
            name_cn='属性',
            examples=[
                {'id': 16, 'name': '圣灵', 'name_en': 'saint', 'hash': '9062249d'}
            ],
            tags=['属性'],
            description='属性资源，该资源仅作为基础资源，保存属性克制关系（TODO）等数据。'
            '不包含双属性数据，实际使用时请使用 TypeCombination 资源。',
        )


class ElementTypeORM(ElementType, table=True):
    primary_combination: list['TypeCombinationORM'] = Relationship(
        back_populates='primary',
        sa_relationship_kwargs={
            'primaryjoin': 'ElementTypeORM.id == TypeCombinationORM.primary_id',
            'viewonly': True,
        },
    )
    secondary_combination: list['TypeCombinationORM'] = Relationship(
        back_populates='secondary',
        sa_relationship_kwargs={
            'primaryjoin': 'ElementTypeORM.id == TypeCombinationORM.secondary_id',
            'viewonly': True,
        },
    )


class TypeCombinationBase(BaseResModel):
    name: str = Field(description='组合类型中文名')
    name_en: str = Field(description='组合类型英文名')

    @classmethod
    def resource_name(cls) -> str:
        return 'element_type_combination'


class TypeCombination(TypeCombinationBase, ConvertToORM['TypeCombinationORM']):
    primary: ResourceRef[ElementType] = Field(description='第一属性')
    secondary: ResourceRef[ElementType] | None = Field(
        default=None, description='第二属性，仅在该属性为双属性时有效'
    )

    @computed_field(description='是否是双属性')
    @property
    def is_double(self) -> bool:
        return self.secondary is not None

    @classmethod
    def get_orm_model(cls) -> type['TypeCombinationORM']:
        return TypeCombinationORM

    def to_orm(self) -> 'TypeCombinationORM':
        return TypeCombinationORM(
            id=self.id,
            name=self.name,
            name_en=self.name_en,
            primary_id=self.primary.id,
            secondary_id=self.secondary.id if self.secondary else None,
        )

    @classmethod
    def get_api_comment(cls) -> APIComment:
        return APIComment(
            name_en=cls.resource_name(),
            name_cn='属性组合',
            examples=[
                {
                    'id': 100,
                    'name': '圣灵 地面',
                    'name_en': 'saint_ground',
                    'primary': {
                        'id': 16,
                        'url': 'https://api.seerapi.com/v1/element_type/16',
                    },
                    'secondary': {
                        'id': 7,
                        'url': 'https://api.seerapi.com/v1/element_type/7',
                    },
                    'is_double': True,
                    'hash': '637da042',
                }
            ],
            tags=['属性', '组合'],
            description='属性组合资源，所有包含所有的单属性和双属性数据。'
            '注意“第一属性”和“第二属性”仅为了区分两个属性，游戏内并无主次之分。',
        )


class TypeCombinationORM(TypeCombinationBase, table=True):
    primary_id: int = Field(foreign_key='element_type.id')
    primary: 'ElementTypeORM' = Relationship(
        back_populates='primary_combination',
        sa_relationship_kwargs={
            'primaryjoin': 'TypeCombinationORM.primary_id == ElementTypeORM.id',
        },
    )
    secondary_id: int | None = Field(default=None, foreign_key='element_type.id')
    secondary: ElementTypeORM | None = Relationship(
        back_populates='secondary_combination',
        sa_relationship_kwargs={
            'primaryjoin': 'TypeCombinationORM.secondary_id == ElementTypeORM.id',
        },
    )
    if not TYPE_CHECKING:
        is_double: bool = Field(
            sa_column=Column(
                Boolean,
                Computed('secondary_id IS NOT NULL', persisted=True),
                nullable=False,
            )
        )

    skill: list['SkillORM'] = Relationship(
        back_populates='type',
    )
    pet: list['PetORM'] = Relationship(
        back_populates='type',
    )
    skill_stone_category: list['SkillStoneCategoryORM'] = Relationship(
        back_populates='type',
    )
