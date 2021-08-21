"""
Object Model for Spectrum Risk Database Version 1.3.2
"""
from enum import Enum

import sqlalchemy
from sqlalchemy import Boolean, Column, DateTime, Float, Identity, Index, Integer, LargeBinary, SmallInteger, Table, \
    Unicode, text, ForeignKey, ForeignKeyConstraint
from sqlalchemy.dialects.mssql import NTEXT
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()
metadata = Base.metadata


class Acase(Base):
    """Задание на расчёт последовательностей (Базовый класс)"""
    __tablename__ = 'Acase'

    Type = Column(SmallInteger, primary_key = True, nullable = False)
    __mapper_args__ = {"polymorphic_on": Type}
    Num = Column(Integer, Identity(start = 1, increment = 1), nullable = False, unique = True)
    ID = Column(Unicode(20), primary_key = True, nullable = False)
    Text = Column(Unicode(100))
    Tag = Column(SmallInteger)
    ResType = Column(SmallInteger)
    Mean = Column(Float(24))
    P05 = Column(Float(24))
    P50 = Column(Float(24))
    P95 = Column(Float(24))
    TextRes = Column(SmallInteger)
    GERes = Column(SmallInteger)
    BERes = Column(SmallInteger)
    ExchRes = Column(SmallInteger)
    Unit = Column(SmallInteger)
    EditDate = Column(DateTime)
    EditUid = Column(Integer, ForeignKey('Users.Num'))
    ReviewDate = Column(DateTime)
    ReviewUid = Column(Integer, ForeignKey('Users.Num'))
    ApprovedDate = Column(DateTime)
    ApprovedUid = Column(Integer, ForeignKey('Users.Num'))
    Flag = Column(Boolean)

    EditUser = relationship(lambda: Users, foreign_keys=[EditUid])
    ReviewUser = relationship(lambda: Users, foreign_keys=[ReviewUid])
    ApprovedUser= relationship(lambda: Users, foreign_keys=[ApprovedUid])


class FailureTreeAcase(Acase):
    """
    Задание на расчёт деревьев отказов
    """
    __mapper_args__ = {'polymorphic_identity': 31}


class ConsequenceAcase(Acase):
    """
    Задание на расчёт последствий деревьев событий
    """
    __mapper_args__ = {'polymorphic_identity': 33}


class SequenceAcase(Acase):
    """
    Задание на расчёт аварийныйх последовательностей
    """
    __mapper_args__ = {'polymorphic_identity': 32}


class GroupAcase(Acase):
    """
    Задание на расчёт группы вариантов анализа
    """
    __mapper_args__ = {'polymorphic_identity': 34}


class AcaseBC(Base):
    __tablename__ = 'AcaseBC'

    RecType = Column(SmallInteger, primary_key = True, nullable = False)
    RecNum = Column(Integer, primary_key = True, nullable = False)
    BCType = Column(SmallInteger)
    BCNum = Column(Integer)
    flag = Column(Boolean)


class AcaseET(Base):
    """Таблица связи Acase и ET"""
    __tablename__ = 'AcaseET'

    AcaseNum = Column(Integer, primary_key = True, nullable = False)
    RecType = Column(SmallInteger, primary_key = True, nullable = False)
    RecNum = Column(Integer, primary_key = True, nullable = False)
    AcaseType = Column(SmallInteger)
    flag = Column(Boolean)


class AcaseSpec(Base):
    __tablename__ = 'AcaseSpec'

    AcaseNum = Column(Integer, primary_key = True, nullable = False)
    SetupType = Column(SmallInteger, primary_key = True, nullable = False)
    AcaseType = Column(SmallInteger)
    SetupNum = Column(Integer)
    DoAna = Column(SmallInteger)
    ResExist = Column(SmallInteger)
    flag = Column(Boolean)


class AttachmentRefs(Base):
    __tablename__ = 'AttachmentRefs'

    IDNum = Column(Integer, Identity(start = 1, increment = 1), primary_key = True, nullable = False)
    RecType = Column(SmallInteger, primary_key = True, nullable = False)
    RecNum = Column(Integer, primary_key = True, nullable = False)
    Attachment = Column(Unicode(4000))


class Attributes(Base):
    """
    Объекты, при помощи которых можно анализировать влияние различных групп базовых событий на конечный результат
    квантификации. Каждому базовому событию можно присвоить несколько атрибутов
    """
    __tablename__ = 'Attrib'

    Type = Column(SmallInteger, primary_key = True, nullable = False)
    Num = Column(Integer, Identity(start = 1, increment = 1), nullable = False, unique = True)
    ID = Column(Unicode(20), primary_key = True, nullable = False)
    Text = Column(Unicode(100))
    Tag = Column(SmallInteger)
    EditDate = Column(DateTime)
    EditUid = Column(Integer, ForeignKey('Users.Num'))
    ReviewDate = Column(DateTime)
    ReviewUid = Column(Integer, ForeignKey('Users.Num'))
    ApprovedDate = Column(DateTime)
    ApprovedUid = Column(Integer, ForeignKey('Users.Num'))
    flag = Column(Boolean)

    EditUser = relationship(lambda: Users, foreign_keys=[EditUid])
    ReviewUser = relationship(lambda: Users, foreign_keys=[ReviewUid])
    ApprovedUser= relationship(lambda: Users, foreign_keys=[ApprovedUid])


class BCHouse(Base):
    __tablename__ = 'BCHouse'

    BCNum = Column(Integer, primary_key = True, nullable = False)
    RecType = Column(SmallInteger, primary_key = True, nullable = False)
    RecNum = Column(Integer, primary_key = True, nullable = False)
    BCType = Column(SmallInteger)
    BCValue = Column(Unicode(10))
    flag = Column(Boolean)


class BCSet(Base):
    """
    Наборы граничных условий
    Набор значений постулированных событий, и/или изменений параметров базовых событий или операторов
    """
    __tablename__ = 'BCSet'

    Type = Column(SmallInteger, primary_key = True, nullable = False)
    Num = Column(Integer, Identity(start = 1, increment = 1), nullable = False, unique = True)
    ID = Column(Unicode(20), primary_key = True, nullable = False)
    Text = Column(Unicode(100))
    Tag = Column(SmallInteger)
    EditDate = Column(DateTime)
    EditUid = Column(Integer, ForeignKey('Users.Num'))
    ReviewDate = Column(DateTime)
    ReviewUid = Column(Integer, ForeignKey('Users.Num'))
    ApprovedDate = Column(DateTime)
    ApprovedUid = Column(Integer, ForeignKey('Users.Num'))
    flag = Column(Boolean)

    EditUser = relationship(lambda: Users, foreign_keys=[EditUid])
    ReviewUser = relationship(lambda: Users, foreign_keys=[ReviewUid])
    ApprovedUser= relationship(lambda: Users, foreign_keys=[ApprovedUid])


class BCSetAtt(Base):
    __tablename__ = 'BCSetAtt'

    BCNum = Column(Integer, primary_key = True, nullable = False)
    AttNum = Column(Integer, primary_key = True, nullable = False)
    flag = Column(Boolean)


t_BEBERelations = Table(
        'BEBERelations', metadata,
        Column('EventNum', Integer),
        Column('Type', SmallInteger),
        Column('Formula', Unicode(4000)),
        Column('Tag', SmallInteger)
)


class CCFEventPar(Base):
    __tablename__ = 'CCFEventPar'

    IDNum = Column(Integer, Identity(start = 1, increment = 1), primary_key = True)
    EventType = Column(SmallInteger, nullable = False)
    EventNum = Column(Integer, nullable = False)
    ParType = Column(SmallInteger)
    ParNum = Column(Integer)
    Value = Column(Float(24))
    flag = Column(Boolean)


