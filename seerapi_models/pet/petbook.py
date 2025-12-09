from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from seerapi_models.build_model import (
    BaseCategoryModel,
    BaseResModel,
    ConvertToORM,
)
from seerapi_models.build_model.comment import APIComment
from seerapi_models.common import ResourceRef

if TYPE_CHECKING:
    from .pet import Pet, PetORM


class PetEncyclopediaEntryBase(BaseResModel):
    id: int = Field(primary_key=True, description='精灵图鉴ID', foreign_key='pet.id')
    name: str = Field(description='精灵名称')
    has_sound: bool = Field(description='精灵是否存在叫声')
    height: float | None = Field(
        default=None,
        description="精灵身高，当这个值在图鉴中为'未知'时，这个值为null",
    )
    weight: float | None = Field(
        default=None,
        description="精灵重量，当这个值在图鉴中为'未知'时，这个值为null",
    )
    foundin: str | None = Field(default=None, description='精灵发现地点')
    food: str | None = Field(default=None, description='精灵喜爱的食物')
    introduction: str = Field(description='精灵介绍')

    @classmethod
    def resource_name(cls) -> str:
        return 'pet_encyclopedia_entry'


class PetEncyclopediaEntry(
    PetEncyclopediaEntryBase, ConvertToORM['PetEncyclopediaEntryORM']
):
    pet: ResourceRef['Pet'] = Field(description='精灵')

    @classmethod
    def get_orm_model(cls) -> type['PetEncyclopediaEntryORM']:
        return PetEncyclopediaEntryORM

    def to_orm(self) -> 'PetEncyclopediaEntryORM':
        return PetEncyclopediaEntryORM(
            id=self.id,
            name=self.name,
            has_sound=self.has_sound,
            height=self.height,
            weight=self.weight,
            foundin=self.foundin,
            food=self.food,
            introduction=self.introduction,
        )

    @classmethod
    def get_api_comment(cls) -> APIComment:
        return APIComment(
            name_en=cls.resource_name(),
            name_cn='精灵图鉴条目',
            examples=[
                {
                    'id': 70,
                    'name': '雷伊',
                    'has_sound': True,
                    'height': 129,
                    'weight': 35.8,
                    'foundin': '赫尔卡星荒地',
                    'food': '闪电能量',
                    'introduction': '雷伊是赫尔卡星的神秘精灵，只有当雷雨天才会出现，全身被电流所包围，尽显王者风范。',
                    'pet': {'id': 70, 'url': 'https://api.seerapi.com/v1/pet/70'},
                    'hash': '6b2af886',
                }
            ],
            tags=['精灵', '图鉴'],
            description='精灵图鉴条目，该资源部分字段来源于旧版图鉴。',
        )


class PetEncyclopediaEntryORM(PetEncyclopediaEntryBase, table=True):
    pet: 'PetORM' = Relationship(back_populates='encyclopedia')


class PetArchiveStoryEntryBase(BaseResModel):
    id: int = Field(primary_key=True, description='故事条目ID')
    content: str = Field(description='故事条目内容')

    @classmethod
    def resource_name(cls) -> str:
        return 'pet_archive_story_entry'


