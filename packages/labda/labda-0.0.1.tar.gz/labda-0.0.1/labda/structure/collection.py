import multiprocessing as mp
import secrets
from functools import partial
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field

from .subject import Subject


def _process_subject(subject, func, **kwargs):
    func(subject, **kwargs)

    return subject


class Collection(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: secrets.token_hex(4))
    subjects: list[Subject] = Field(default_factory=list)

    def __repr__(self):
        subjects_repr = ", ".join([p.metadata.id for p in self.subjects])  # type: ignore
        return f"Collection(id={self.id}, subjects=[{subjects_repr}])"

    def add_subject(self, subject: Subject):
        subjects_ids = [s.metadata.id for s in self.subjects]

        if subject.metadata.id in subjects_ids:
            raise ValueError(
                f"Subject with id '{subject.metadata.id}' already exists in collection."
            )

        subject.collection = self.id  # type: ignore
        self.subjects.append(subject)  # type: ignore

    def get_subject(self, id: str) -> Subject:
        for subject in self.subjects:
            if subject.metadata.id == id:
                return subject
        raise ValueError(f"Subject with id '{id}' not found.")

    @classmethod
    def from_folder(cls, path: str | Path, id: str | None = None) -> "Collection":
        if isinstance(path, str):
            path = Path(path)

        subjects = [Subject.from_parquet(file) for file in path.glob("*.parquet")]
        return cls(id=id, subjects=subjects)

    def to_folder(self, path: str | Path, overwrite: bool = False):
        if isinstance(path, str):
            path = Path(path)

        path.mkdir(parents=True, exist_ok=True)
        for subject in self.subjects:
            subject.to_parquet(
                path / f"{subject.metadata.id}.parquet", overwrite=overwrite
            )

    def detect_trips(self, **kwargs):
        with mp.Pool(mp.cpu_count()) as pool:
            self.subjects = pool.map(
                partial(_process_subject, func=Subject.detect_trips, **kwargs),
                self.subjects,
            )

    def detect_activity_intensity(self, **kwargs) -> None:
        with mp.Pool(mp.cpu_count()) as pool:
            self.subjects = pool.map(
                partial(
                    _process_subject, func=Subject.detect_activity_intensity, **kwargs
                ),
                self.subjects,
            )

    # TODO: Rework whole consistency check
    # TODO: Add also check columns consistency
    def _check_consistency(self, attribute, error_message):
        # TODO: Add docstring, better name for method
        values = [getattr(subject.metadata, attribute) for subject in self.subjects]
        unique = set(values)

        if len(unique) != 1:
            print(f"{error_message}: {unique}")

    def _check_consistent_sampling_frequencies(self):
        self._check_consistency(
            "sampling_frequency", "Sampling frequencies are not consistent"
        )

    def _check_consistent_crs(self):
        self._check_consistency("crs", "CRS are not consistent")

    def _check_consistent_timezones(self):
        self._check_consistency("timezone", "Timezones are not consistent")

    def check_consistency(self):
        self._check_consistent_sampling_frequencies()
        self._check_consistent_crs()
        self._check_consistent_timezones()

        print("Consistency check finished.")