class CCFGroup(Base):
    """
    Группы ООП
    Объекты, для которых указываются базовые события, к ним относящиеся.
    """
    __tablename__ = 'CCFGroup'

    Type = Column(SmallInteger, primary_key = True, nullable = False)
    Num = Column(Integer, Identity(start = 1, increment = 1), nullable = False, unique = True)
    ID = Column(Unicode(20), primary_key = True, nullable = False)
    Text = Column(Unicode(100))
    Tag = Column(SmallInteger)
    CCFModel = Column(SmallInteger)
    EditDate = Column(DateTime)
    EditUid = Column(Integer, ForeignKey('Users.Num'))
    ReviewDate = Column(DateTime)
    ReviewUid = Column(Integer, ForeignKey('Users.Num'))
    ApprovedDate = Column(DateTime)
    ApprovedUid = Column(Integer, ForeignKey('Users.Num'))
    flag = Column(Boolean)
    CCFAlpha8Bound = Column(Integer)

    EditUser = relationship(lambda: Users, foreign_keys=[EditUid])
    ReviewUser = relationship(lambda: Users, foreign_keys=[ReviewUid])
    ApprovedUser= relationship(lambda: Users, foreign_keys=[ApprovedUid])


class CCFRec(Base):
    __tablename__ = 'CCFRec'

    CCGType = Column(SmallInteger, primary_key = True, nullable = False)
    CCGNum = Column(Integer, primary_key = True, nullable = False)
    EventNum = Column(Integer, primary_key = True, nullable = False)
    EventType = Column(SmallInteger)
    flag = Column(Boolean)


class CCGBasic(Base):
    __tablename__ = 'CCGBasic'

    CCGType = Column(SmallInteger, primary_key = True, nullable = False)
    CCGNum = Column(Integer, primary_key = True, nullable = False)
    EventNum = Column(Integer, primary_key = True, nullable = False)
    EventType = Column(SmallInteger)
    flag = Column(Boolean)


class CompEvent(Base):
    __tablename__ = 'CompEvent'
    __table_args__ = (
        ForeignKeyConstraint(
            ['RecType1', 'RecNum1'],
            ['Components.Type','Components.Num'],
            name = 'fk_comp_entry'),
        ForeignKeyConstraint(
            ['RecType2', 'RecNum2'],
            ['Events.Type', 'Events.Num'],
            name = 'fk_event_entry'),
    )
    RecNum1 = Column(Integer, primary_key = True, nullable = False)
    RecNum2 = Column(Integer, primary_key = True, nullable = False)
    RecType1 = Column(SmallInteger, default = 24)
    RecType2 = Column(SmallInteger, default = 5)
    QueryFlag = Column(SmallInteger)
    FailMode = Column(Integer, ForeignKey('FailMode.Num'))
    flag = Column(Boolean)


class Components(Base):
    """
    Компоненты
    Объекты, объединяющие несколько базовых событий, относящихся к одной единице оборудования
    """
    __tablename__ = 'Components'

    Type = Column(SmallInteger, primary_key = True, nullable = False, default = 24)
    Num = Column(Integer, Identity(start = 1, increment = 1), nullable = False)
    ID = Column(Unicode(20), primary_key = True, nullable = False)
    Text = Column(Unicode(100))
    Tag = Column(SmallInteger, default = 0)
    EditDate = Column(DateTime)
    EditUid = Column(Integer, ForeignKey('Users.Num'))
    ReviewDate = Column(DateTime)
    ReviewUid = Column(Integer, ForeignKey('Users.Num'))
    ApprovedDate = Column(DateTime)
    ApprovedUid = Column(Integer, ForeignKey('Users.Num'))
    flag = Column(Boolean)

    BasicEvents = relationship(
            lambda: BasicEvents,
            secondary = lambda: CompEvent.__table__,
            primaryjoin = lambda: Components.Num == CompEvent.RecNum1 and Components.Type == CompEvent.Type1,
            secondaryjoin = lambda: BasicEvents.Num == CompEvent.RecNum2 and BasicEvents.Type == CompEvent.Type2,
            back_populates = 'Components')

    Systems = relationship(lambda: Systems, secondary=lambda: SysComp, back_populates = 'Components')

    EditUser = relationship(lambda: Users, foreign_keys=[EditUid])
    ReviewUser = relationship(lambda: Users, foreign_keys=[ReviewUid])
    ApprovedUser= relationship(lambda: Users, foreign_keys=[ApprovedUid])

class DistPoints(Base):
    __tablename__ = 'DistPoints'

    ParNum = Column(Integer, primary_key = True, nullable = False)
    Y = Column(Float(24), primary_key = True, nullable = False)
    X = Column(Float(24))
    flag = Column(Boolean)


t_Duplicated = Table(
        'Duplicated', metadata,
        Column('OldNum', Integer, nullable = False),
        Column('NewNum', Integer)
)


class EventTrees(Base):
    """Деревья событий """
    __tablename__ = 'ET'

    Type = Column(SmallInteger, primary_key = True, nullable = False)
    Num = Column(Integer, Identity(start = 1, increment = 1), nullable = False, unique = True)
    ID = Column(Unicode(20), primary_key = True, nullable = False)
    Text = Column(Unicode(100))
    Tag = Column(SmallInteger)
    Align = Column(SmallInteger)
    EditDate = Column(DateTime)
    EditUid = Column(Integer, ForeignKey('Users.Num'))
    ReviewDate = Column(DateTime)
    ReviewUid = Column(Integer, ForeignKey('Users.Num'))
    ApprovedDate = Column(DateTime)
    ApprovedUid = Column(Integer, ForeignKey('Users.Num'))
    flag = Column(Boolean)

    EditUser = relationship(lambda: Users, foreign_keys=[EditUid])
    ReviewUser = relationship(lambda: Users, foreign_keys=[ReviewUid])
    ApprovedUser= relationship(lambda: Users, foreign_keys=[ApprovedUid])


class ETEvents(Base):
    __tablename__ = 'ETEvents'

    ETNum = Column(Integer, primary_key = True, nullable = False)
    Pos = Column(SmallInteger, primary_key = True, nullable = False)
    EventType = Column(SmallInteger)
    EventNum = Column(Integer)
    flag = Column(Boolean)


class ETNodes(Base):
    """
     Ноды образуют граф взаимосвязей между функциональными событиями в дереве событий
    """
    __tablename__ = 'ETNodes'

    ETNum = Column(Integer, primary_key = True, nullable = False)
    Num = Column(SmallInteger, primary_key = True, nullable = False)
    FatherNum = Column(SmallInteger)
    HPos = Column(SmallInteger)
    VPos = Column(SmallInteger)
    AltNum = Column(SmallInteger)
    flag = Column(Boolean)


class ETSeq(Base):
    __tablename__ = 'ET_Seq'

    ETNum = Column(Integer, primary_key = True, nullable = False)
    SeqPos = Column(SmallInteger, primary_key = True, nullable = False)
    SeqNum = Column(Integer)
    FatherNum = Column(SmallInteger)
    flag = Column(Boolean)


class EventAtt(Base):
    __tablename__ = 'EventAtt'
    __table_args__ = (
        ForeignKeyConstraint(
            ['EventNum', 'EventType'],
            ['Events.Num', 'Events.Type'],
            name = 'fk_events_entry'),
        ForeignKeyConstraint(
            ['AttNum', 'AttType'],
            ['Attrib.Num','Attrib.Type'],
            name = 'fk_attrib_entry'),
    )

    EventNum = Column(Integer, primary_key = True, nullable = False)
    AttNum = Column(Integer, primary_key = True, nullable = False)
    EventType = Column(SmallInteger)
    AttType = Column(SmallInteger)
    flag = Column(Boolean)


t_EventExch = Table(
        'EventExch', metadata,
        Column('EventType', SmallInteger),
        Column('EventNum', Integer, nullable = False),
        Column('CondType', SmallInteger),
        Column('CondNum', Integer),
        Column('ExchType', SmallInteger),
        Column('ExchNum', Integer),
        Column('flag', Boolean),
        Index('IX_EventExch', 'EventNum', 'CondNum', unique = True)
)