class PetArchiveStoryEntry(
    PetArchiveStoryEntryBase, ConvertToORM['PetArchiveStoryEntryORM']
):
    pet: ResourceRef['Pet'] = Field(description='精灵')
    book: ResourceRef['PetArchiveStoryBook'] = Field(description='故事系列')

    @classmethod
    def get_orm_model(cls) -> type['PetArchiveStoryEntryORM']:
        return PetArchiveStoryEntryORM

    def to_orm(self) -> 'PetArchiveStoryEntryORM':
        return PetArchiveStoryEntryORM(
            id=self.id, content=self.content, pet_id=self.pet.id, book_id=self.book.id
        )

    @classmethod
    def get_api_comment(cls) -> APIComment:
        return APIComment(
            name_en=cls.resource_name(),
            name_cn='精灵故事条目',
            examples=[
                {
                    'id': 650,
                    'content': '我失去了我的厄孽提亚……\\n老大说得对，和自己的精灵产生感情，是愚蠢的，是荒谬的。赫米娅，你应该振作起来！\\n我的基地被毁了，我辜负了老大……这都怪小赛尔，这些只会在宇宙中四处搞破坏的机器人，他们作恶多端，还害死了我的厄孽提亚！这些赛尔机器人为什么要处处和我们作对？\\n厄孽提亚，我还记得你从孢子囊中钻出来的那一刻，你那么有活力，挥舞着两条有力的藤鞭游来游去，我猜你一定开心极了，对什么都充满好奇。不像我刚来到这个世界时，只有茫然与疑惑。\\n我从未向你讲起你从何而来，我怕你伤心。那时我们的队伍刚来到海洋星，为了寻找传说中的深海古龙，我们在海洋星找了一次又一次，卡兰星系留下来的资料里记录了古龙的坐标，可是那些愚蠢的资料分析员根本不知道龙族使用的坐标记录方式和我们完全不一样。那一次，我们的飞船降落在了一个特别冷的地方，我猜这一定是海洋星上温度最低的位置，海面还结着厚厚的冰盖，但这是一件好事，因为我们的飞船终于有了停泊的地方，这对于海洋星这种完全被水淹没的星球来说是特别特殊的地方。刚进入海里，我们就看到了特别令我们难忘的恐怖景象：海面上的浮冰竟突然凝结出一根不断向下蔓延的冰梯，所有触碰到冰梯的东西全部都被冻结在了冰梯之中。而你的母亲，就是冰梯的第一个受害者。那片寒冷水域中有不少你母亲的同类，它们见到你母亲的悲惨遭遇之后全部都以最快的速度远离了冰梯。冰梯就这样一路蔓延，触碰到了浅海底，海底那些智能程度极低的精灵们也都被冻结在了寒冰之中。当冰梯不再蔓延，我靠近了你的母亲，发现它身上正结着一个鼓胀的孢子囊。我把孢子囊切下，带回去细心照料——终于，你诞生了。你是这个孢子囊中活下来的唯一一个，我叫你“厄孽提亚”。\\n你从出生开始就在我的身边，你的每一次进步我都无法忘记。你的双腕越来越有力，从最开始只能缠住敌人，到之后可以瞬间鞭打对手十余次，你的力量增长迅猛。过去，那些胆敢阻挡我们的家伙都会尝到你率先发起的旋转缠缚，而到最后之时，你已经可以利用这种藤蔓的旋转，在海水之中制造出极有破坏力的水龙卷……\\n你是深沉绽放的深海之花，我从你身上感受到的生命力完全不亚于旁边的火山里面蕴含的力量。当我发现你的身上也生出了孢子囊时我兴奋极了。但是或许是因为我们基地的所在位置不够寒冷，你的孩子们降生时完全没有像你那时一样的活力，我只能把他们重新养殖在冷水缸中，期盼它们也能够像你一样茁壮成长，它们在未来都会和你一样成为组织的好帮手。但是，我此前所畅想的一切都被赛尔破坏了！\\n愿宇宙中没有赛尔，我的厄孽提亚…… \\n厄孽提亚，老大说得对。我必须要忘记你，我的厄孽提亚。这是我最后一次回忆你，但愿你安息，我一定会让那些可恶的赛尔为他们所做的一切付出代价！\\n——节选自《赫米娅的日志》',
                    'pet': {'id': 4793, 'url': 'https://api.seerapi.com/v1/pet/4793'},
                    'book': {
                        'id': 1,
                        'url': 'https://api.seerapi.com/v1/pet_archive_story_book/1',
                    },
                    'hash': '3249a54e',
                }
            ],
            tags=['精灵', '故事', '图鉴'],
            description='精灵故事条目（永夜纪年/莱达物语）。',
        )


class PetArchiveStoryEntryORM(PetArchiveStoryEntryBase, table=True):
    pet_id: int = Field(description='精灵ID', foreign_key='pet.id')
    pet: 'PetORM' = Relationship(back_populates='archive_story')
    book_id: int = Field(
        foreign_key='pet_archive_story_book.id',
    )
    book: 'PetArchiveStoryBookORM' = Relationship(back_populates='entries')


class PetArchiveStoryBookBase(BaseCategoryModel):
    name: str = Field(description='故事名称')

    @classmethod
    def resource_name(cls) -> str:
        return 'pet_archive_story_book'


class PetArchiveStoryBook(
    PetArchiveStoryBookBase, ConvertToORM['PetArchiveStoryBookORM']
):
    entries: list[ResourceRef[PetArchiveStoryEntryBase]] = Field(
        default_factory=list, description='故事条目'
    )

    @classmethod
    def get_orm_model(cls) -> type['PetArchiveStoryBookORM']:
        return PetArchiveStoryBookORM

    def to_orm(self) -> 'PetArchiveStoryBookORM':
        return PetArchiveStoryBookORM(
            id=self.id,
            name=self.name,
        )

    @classmethod
    def get_api_comment(cls) -> APIComment:
        return APIComment(
            name_en=cls.resource_name(),
            name_cn='精灵故事系列',
            examples=[
                {
                    'id': 2,
                    'name': '莱达物语',
                    'entries': [
                        {
                            'id': 306,
                            'url': 'https://api.seerapi.com/v1/pet_archive_story_entry/306',
                        },
                        {
                            'id': 315,
                            'url': 'https://api.seerapi.com/v1/pet_archive_story_entry/315',
                        },
                        {
                            'id': 316,
                            'url': 'https://api.seerapi.com/v1/pet_archive_story_entry/316',
                        },
                    ],
                    'hash': '726fd01',
                }
            ],
            tags=['精灵', '故事', '图鉴', '分类'],
            description='精灵故事系列（永夜纪年/莱达物语）。',
        )


class PetArchiveStoryBookORM(PetArchiveStoryBookBase, table=True):
    entries: list[PetArchiveStoryEntryORM] = Relationship(back_populates='book')
