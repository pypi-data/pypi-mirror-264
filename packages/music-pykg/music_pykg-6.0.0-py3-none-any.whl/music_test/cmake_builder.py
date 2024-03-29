from __future__ import annotations

import shutil
import subprocess
import typing
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path

from .term import BlackHole, TermBase, err_msg, info_msg, warn_msg

if typing.TYPE_CHECKING:
    from typing import Iterable, Optional, Sequence

    from .dirs import BuildsDirectory, TestsOutputDirectory

CMAKE_CACHE = "CMakeCache.txt"


class NoCacheFoundError(Exception):
    """Raised when automatic lookup of an existing cache failed."""

    pass


@dataclass(frozen=True)
class Target:
    name: str
    with_idx64: bool = False

    @property
    def idx_tag(self) -> str:
        return "idx64" if self.with_idx64 else "idx32"


def _curated_cache_copy(old: Path, new: Path) -> None:
    """Copy cache, removing undesired lines.

    The removed line is the one keeping track of the directory in which the
    cache was created.  This is fine to remove only this line and keep a lot of
    "INTERNAL" that shouldn't be copied in general since we are building the
    same code base and we aim at reproducing the build as closely as possible.
    """
    with old.open() as old_cache, new.open("w") as new_cache:
        for line in old_cache:
            if not line.startswith("CMAKE_CACHEFILE_DIR:INTERNAL"):
                new_cache.writelines([line])


@dataclass(frozen=True)
class BuildOutcome:
    """Result from calling CmakeBuilder.build_targets."""

    built_targets: frozenset[Target]
    all_successful: bool


@dataclass(frozen=True)
class CmakeBuilder:
    """Build binaries for tests using CMake.

    music_dir: the root of the music repository.
    cache_dir: an already existing build-tree whose CMake cache should be
        reused if necessary.
    """

    music_dir: Path
    outdir: TestsOutputDirectory
    requested_cache: Optional[Path] = None

    @cached_property
    def _found_cache(self) -> Path:
        """Cache directory location."""
        if self.requested_cache is not None:
            return self.requested_cache
        build_dirs = ("build-debug", "bld-debug", "build", "bld")
        for build_dir in build_dirs:
            cache_dir = self.music_dir / build_dir
            if (cache_dir / CMAKE_CACHE).is_file():
                return cache_dir
        for cache_file in self.music_dir.glob(f"*/{CMAKE_CACHE}"):
            return cache_file.parent
        raise NoCacheFoundError

    @property
    def builds_dir(self) -> BuildsDirectory:
        return self.outdir.builds_directory

    def target_tags(self, target: Target) -> Sequence[str]:
        """Tags related to build options."""
        return (target.name, target.idx_tag)

    def _configure_idx(
        self, with_idx64: bool, *, output_to: TermBase, indent: int
    ) -> bool:
        idx_flag = "ON" if with_idx64 else "OFF"
        build_dir = self.builds_dir.idx_path(with_idx64)
        config_log = self.builds_dir.path / f"config_{build_dir.name}.log"
        with config_log.open("w") as clog:
            config_process = subprocess.run(
                [
                    "cmake",
                    "-S",
                    self.music_dir,
                    "-B",
                    build_dir,
                    "-D",
                    f"MUSIC_USE_64BIT_GLOBAL_ORDINALS={idx_flag}",
                ],
                stdout=clog,
                stderr=clog,
            )
        if config_process.returncode == 0:
            return True
        else:
            err_msg(
                "Configuration failed",
                f"See log in {config_log}",
            ).print_to(output_to, indent)
            return False

    def build_targets(
        self,
        targets: Iterable[Target],
        *,
        output_to: Optional[TermBase] = None,
        indent: int = 0,
    ) -> BuildOutcome:
        """Build test targets."""
        output_to = output_to if output_to is not None else BlackHole()

        cache = self.builds_dir.path / "cache.cmake"
        if cache.is_file() and self.requested_cache is not None:
            warn_msg(
                "Explicit cache location requested with `-c|--cache-from` is",
                "ignored as a cache already exists and `--keep` was passed",
            ).print_to(output_to, indent)
        if not cache.is_file():
            if self.requested_cache is None:
                warn_msg(
                    f"Found cache in existing build-tree {self._found_cache}",
                    "Use `-c|--cache-from <path>` to request a specific tree",
                ).print_to(output_to, indent)
            else:
                info_msg(
                    f"Using cache in existing build-tree {self._found_cache}"
                ).print_to(output_to, indent)
            _curated_cache_copy(self._found_cache / CMAKE_CACHE, cache)

        tgts_by_idx: dict[bool, set[Target]] = {}
        for target in targets:
            tgts_by_idx.setdefault(target.with_idx64, set()).add(target)

        nconfigs = len(tgts_by_idx)
        build_success = True
        built_targets: list[Target] = []
        for i, (with_idx64, targets) in enumerate(tgts_by_idx.items(), 1):
            target_names = {target.name for target in targets}
            config_name = "idx64" if with_idx64 else "idx32"
            info_msg(
                f"Building config {i}/{nconfigs}: {config_name} {target_names!r}"
            ).print_to(output_to, indent)
            build_dir = self.builds_dir.idx_path(with_idx64)
            build_dir.mkdir(exist_ok=True)
            build_cache = build_dir / CMAKE_CACHE
            if not build_cache.is_file():
                shutil.copy(cache, build_cache)
            config_success = self._configure_idx(
                with_idx64, output_to=output_to, indent=indent + 1
            )
            if not config_success:
                build_success = False
                continue
            for tgt in targets:
                info_msg(f"Target {tgt.name}").print_to(output_to, indent + 1)
                build_log = build_dir / f"build_{tgt.name}.log"
                with build_log.open("w") as blog:
                    bld_process = subprocess.run(
                        [
                            "cmake",
                            "--build",
                            build_dir,
                            "--target",
                            tgt.name,
                            "--parallel",
                        ],
                        stdout=blog,
                        stderr=blog,
                    )
                if bld_process.returncode == 0:
                    built_targets.append(tgt)
                else:
                    build_success = False
                    err_msg(
                        f"Build of target `{tgt.name}` failed",
                        f"See log in {build_log}",
                    ).print_to(output_to, indent + 1)
        return BuildOutcome(frozenset(built_targets), build_success)