class EventGroup(Base):
    """
    Группы базовых событий Объекты, при помощи которых можно анализировать влияние различных групп базовых событий на
    конечный результат квантификации. Каждое базовое событие может содержаться только в одной группе
    """
    __tablename__ = 'EventGroup'

    Type = Column(SmallInteger, primary_key = True, nullable = False)
    Num = Column(Integer, Identity(start = 1, increment = 1), nullable = False, unique = True)
    ID = Column(Unicode(20), primary_key = True, nullable = False)
    Text = Column(Unicode(100))
    Tag = Column(SmallInteger)
    EditDate = Column(DateTime)
    EditUid = Column(Integer, ForeignKey('Users.Num'))
    ReviewDate = Column(DateTime)
    ReviewUid = Column(Integer, ForeignKey('Users.Num'))
    ApprovedDate = Column(DateTime)
    ApprovedUid = Column(Integer, ForeignKey('Users.Num'))
    flag = Column(Boolean)

    EditUser = relationship(lambda: Users, foreign_keys=[EditUid])
    ReviewUser = relationship(lambda: Users, foreign_keys=[ReviewUid])
    ApprovedUser= relationship(lambda: Users, foreign_keys=[ApprovedUid])


class EventPar(Base):
    __tablename__ = 'EventPar'

    EventNum = Column(Integer, primary_key = True, nullable = False)
    ParType = Column(SmallInteger, primary_key = True, nullable = False)
    EventType = Column(SmallInteger)
    ParNum = Column(Integer)
    Value = Column(Float(24))
    flag = Column(Boolean)


class SymbolEnum(Enum):
    N = sqlalchemy.sql.null()
    Reserv1 = 0
    Oval = 1
    Diamond = 2
    House = 3
    CCFOval = 4
    Undefine = 5
    OR = 100
    AND = 200
    KN = 300
    XOR = 400
    Comment = 500
    Continuation = 900


class Events(Base):
    """
    События
    Таблица хранит перечень всех событий в моделе, см. типы событий
    """
    __tablename__ = 'Events'

    Type = Column(SmallInteger, primary_key = True, nullable = False)
    __mapper_args__ = {"polymorphic_on": Type}
    Num = Column(Integer, Identity(start = 1, increment = 1), nullable = False, unique = True)
    ID = Column(Unicode(20), primary_key = True, nullable = False)
    Text = Column(Unicode(100))
    Tag = Column(SmallInteger)
    Symbol = Column(SmallInteger)
    Model = Column(SmallInteger)
    State = Column(SmallInteger)
    CalcType = Column(SmallInteger)
    Mean = Column(Float(24))
    InitEnabl = Column(SmallInteger)
    EditDate = Column(DateTime)
    EditUid = Column(Integer, ForeignKey('Users.Num'))
    ReviewDate = Column(DateTime)
    ReviewUid = Column(Integer, ForeignKey('Users.Num'))
    ApprovedDate = Column(DateTime)
    ApprovedUid = Column(Integer, ForeignKey('Users.Num'))
    flag = Column(Boolean)

    Nodes = relationship(lambda: FTNodes, back_populates = 'Event')

    EditUser = relationship(lambda: Users, foreign_keys=[EditUid])
    ReviewUser = relationship(lambda: Users, foreign_keys=[ReviewUid])
    ApprovedUser= relationship(lambda: Users, foreign_keys=[ApprovedUid])


class BasicEvents(Events):
    """
    Базисное событие
    """
    __mapper_args__ = {'polymorphic_identity': 5}

    Components = relationship(
            lambda: Components,
            secondary = lambda: CompEvent.__table__,
            primaryjoin = lambda: BasicEvents.Num == CompEvent.RecNum2 and BasicEvents.Type == CompEvent.Type2,
            secondaryjoin = lambda: Components.Num == CompEvent.RecNum1 and Components.Type == CompEvent.Type1,
            back_populates = 'BasicEvents')

    Attributes = relationship(
            lambda: Attributes,
            secondary = lambda: EventAtt.__table__,
            primaryjoin = lambda: BasicEvents.Num == EventAtt.EventNum and BasicEvents.Type == EventAtt.EventType,
            secondaryjoin = lambda: Attributes.Num == EventAtt.AttNum and Attributes.Type == EventAtt.AttType,
            backref = 'BasicEvents')

    #Nodes = relationship(
    #        lambda: FTNodes,
    #        primaryjoin = lambda: BasicEvents.Num==FTNodes.RecNum and BasicEvents.Type==FTNodes.RecType,
    #        backref = "BasicEvents")

    #GetNodes = relationship(
    #        lambda: FTNodes,
    #        secondary =lambda: FTNodes.__table__,
    #        primaryjoin= lambda:BasicEvents.Num==FTNodes.RecNum and BasicEvents.Type==FTNodes.RecType,
    #        backref="BasicEvents")

    #FatherGate = relationship(
    #        lambda: Gates.__tablename__,
    #
    #)
    CCFGroup = relationship(
            lambda: CCFGroup,
            secondary = lambda: CCGBasic.__table__,
            primaryjoin = lambda: BasicEvents.Num == CCGBasic.EventNum and BasicEvents.Type==CCGBasic.EventType,
            secondaryjoin = lambda: CCGBasic.CCGNum == CCFGroup.Num and CCGBasic.CCGType==CCFGroup.Type,
            uselist = False,
            backref = "BasicEvents")





class Gates(Events):
    """Гейты"""
    __mapper_args__ = {'polymorphic_identity': 6}

    Attributes = relationship(
            lambda: Attributes,
            secondary = lambda: EventAtt.__table__,
            primaryjoin = lambda: Gates.Num == EventAtt.EventNum and Gates.Type == EventAtt.EventType,
            secondaryjoin = lambda: Attributes.Num == EventAtt.AttNum and Attributes.Type == EventAtt.AttType,
            backref = 'Events')

    #Nodes = relationship(
    #        lambda: FTNodes,
    #        primaryjoin = lambda: BasicEvents.Num==FTNodes.RecNum and BasicEvents.Type==FTNodes.RecType,
    #        backref = 'Gate')

class HouseEvents(Events):
    """
    House events
    Постулируемые базисные события
    """
    __mapper_args__ = {'polymorphic_identity': 7}

    Attributes = relationship(
            lambda: Attributes,
            secondary = lambda: EventAtt.__table__,
            primaryjoin = lambda: HouseEvents.Num == EventAtt.EventNum and HouseEvents.Type == EventAtt.EventType,
            secondaryjoin = lambda: Attributes.Num == EventAtt.AttNum and Attributes.Type == EventAtt.AttType,
            backref = 'HouseEvents')


class ConsequenceEvents(Events):
    """
    Sequence
    """
    __mapper_args__ = {'polymorphic_identity': 8}


class TemplateEvents(Events):
    """
        Собятия с фозможностью генерирования по шаблону
    """
    __mapper_args__ = {'polymorphic_identity': 9}
    Attributes = relationship(
            lambda: Attributes,
            secondary = lambda: EventAtt.__table__,
            primaryjoin = lambda: TemplateEvents.Num == EventAtt.EventNum and TemplateEvents.Type == EventAtt.EventType,
            secondaryjoin = lambda: Attributes.Num == EventAtt.AttNum and Attributes.Type == EventAtt.AttType,
            backref = 'TemplateEvents')


class InitiatingEvent(Events):
    """Исхожные события (в дереве событий)"""
    __mapper_args__ = {'polymorphic_identity': 10}


class FunctionEvents(Events):
    """Функциональные события (в дереве событий)"""
    __mapper_args__ = {'polymorphic_identity': 11}


class CCFEvent1(Events):
    """
    CCF1
    """
    __mapper_args__ = {'polymorphic_identity': 12}


class CCFEvent2(Events):
    """
    CCF2
    """
    __mapper_args__ = {'polymorphic_identity': 21}


class FEGroup(Base):
    __tablename__ = 'FEGroup'

    ETNum = Column(Integer, primary_key = True, nullable = False)
    FEMin = Column(SmallInteger, primary_key = True, nullable = False)
    FEMax = Column(SmallInteger)
    Text = Column(Unicode(100))
    flag = Column(Boolean)


class FunctionEventInputs(Base):
    """
    Таблица для связи между функциональными/исходными событиями и их воходными данными в виде последствий,
    бахзисных событий и гейтов
    """
    __tablename__ = 'FEInputs'

    AltNum = Column(Integer, primary_key = True, nullable = False)
    FEType = Column(SmallInteger, nullable = False)
    FENum = Column(Integer, primary_key = True, nullable = False)
    InputType = Column(SmallInteger)
    InputNum = Column(Integer)
    BCNum = Column(Integer)
    flag = Column(Boolean)


