from datetime import date
from re import fullmatch
from typing import ClassVar, Literal

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ...bases import Base, Data, Process
from ...custom_types import samplesheet_str, samplesheet_str_pk, stripped_str
from ..data import DataSet, Sample

__all__ = [
    'ChromiumDataSet',
    'ChromiumTag',
    'ChromiumSample',
    'SequencingRun',
    'ChromiumLibraryType',
    'ChromiumLibrary',
]


class ChromiumDataSet(DataSet, kw_only=True):
    # Child models
    samples: Mapped[list['ChromiumSample']] = relationship(
        back_populates='data_set', default_factory=list, repr=False
    )
    libraries: Mapped[list['ChromiumLibrary']] = relationship(
        back_populates='data_set', default_factory=list, repr=False
    )

    # Model metadata
    id_prefix: ClassVar[Literal['SD']] = 'SD'
    id_length: ClassVar[Literal[9]] = 9

    __mapper_args__ = {
        'polymorphic_identity': 'Chromium',
    }


class ChromiumTag(Base, kw_only=True):
    __tablename__ = 'chromium_tag'

    # TODO: add validation
    # Tag attributes
    id: Mapped[samplesheet_str_pk]
    name: Mapped[samplesheet_str | None]
    type: Mapped[stripped_str]
    read: Mapped[stripped_str]
    sequence: Mapped[stripped_str]
    pattern: Mapped[stripped_str]
    five_prime_offset: Mapped[int]


class ChromiumSample(Sample, kw_only=True):
    # Sample attributes
    targeted_cell_recovery: Mapped[int | None] = mapped_column(default=None)

    # Parent foreign keys
    tag_id: Mapped[str | None] = mapped_column(
        ForeignKey('chromium_tag.id'), default=None, repr=False, init=False
    )

    # Parent models
    data_set: Mapped[ChromiumDataSet] = relationship(
        back_populates='samples', default=None, repr=False
    )
    tag: Mapped[ChromiumTag | None] = relationship(default=None, repr=False)

    # Model metadata
    id_prefix: ClassVar[Literal['SS']] = 'SS'
    id_length: ClassVar[Literal[9]] = 9

    __mapper_args__ = {'polymorphic_identity': 'Chromium'}


class SequencingRun(Data, kw_only=True):
    __tablename__ = 'sequencing_run'

    libraries: Mapped[list['ChromiumLibrary']] = relationship(
        back_populates='sequencing_run', default_factory=list, repr=False
    )

    def __post_init__(self):
        self.id = self.id.strip().lower()

        pattern = rf'\d{{2}}-scbct-\d{{2,3}}'

        model_name = type(self).__name__
        if fullmatch(pattern, self.id) is None:
            raise ValueError(
                f'{model_name} ID {self.id} does not match the pattern {pattern}.'
            )


class ChromiumLibraryType(Process, kw_only=True):
    __tablename__ = 'chromium_library_type'


class ChromiumLibrary(Data, kw_only=True):
    __tablename__ = 'chromium_library'

    # Library attributes
    date_constructed: Mapped[date | None] = mapped_column(default=None, repr=False)

    # TODO: add some validation so that libraries with a particular
    # status must have a sequencing run
    status: Mapped[stripped_str]

    # Parent foreign keys
    data_set_id: Mapped[str] = mapped_column(
        ForeignKey('data_set.id'), default=None, init=False, repr=False
    )
    library_type_name: Mapped[int] = mapped_column(
        ForeignKey('chromium_library_type.name'), default=None, init=False, repr=False
    )
    sequencing_run_id: Mapped[str | None] = mapped_column(
        ForeignKey('sequencing_run.id'),
        default=None,
        compare=False,
        init=False,
        repr=False,
    )

    # Parent models
    data_set: Mapped[ChromiumDataSet] = relationship(
        back_populates='libraries', default=None, repr=False
    )
    library_type: Mapped[ChromiumLibraryType] = relationship(default=None, repr=False)
    sequencing_run: Mapped[SequencingRun | None] = relationship(
        default=None, compare=False, repr=False
    )

    # Model metadata
    id_date_col: ClassVar[Literal['date_constructed']] = 'date_constructed'
    id_prefix: ClassVar[Literal['SC']] = 'SC'
    id_length: ClassVar[Literal[9]] = 9