class FaultTrees(Base):
    """ Дерево отказов """
    __tablename__ = 'FT'

    Type = Column(SmallInteger, primary_key = True, nullable = False)
    __mapper_args__ = {"polymorphic_on": Type}
    Num = Column(Integer, Identity(start = 1, increment = 1), nullable = False, unique = True)
    ID = Column(Unicode(20), primary_key = True, nullable = False)
    Text = Column(Unicode(100))
    Tag = Column(SmallInteger)
    Align = Column(SmallInteger)
    EditDate = Column(DateTime)
    EditUid = Column(Integer, ForeignKey('Users.Num'))
    ReviewDate = Column(DateTime)
    ReviewUid = Column(Integer, ForeignKey('Users.Num'))
    ApprovedDate = Column(DateTime)
    ApprovedUid = Column(Integer, ForeignKey('Users.Num'))
    flag = Column(Boolean)
    IsPositioned = Column(SmallInteger, server_default = text('((0))'))

    EditUser = relationship(lambda: Users, foreign_keys=[EditUid])
    ReviewUser = relationship(lambda: Users, foreign_keys=[ReviewUid])
    ApprovedUser= relationship(lambda: Users, foreign_keys=[ApprovedUid])

    """Ноды связанные с деревом (События, гейты, итд) """
    Nodes = relationship(lambda: FTNodes, back_populates='FaultTree')

    """Топ(верхняя) нода"""
    TopGate = relationship(Gates,
                           secondary = lambda: FTNodes.__table__,
                           primaryjoin = lambda: FaultTrees.Num == FTNodes.FTNum and FTNodes.FatherGateNum == 0,
                           secondaryjoin = lambda: FTNodes.RecNum == Gates.Num and FTNodes.RecType == Gates.Type,
                           uselist = False,
                           viewonly = True)

    """Трансферные гейты """
    Transfers = relationship(lambda: Gates,
                             secondary = lambda: FTNodes.__table__,
                             primaryjoin = lambda: FaultTrees.Num == FTNodes.FTNum and FTNodes.Transfer == -1,
                             secondaryjoin = lambda: FTNodes.RecNum == Gates.Num,
                             viewonly = True)

    Gates = relationship(lambda: Gates,
                         secondary = lambda: FTNodes.__table__,
                         primaryjoin = lambda: FaultTrees.Num == FTNodes.FTNum,
                         secondaryjoin = lambda: FTNodes.RecNum == Gates.Num,
                         viewonly = True)

    BasicEvents = relationship(lambda: BasicEvents,
                               secondary = lambda: FTNodes.__table__,
                               primaryjoin = lambda: FaultTrees.Num == FTNodes.FTNum,
                               secondaryjoin = lambda: FTNodes.RecNum == BasicEvents.Num,
                               viewonly = True)


class CommonFailureTree(FaultTrees):
    """
    Обычные деревья отказов
    """
    __mapper_args__ = {'polymorphic_identity': 3}


class CCFFailureTree(FaultTrees):
    """
    Деревья отказов которые генерируются при создании ООП
    """
    __mapper_args__ = {'polymorphic_identity': 4}

class TransferEnum(Enum):
    Yes = -1
    Not = 0


class FTNodes(Base):
    """
    Ноды
    Объекты иерархически связанные между собой из которых набирается дерево отказов
    """
    __tablename__ = 'FTNodes'
    __table_args__ = (
        ForeignKeyConstraint(
                ["RecType", "RecNum"],
                ["Events.Type", "Events.Num"],
                name = 'fk_event_entry'),
    )

    FTNum = Column(Integer, ForeignKey('FT.Num'), primary_key = True, nullable = False)
    FatherGateNum = Column(Integer, ForeignKey("FTNodes.RecNum"), primary_key = True, nullable = False)
    """ см. Event.Type """
    RecType = Column(SmallInteger, primary_key = True, nullable = False)
    RecNum = Column(Integer, primary_key = True, nullable = False)
    """ Позиция по горизонтали в дереве отказов. Автоматически обновляется при открытии дерева в оболочке RiskSpectrum PSA """
    Pos = Column(SmallInteger, primary_key = True, nullable = False)
    """ Позиция по вертикали в FT """
    InLevel = Column(SmallInteger, primary_key = True, nullable = False)
    """ -1 - трансфер; 0 - не трансфер """
    Transfer = Column(SmallInteger, default = 0)
    Neg = Column(SmallInteger, default = 0)
    flag = Column(Boolean)

    """Событие ноды"""
    Event = relationship(Events, back_populates= 'Nodes', uselist=False, lazy='select')
    """Верхняя нода"""
    FatherNode = relationship(lambda: FTNodes,  remote_side=[RecNum], backref='ChildNodes', lazy='select')
    """Дерево отказов"""
    FaultTree = relationship(FaultTrees,  back_populates='Nodes', uselist=False, lazy='select')

class FailMode(Base):
    __tablename__ = 'FailMode'

    Type = Column(SmallInteger, primary_key = True, nullable = False)
    Num = Column(Integer, Identity(start = 1, increment = 1), nullable = False, unique = True)
    ID = Column(Unicode(20), primary_key = True, nullable = False)
    Text = Column(Unicode(100))
    Tag = Column(SmallInteger)
    EditDate = Column(DateTime)
    EditUid = Column(Integer, ForeignKey('Users.Num'))
    ReviewDate = Column(DateTime)
    ReviewUid = Column(Integer, ForeignKey('Users.Num'))
    ApprovedDate = Column(DateTime)
    ApprovedUid = Column(Integer, ForeignKey('Users.Num'))
    flag = Column(Boolean)

    EditUser = relationship(lambda: Users, foreign_keys=[EditUid])
    ReviewUser = relationship(lambda: Users, foreign_keys=[ReviewUid])
    ApprovedUser= relationship(lambda: Users, foreign_keys=[ApprovedUid])


class GroupSpec(Base):
    __tablename__ = 'GroupSpec'

    IDNum = Column(Integer, Identity(start = 1, increment = 1), primary_key = True)
    RecType = Column(SmallInteger, nullable = False)
    RecNum = Column(Integer, nullable = False)
    Type = Column(SmallInteger, nullable = False)
    IDFilter = Column(Unicode(20))
    flag = Column(Boolean)


class ImpSetup(Base):
    """
    Спецификации анализа значимости
    Объект, определяющий параметры процесса анализа значимости для сеанса квантификации
    """
    __tablename__ = 'ImpSetup'

    Type = Column(SmallInteger, primary_key = True, nullable = False)
    Num = Column(Integer, Identity(start = 1, increment = 1), nullable = False)
    ID = Column(Unicode(20), primary_key = True, nullable = False)
    Text = Column(Unicode(100))
    Tag = Column(SmallInteger)
    CalcType = Column(SmallInteger)
    Time = Column(Float(24))
    SensFactor = Column(Float(24))
    Bas = Column(SmallInteger)
    CCFGroup = Column(SmallInteger)
    Par = Column(SmallInteger)
    Att = Column(SmallInteger)
    Sys = Column(SmallInteger)
    Comp = Column(SmallInteger)
    BEGroup = Column(SmallInteger)
    MCSCut = Column(Float(24))
    RefreshData = Column(SmallInteger)
    Extra = Column(Integer)
    EditDate = Column(DateTime)
    EditUid = Column(Integer, ForeignKey('Users.Num'))
    ReviewDate = Column(DateTime)
    ReviewUid = Column(Integer, ForeignKey('Users.Num'))
    ApprovedDate = Column(DateTime)
    ApprovedUid = Column(Integer, ForeignKey('Users.Num'))
    flag = Column(Boolean)

    EditUser = relationship(lambda: Users, foreign_keys=[EditUid])
    ReviewUser = relationship(lambda: Users, foreign_keys=[ReviewUid])
    ApprovedUser= relationship(lambda: Users, foreign_keys=[ApprovedUid])


class LockUnLockHistory(Base):
    __tablename__ = 'LockUnLockHistory'

    Num = Column(Integer, Identity(start = 1, increment = 1), primary_key = True)
    EditUid = Column(Integer)
    EditDate = Column(DateTime)
    LockStatus = Column(Boolean)


class MCSPP(Base):
    __tablename__ = 'MCSPP'

    Type = Column(SmallInteger, primary_key = True, nullable = False)
    Num = Column(Integer, Identity(start = 1, increment = 1), nullable = False, unique = True)
    ID = Column(Unicode(20), primary_key = True, nullable = False)
    Text = Column(Unicode(100))
    Tag = Column(SmallInteger)
    EditDate = Column(DateTime)
    EditUid = Column(Integer, ForeignKey('Users.Num'))
    ReviewDate = Column(DateTime)
    ReviewUid = Column(Integer, ForeignKey('Users.Num'))
    ApprovedDate = Column(DateTime)
    ApprovedUid = Column(Integer, ForeignKey('Users.Num'))
    flag = Column(Boolean)

    EditUser = relationship(lambda: Users, foreign_keys=[EditUid])
    ReviewUser = relationship(lambda: Users, foreign_keys=[ReviewUid])
    ApprovedUser= relationship(lambda: Users, foreign_keys=[ApprovedUid])


class MCSPPRules(Base):
    __tablename__ = 'MCSPPRules'

    IDNum = Column(Integer, Identity(start = 1, increment = 1), primary_key = True)
    RecType = Column(SmallInteger, nullable = False)
    RecNum = Column(Integer, nullable = False)
    Type = Column(SmallInteger, nullable = False)
    IDFilter1 = Column(Unicode(21))
    IDFilter2 = Column(Unicode(21))
    IDFilter3 = Column(Unicode(21))
    IDFilter4 = Column(Unicode(21))
    IDFilter5 = Column(Unicode(21))
    IDFilter6 = Column(Unicode(21))
    IDFilter7 = Column(Unicode(21))
    IDFilter8 = Column(Unicode(21))
    IDFilter9 = Column(Unicode(21))
    IDFilter10 = Column(Unicode(21))
    flag = Column(Boolean)


class MCSPPSetup(Base):
    __tablename__ = 'MCSPPSetup'

    Type = Column(SmallInteger, primary_key = True, nullable = False)
    Num = Column(Integer, Identity(start = 1, increment = 1), nullable = False, unique = True)
    ID = Column(Unicode(20), primary_key = True, nullable = False)
    Text = Column(Unicode(100))
    Tag = Column(SmallInteger)
    EditDate = Column(DateTime)
    EditUid = Column(Integer, ForeignKey('Users.Num'))
    ReviewDate = Column(DateTime)
    ReviewUid = Column(Integer, ForeignKey('Users.Num'))
    ApprovedDate = Column(DateTime)
    ApprovedUid = Column(Integer, ForeignKey('Users.Num'))
    flag = Column(Boolean)

    EditUser = relationship(lambda: Users, foreign_keys=[EditUid])
    ReviewUser = relationship(lambda: Users, foreign_keys=[ReviewUid])
    ApprovedUser= relationship(lambda: Users, foreign_keys=[ApprovedUid])


class MCSPPSetupAction(Base):
    __tablename__ = 'MCSPPSetupAction'

    SetupNum = Column(Integer, primary_key = True, nullable = False)
    PPNum = Column(Integer, primary_key = True, nullable = False)
    SetupType = Column(SmallInteger)
    PPType = Column(SmallInteger)
    flag = Column(Boolean)


class MCSSetup(Base):
    """
    Спецификации анализа минимальных сечений
    Объект, определяющий параметры процесса анализа минимальных сечений для сеанса квантификации
    """
    __tablename__ = 'MCSSetup'

    Type = Column(SmallInteger, primary_key = True, nullable = False)
    Num = Column(Integer, Identity(start = 1, increment = 1), nullable = False, unique = True)
    ID = Column(Unicode(20), primary_key = True, nullable = False)
    Text = Column(Unicode(100))
    Tag = Column(SmallInteger)
    CalcType = Column(SmallInteger)
    Time = Column(Float(24))
    CutoffType = Column(SmallInteger)
    AbsCutoff = Column(Float(24))
    RelCutoff = Column(Float(24))
    Approx = Column(SmallInteger)
    Negated = Column(SmallInteger)
    IncCCF = Column(SmallInteger)
    MaxMod = Column(Integer)
    MaxDemod = Column(Integer)
    SaveCutoff = Column(Float(24))
    RefreshData = Column(SmallInteger)
    Extra = Column(Integer)
    EditDate = Column(DateTime)
    EditUid = Column(Integer, ForeignKey('Users.Num'))
    ReviewDate = Column(DateTime)
    ReviewUid = Column(Integer, ForeignKey('Users.Num'))
    ApprovedDate = Column(DateTime)
    ApprovedUid = Column(Integer, ForeignKey('Users.Num'))
    flag = Column(Boolean)

    EditUser = relationship(lambda: Users, foreign_keys=[EditUid])
    ReviewUser = relationship(lambda: Users, foreign_keys=[ReviewUid])
    ApprovedUser= relationship(lambda: Users, foreign_keys=[ApprovedUid])


class MemoRefs(Base):
    __tablename__ = 'MemoRefs'

    MemoNum = Column(Integer, primary_key = True, nullable = False)
    RecType = Column(SmallInteger, primary_key = True, nullable = False)
    RecNum = Column(Integer, primary_key = True, nullable = False)
    MemoType = Column(SmallInteger)
    flag = Column(Boolean)


class Memo(Base):
    """
    Комментарии
    Текст в свободной форме
    """
    __tablename__ = 'Memo'

    Type = Column(SmallInteger, primary_key = True, nullable = False)
    Num = Column(Integer, Identity(start = 1, increment = 1), nullable = False, unique = True)
    ID = Column(Unicode(20), primary_key = True, nullable = False)
    Text = Column(Unicode(100))
    Tag = Column(SmallInteger)
    Note = Column(NTEXT(1073741823))
    EditDate = Column(DateTime)
    EditUid = Column(Integer, ForeignKey('Users.Num'))
    ReviewDate = Column(DateTime)
    ReviewUid = Column(Integer, ForeignKey('Users.Num'))
    ApprovedDate = Column(DateTime)
    ApprovedUid = Column(Integer, ForeignKey('Users.Num'))
    flag = Column(Boolean)

    EditUser = relationship(lambda: Users, foreign_keys=[EditUid])
    ReviewUser = relationship(lambda: Users, foreign_keys=[ReviewUid])
    ApprovedUser= relationship(lambda: Users, foreign_keys=[ApprovedUid])

    '''
    FaultTrees = relationship(FaultTrees,
                            secondary=MemoRefs.__table__,
                            primaryjoin= lambda: Memo.Num == MemoRefs.MemoNum and Memo.Type == MemoRefs.MemoType,
                            secondaryjoin= FaultTrees.Num == MemoRefs.RecNum and FaultTrees.Type == MemoRefs.RecType,
                            backref='Memos')

    BasicEvents = relationship(BasicEvents,
                    secondary=MemoRefs.__table__,
                    primaryjoin=lambda: Memo.Num == MemoRefs.MemoNum and Memo.Type == MemoRefs.MemoType,
                    secondaryjoin=BasicEvents.Num == MemoRefs.RecNum and BasicEvents.Type == MemoRefs.RecType,
                    backref = 'Memos')

    Sequences = relationship(lambda: Sequence,
                    secondary=MemoRefs.__table__,
                    primaryjoin=lambda: Memo.Num == MemoRefs.MemoNum and Memo.Type == MemoRefs.MemoType,
                    secondaryjoin= lambda: Sequence.Num == MemoRefs.RecNum and Sequence.Type == MemoRefs.RecType,
                    backref = 'Memos')

    Gates = relationship(Gates,
                    secondary=MemoRefs.__table__,
                    primaryjoin=lambda: Memo.Num == MemoRefs.MemoNum and Memo.Type == MemoRefs.MemoType,
                    secondaryjoin=Gates.Num == MemoRefs.RecNum and Gates.Type == MemoRefs.RecType,
                    backref = 'Memos')

    HouseEvents = relationship(HouseEvents,
                    secondary=MemoRefs.__table__,
                    primaryjoin=lambda: Memo.Num == MemoRefs.MemoNum and Memo.Type == MemoRefs.MemoType,
                    secondaryjoin=HouseEvents.Num == MemoRefs.RecNum and HouseEvents.Type == MemoRefs.RecType,
                    backref = 'Memos')

    CCFGroups = relationship(CCFGroup,
                    secondary=MemoRefs.__table__,
                    primaryjoin=lambda: Memo.Num == MemoRefs.MemoNum and Memo.Type == MemoRefs.MemoType,
                    secondaryjoin=CCFGroup.Num == MemoRefs.RecNum and CCFGroup.Type == MemoRefs.RecType,
                    backref = 'Memos')
    '''


t_MuxEvents = Table(
        'MuxEvents', metadata,
        Column('MuxType', SmallInteger),
        Column('MuxNum', Integer),
        Column('EventType', SmallInteger),
        Column('EventNum', Integer)
)

t_MuxSets = Table(
        'MuxSets', metadata,
        Column('Num', Integer, Identity(start = 1, increment = 1), nullable = False),
        Column('Type', SmallInteger),
        Column('ID', Unicode(20)),
        Column('Tag', SmallInteger)
)


class Params(Base):
    """
    Параметры
    Объекты, содержащие численные значения, используемые при квантификации моделей.
    """
    __tablename__ = 'Params'
    Type = Column(SmallInteger, primary_key = True, nullable = False)
    __mapper_args__ = {"polymorphic_on": Type}
    Num = Column(Integer, Identity(start = 1, increment = 1), nullable = False, unique = True)
    ID = Column(Unicode(20), primary_key = True, nullable = False)
    Text = Column(Unicode(100))
    Tag = Column(SmallInteger)
    Mean = Column(Float(24))
    DistType = Column(SmallInteger)
    DistPar1 = Column(Float(24))
    DistPar2 = Column(Float(24))
    DistPar3 = Column(Float(24))
    Unit = Column(SmallInteger)
    Median = Column(Float(24))
    P05 = Column(Float(24))
    P95 = Column(Float(24))
    VarCoeff = Column(Float(24))
    EditDate = Column(DateTime)
    EditUid = Column(Integer, ForeignKey('Users.Num'))
    ReviewDate = Column(DateTime)
    ReviewUid = Column(Integer, ForeignKey('Users.Num'))
    ApprovedDate = Column(DateTime)
    ApprovedUid = Column(Integer, ForeignKey('Users.Num'))
    flag = Column(Boolean)

    EditUser = relationship(lambda: Users, foreign_keys=[EditUid])
    ReviewUser = relationship(lambda: Users, foreign_keys=[ReviewUid])
    ApprovedUser= relationship(lambda: Users, foreign_keys=[ApprovedUid])


class ProbabilityParam(Params):
    """
    Тип параметра Probability
    """
    __mapper_args__ = {"polymorphic_identity": 14}


class FailureRateParam(Params):
    """
    Тип параметра Falilure Rate
    """
    __mapper_args__ = {
        "polymorphic_identity": 15
    }


class FrequencyParam(Params):
    """
    Тип параметра Frequency
    """
    __mapper_args__ = {
        "polymorphic_identity": 16
    }


class MTTRParam(Params):
    """
    Тип параметра MTTR
    """
    __mapper_args__ = {
        "polymorphic_identity": 17
    }


class TestIntervalParam(Params):
    """
    Тип параметра TestInterval
    """
    __mapper_args__ = {
        "polymorphic_identity": 18
    }


class MissionTimeParam(Params):
    """
    Тип параметра Mission Time
    """
    __mapper_args__ = {
        "polymorphic_identity": 20
    }


class BeatFactorParam(Params):
    """
    Тип параметра для отказов по общей причине Beta Factor
    """
    __mapper_args__ = {
        "polymorphic_identity": 43
    }


class Alpha2FactorParam(Params):
    """
    Тип параметра для отказа по общей причине Альфа 2 фактор
    """
    __mapper_args__ = {
        "polymorphic_identity": 47
    }


class Alpha3FactorParam(Params):
    """
    Тип параметра для отказа по общей причине Альфа 3 фактор
    """
    __mapper_args__ = {
        "polymorphic_identity": 48
    }


class Alpha4FactorParam(Params):
    """
    Тип параметра для отказа по общей причине Альфа 4 фактор
    """
    __mapper_args__ = {
        "polymorphic_identity": 49
    }


class Alpha5FactorParam(Params):
    """
    Тип параметра для отказа по общей причине Альфа 5 фактор
    """
    __mapper_args__ = {
        "polymorphic_identity": 56
    }


class Alpha6FactorParam(Params):
    """
    Тип параметра для отказа по общей причине Альфа 6 фактор
    """
    __mapper_args__ = {
        "polymorphic_identity": 57
    }


class Alpha7FactorParam(Params):
    """
    Тип параметра для отказа по общей причине Альфа 7 фактор
    """
    __mapper_args__ = {
        "polymorphic_identity": 58
    }


class Alpha8FactorParam(Params):
    """
    Тип параметра для отказа по общей причине Альфа 8 фактор
    """
    __mapper_args__ = {
        "polymorphic_identity": 59
    }


t_ProjSettings = Table(
        'ProjSettings', metadata,
        Column('Num', Integer, Identity(start = 1, increment = 1), nullable = False),
        Column('Type', SmallInteger),
        Column('ID', Unicode(40)),
        Column('SettingValue', Unicode(40)),
        Column('Tag', SmallInteger)
)


class Propagated(Base):
    __tablename__ = 'Propagated'

    Num = Column(Integer, primary_key = True)
    OriginalState = Column(SmallInteger, nullable = False)


class Properties(Base):
    __tablename__ = 'Properties'

    Num = Column(SmallInteger, primary_key = True)
    Text = Column(Unicode(300))
    EditDate = Column(DateTime)
    EditUid = Column(Integer, ForeignKey('Users.Num'))
    ReviewDate = Column(DateTime)
    ReviewUid = Column(Integer, ForeignKey('Users.Num'))
    ApprovedDate = Column(DateTime)
    ApprovedUid = Column(Integer, ForeignKey('Users.Num'))
    flag = Column(Boolean)

    EditUser = relationship(lambda: Users, foreign_keys=[EditUid])
    ReviewUser = relationship(lambda: Users, foreign_keys=[ReviewUid])
    ApprovedUser= relationship(lambda: Users, foreign_keys=[ApprovedUid])


class RepFields(Base):
    __tablename__ = 'RepFields'

    RepNum = Column(Integer, primary_key = True, nullable = False)
    FieldNum = Column(SmallInteger, primary_key = True, nullable = False)
    flag = Column(Boolean)


class RepRel(Base):
    __tablename__ = 'RepRel'

    RepNum = Column(Integer, primary_key = True, nullable = False)
    RelNum = Column(SmallInteger, primary_key = True, nullable = False)
    flag = Column(Boolean)


class Report(Base):
    __tablename__ = 'Report'

    Type = Column(SmallInteger, primary_key = True, nullable = False)
    Num = Column(Integer, Identity(start = 1, increment = 1), nullable = False)
    ID = Column(Unicode(40), primary_key = True, nullable = False)
    HeaderFirstPageOnly = Column(Boolean, nullable = False)
    FooterLastPageOnly = Column(Boolean, nullable = False)
    Text = Column(Unicode(100))
    Tag = Column(SmallInteger)
    DefaultValue = Column(SmallInteger)
    ReportType = Column(SmallInteger)
    FontName1 = Column(Unicode(40))
    FontSize1 = Column(Float(24))
    FontBold1 = Column(SmallInteger)
    FontItalic1 = Column(SmallInteger)
    FontUnderline1 = Column(SmallInteger)
    ForeColor1 = Column(Integer)
    FontName2 = Column(Unicode(40))
    FontSize2 = Column(Float(24))
    FontBold2 = Column(SmallInteger)
    FontItalic2 = Column(SmallInteger)
    FontUnderline2 = Column(SmallInteger)
    ForeColor2 = Column(Integer)
    FontName3 = Column(Unicode(40))
    FontSize3 = Column(Float(24))
    FontBold3 = Column(SmallInteger)
    FontItalic3 = Column(SmallInteger)
    FontUnderline3 = Column(SmallInteger)
    ForeColor3 = Column(Integer)
    LeftMargin = Column(SmallInteger)
    RightMargin = Column(SmallInteger)
    TopMargin = Column(SmallInteger)
    BottomMargin = Column(SmallInteger)
    HeaderLeft = Column(Unicode(100))
    HeaderCenter = Column(Unicode(100))
    HeaderRight = Column(Unicode(100))
    FooterLeft = Column(Unicode(100))
    FooterCenter = Column(Unicode(100))
    FooterRight = Column(Unicode(100))
    PageFrame = Column(SmallInteger)
    TableFrame = Column(SmallInteger)
    IDColWidth = Column(SmallInteger)
    MaxMCS = Column(SmallInteger)
    MaxImportance = Column(SmallInteger)
    FitToPage = Column(SmallInteger)
    QueryFlag = Column(SmallInteger)
    ETCol1Width = Column(SmallInteger)
    ETCol2Width = Column(SmallInteger)
    ETCol3Width = Column(SmallInteger)
    ETCol4Width = Column(SmallInteger)
    ETCol5Width = Column(SmallInteger)
    NoFE = Column(SmallInteger)
    NoSequence = Column(SmallInteger)
    EditDate = Column(DateTime)
    EditUid = Column(Integer, ForeignKey('Users.Num'))
    ReviewDate = Column(DateTime)
    ReviewUid = Column(Integer, ForeignKey('Users.Num'))
    ApprovedDate = Column(DateTime)
    ApprovedUid = Column(Integer, ForeignKey('Users.Num'))
    flag = Column(Boolean)

    EditUser = relationship(lambda: Users, foreign_keys=[EditUid])
    ReviewUser = relationship(lambda: Users, foreign_keys=[ReviewUid])
    ApprovedUser= relationship(lambda: Users, foreign_keys=[ApprovedUid])


class SeqCon(Base):
    __tablename__ = 'SeqCon'
    __table_args__ = (
        ForeignKeyConstraint(
            ['EventNum', 'EventType'],
            ['Events.Num','Events.Type'],
            name = 'fk_conseq_entry'),
    )
    SeqNum = Column(Integer, ForeignKey('Sequence.Num'), primary_key = True, nullable = False)
    EventNum = Column(Integer, primary_key = True, nullable = False)
    EventType = Column(SmallInteger)
    flag = Column(Boolean)


class Sequence(Base):
    __tablename__ = 'Sequence'

    Type = Column(SmallInteger, primary_key = True, nullable = False)
    Num = Column(Integer, Identity(start = 1, increment = 1), nullable = False, unique = True)
    ID = Column(Unicode(255), primary_key = True, nullable = False)
    Text = Column(Unicode(100))
    Tag = Column(SmallInteger)
    CalcType = Column(SmallInteger)
    Mean = Column(Float(24))
    EditDate = Column(DateTime)
    EditUid = Column(Integer)
    ReviewDate = Column(DateTime)
    ReviewUid = Column(Integer)
    ApprovedDate = Column(DateTime)
    ApprovedUid = Column(Integer)
    flag = Column(Boolean)


class SysBC(Base):
    __tablename__ = 'SysBC'

    SysNum = Column(Integer, primary_key = True, nullable = False)
    BCNum = Column(Integer, primary_key = True, nullable = False)
    flag = Column(Boolean)


class SysComp(Base):
    """
    Промежуточная таблица связи между системами и компонентами
    """
    __tablename__ = 'SysComp'
    __table_args__ = (
        ForeignKeyConstraint(
            ['RecType1', 'RecNum1'],
            ['Systems.Type', 'Systems.Num'],
            name = 'fk_system_entry'),
        ForeignKeyConstraint(
            ['RecType2', 'RecNum2'],
            ['Components.Type','Components.Num'],
            name = 'fk_comp_entry'),
    )
    RecNum1 = Column(Integer, primary_key = True, nullable = False)
    RecNum2 = Column(Integer, primary_key = True, nullable = False)
    RecType1 = Column(SmallInteger)
    RecType2 = Column(SmallInteger)
    flag = Column(Boolean)


class SysFT(Base):
    """
    Промежуточная таблица связи между системами и деревьями отказов
    """
    __tablename__ = 'SysFT'
    __table_args__ = (
        ForeignKeyConstraint(
            ['RecType1', 'RecNum1'],
            ['Systems.Type','Systems.Num'],
            name = 'fk_comp_entry'),
        ForeignKeyConstraint(
            ['RecType2', 'RecNum2'],
            ['FT.Type', 'FT.Num'],
            name = 'fk_event_entry'),
    )
    RecNum1 = Column(Integer, primary_key = True, nullable = False)
    RecNum2 = Column(Integer, primary_key = True, nullable = False)
    RecType1 = Column(SmallInteger)
    RecType2 = Column(SmallInteger)
    flag = Column(Boolean)


class SysGate(Base):
    """
    Промежуточная таблица связи между системами и гейтами
    """
    __tablename__ = 'SysGate'

    SysNum = Column(Integer, ForeignKey('Systems.Num'), primary_key = True, nullable = False)
    EventNum = Column(Integer, ForeignKey('Events.Num'), primary_key = True, nullable = False)
    flag = Column(Boolean)


class SysSubsys(Base):
    __tablename__ = 'SysSubsys'

    SysNum = Column(Integer, ForeignKey('Systems.Num'), primary_key = True, nullable = False)
    SubsysNum = Column(Integer, primary_key = True, nullable = False)
    flag = Column(Boolean)


class SysTestProc(Base):
    __tablename__ = 'SysTestProc'

    SysNum = Column(Integer, ForeignKey('Systems.Num'), primary_key = True, nullable = False)
    TestProcNum = Column(Integer, ForeignKey('TestProc.Num'), primary_key = True, nullable = False)
    flag = Column(Boolean)


class Systems(Base):
    """
    Сиcтемы
    Объекты, объединяющие компоненты, входящие в одну систему
    """
    __tablename__ = 'Systems'

    Type = Column(SmallInteger, primary_key = True, nullable = False)
    Num = Column(Integer, Identity(start = 1, increment = 1), nullable = False)
    ID = Column(Unicode(20), primary_key = True, nullable = False)
    Text = Column(Unicode(100))
    Tag = Column(SmallInteger)
    EditDate = Column(DateTime)
    EditUid = Column(Integer, ForeignKey('Users.Num'))
    ReviewDate = Column(DateTime)
    ReviewUid = Column(Integer, ForeignKey('Users.Num'))
    ApprovedDate = Column(DateTime)
    ApprovedUid = Column(Integer, ForeignKey('Users.Num'))
    flag = Column(Boolean)

    SubSystems = relationship(lambda: Systems,
                              secondary = SysSubsys.__table__,
                              primaryjoin = lambda: Systems.Num == SysSubsys.SysNum,
                              secondaryjoin = lambda: Systems.Num == SysSubsys.SubsysNum,
                              backref = 'ParentSystems')

    #Components = relationship(Components,
    #                          secondary = SysComp.__table__,
    #                          primaryjoin = lambda: Systems.Num == SysComp.RecNum1 and Systems.Type == SysComp.RecType1,
    #                          secondaryjoin = Components.Num == SysComp.RecNum2 and Components.Type == SysComp.RecType2,
    #                          backref = 'Systems')
    Components = relationship(lambda: Components, secondary=SysComp, back_populates = 'Systems')

    FaultTrees = relationship(FaultTrees,
                              secondary = SysFT.__table__,
                              primaryjoin = lambda: Systems.Num == SysFT.RecNum1 and Systems.Type == SysFT.RecType1,
                              secondaryjoin = FaultTrees.Num == SysFT.RecNum2 and FaultTrees.Type == SysFT.RecType2,
                              backref = 'Systems')

    TopGates = relationship(Gates,
                            secondary = SysGate.__table__,
                            primaryjoin = lambda: Systems.Num == SysGate.SysNum,
                            secondaryjoin = Gates.Num == SysGate.EventNum,
                            backref = 'Systems')

    BCSets = relationship(lambda: BCSet,
                          secondary = SysBC.__table__,
                          primaryjoin = lambda: Systems.Num == SysBC.SysNum,
                          secondaryjoin = lambda: BCSet.Num == SysBC.BCNum,
                          backref = 'Systems')
    TestProcedures = relationship(lambda: TestProc,
                                  secondary = SysTestProc.__table__,
                                  primaryjoin = lambda: Systems.Num == SysTestProc.SysNum,
                                  secondaryjoin = lambda: TestProc.Num == SysTestProc.TestProcNum,
                                  backref = 'Systems')

    EditUser = relationship(lambda: Users, foreign_keys=[EditUid])
    ReviewUser = relationship(lambda: Users, foreign_keys=[ReviewUid])
    ApprovedUser= relationship(lambda: Users, foreign_keys=[ApprovedUid])


class TDSetup(Base):
    __tablename__ = 'TDSetup'

    Type = Column(SmallInteger, primary_key = True, nullable = False)
    Num = Column(Integer, Identity(start = 1, increment = 1), nullable = False, unique = True)
    ID = Column(Unicode(20), primary_key = True, nullable = False)
    Text = Column(Unicode(100))
    Tag = Column(SmallInteger)
    Time1 = Column(Float(24))
    Time2 = Column(Float(24))
    MCSCut = Column(Float(24))
    RefreshData = Column(SmallInteger)
    Extra = Column(Integer)
    EditDate = Column(DateTime)
    EditUid = Column(Integer, ForeignKey('Users.Num'))
    ReviewDate = Column(DateTime)
    ReviewUid = Column(Integer, ForeignKey('Users.Num'))
    ApprovedDate = Column(DateTime)
    ApprovedUid = Column(Integer, ForeignKey('Users.Num'))
    flag = Column(Boolean)

    EditUser = relationship(lambda: Users, foreign_keys=[EditUid])
    ReviewUser = relationship(lambda: Users, foreign_keys=[ReviewUid])
    ApprovedUser= relationship(lambda: Users, foreign_keys=[ApprovedUid])


class TestProc(Base):
    __tablename__ = 'TestProc'

    Type = Column(SmallInteger, primary_key = True, nullable = False)
    Num = Column(Integer, Identity(start = 1, increment = 1), nullable = False, unique = True)
    ID = Column(Unicode(20), primary_key = True, nullable = False)
    Text = Column(Unicode(100))
    Tag = Column(SmallInteger)
    EditDate = Column(DateTime)
    EditUid = Column(Integer, ForeignKey('Users.Num'))
    ReviewDate = Column(DateTime)
    ReviewUid = Column(Integer, ForeignKey('Users.Num'))
    ApprovedDate = Column(DateTime)
    ApprovedUid = Column(Integer, ForeignKey('Users.Num'))
    flag = Column(Boolean)

    EditUser = relationship(lambda: Users, foreign_keys=[EditUid])
    ReviewUser = relationship(lambda: Users, foreign_keys=[ReviewUid])
    ApprovedUser= relationship(lambda: Users, foreign_keys=[ApprovedUid])


class TestProcEvent(Base):
    __tablename__ = 'TestProc_Event'

    TestProcNum = Column(Integer, ForeignKey('TestProc.Num'), primary_key = True, nullable = False)
    EventNum = Column(Integer, ForeignKey('Events.Num'), primary_key = True, nullable = False)
    TestEff = Column(Float(24))
    flag = Column(Boolean)


class TextMacro(Base):
    __tablename__ = 'TextMacro'

    Num = Column(SmallInteger, primary_key = True)
    Text = Column(Unicode(100))
    EditDate = Column(DateTime)
    EditUid = Column(Integer, ForeignKey('Users.Num'))
    ReviewDate = Column(DateTime)
    ReviewUid = Column(Integer, ForeignKey('Users.Num'))
    ApprovedDate = Column(DateTime)
    ApprovedUid = Column(Integer, ForeignKey('Users.Num'))
    flag = Column(Boolean)

    EditUser = relationship(lambda: Users, foreign_keys=[EditUid])
    ReviewUser = relationship(lambda: Users, foreign_keys=[ReviewUid])
    ApprovedUser= relationship(lambda: Users, foreign_keys=[ApprovedUid])


class TopAcase(Base):
    __tablename__ = 'TopAcase'

    AcaseNum = Column(Integer, primary_key = True)
    TopType = Column(SmallInteger)
    TopNum = Column(Integer)
    AcaseType = Column(SmallInteger)
    flag = Column(Boolean)


class UncSetup(Base):
    """
    Спецификации анализа неопределенности
    Объект, определяющий параметры процесса анализа неопределенности для сеанса квантификации
    """
    __tablename__ = 'UncSetup'

    Type = Column(SmallInteger, primary_key = True, nullable = False)
    Num = Column(Integer, Identity(start = 1, increment = 1), nullable = False, unique = True)
    ID = Column(Unicode(20), primary_key = True, nullable = False)
    Text = Column(Unicode(100))
    Tag = Column(SmallInteger)
    CalcType = Column(SmallInteger)
    Time = Column(Float(24))
    SimType = Column(SmallInteger)
    NumSim = Column(Integer)
    RandType = Column(SmallInteger)
    Seed = Column(SmallInteger)
    MCSCut = Column(Float(24))
    ImpCut = Column(Float(24))
    RefreshData = Column(SmallInteger)
    Extra = Column(Integer)
    EditDate = Column(DateTime)
    EditUid = Column(Integer, ForeignKey('Users.Num'))
    ReviewDate = Column(DateTime)
    ReviewUid = Column(Integer, ForeignKey('Users.Num'))
    ApprovedDate = Column(DateTime)
    ApprovedUid = Column(Integer, ForeignKey('Users.Num'))
    flag = Column(Boolean)

    EditUser = relationship(lambda: Users, foreign_keys=[EditUid])
    ReviewUser = relationship(lambda: Users, foreign_keys=[ReviewUid])
    ApprovedUser= relationship(lambda: Users, foreign_keys=[ApprovedUid])


t_UncertaintyFiles = Table(
        'UncertaintyFiles', metadata,
        Column('Num', Integer, Identity(start = 1, increment = 1), nullable = False),
        Column('Type', SmallInteger),
        Column('ID', Unicode(100)),
        Column('FileBinary', LargeBinary),
        Column('Tag', SmallInteger)
)


class Users(Base):
    """
    Пользователи
    Используются для идентификации создателей и редакторов любых перечисленных объектов
    """
    __tablename__ = 'Users'

    Type = Column(SmallInteger, primary_key = True, nullable = False)
    Num = Column(Integer, Identity(start = 1, increment = 1), nullable = False, unique = True)
    ID = Column(Unicode(20), primary_key = True, nullable = False)
    IsSecreteUser = Column(SmallInteger, nullable = False, server_default = text('((0))'))
    IsRemoved = Column(SmallInteger, nullable = False, server_default = text('((0))'))
    Password = Column(Unicode(20))
    Text = Column(Unicode(100))
    Tag = Column(SmallInteger)
    UserRights = Column(SmallInteger)
    EditDate = Column(DateTime)
    EditUid = Column(Integer, ForeignKey('Users.Num'))
    ReviewDate = Column(DateTime)
    ReviewUid = Column(Integer, ForeignKey('Users.Num'))
    ApprovedDate = Column(DateTime)
    ApprovedUid = Column(Integer, ForeignKey('Users.Num'))
    flag = Column(Boolean)

    EditUser = relationship(lambda: Users, foreign_keys=[EditUid], remote_side=[Num])
    ReviewUser = relationship(lambda: Users, foreign_keys=[ReviewUid], remote_side=[Num])
    ApprovedUser= relationship(lambda: Users, foreign_keys=[ApprovedUid], remote_side=[Num])


class Sysdiagrams(Base):
    __tablename__ = 'sysdiagrams'
    __table_args__ = (
        Index('UK_principal_name', 'principal_id', 'name', unique = True),
    )

    name = Column(Unicode(128), nullable = False)
    principal_id = Column(Integer, nullable = False)
    diagram_id = Column(Integer, Identity(start = 1, increment = 1), primary_key = True)
    version = Column(Integer)
    definition = Column(LargeBinary)
