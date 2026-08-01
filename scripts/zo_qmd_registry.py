"""Static module registry and validation planning for configured QMD projects.

The YAML configuration may name only module IDs registered here. It never
contains Python import paths or callable names. The checker resolves symbolic
adapter IDs from the plan through its own fixed adapter tables.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Protocol, Sequence


EXIT_OK = 0
EXIT_INVALID = 1


class ModuleRegistryError(ValueError):
    """Raised when configured modules cannot form a valid validation plan."""


class ProjectModuleConfig(Protocol):
    """Minimal project-configuration interface consumed by the registry."""

    required_modules: tuple[str, ...]
    optional_modules: tuple[str, ...]
    compatibility_mode: str
    legacy_validator: str | None


@dataclass(frozen=True)
class ModuleSpec:
    """One safe, statically registered QMD production module."""

    id: str
    article_types: tuple[str, ...] = ()
    source_adapter: str | None = None
    render_adapter: str | None = None
    requires_human_acceptance: bool = False

    def applies_to(self, article_type: str) -> bool:
        return not self.article_types or article_type in self.article_types


@dataclass(frozen=True)
class ValidationPlan:
    """Resolved module and adapter plan for one configured article."""

    article_type: str
    active_modules: tuple[str, ...]
    source_adapters: tuple[str, ...]
    render_adapters: tuple[str, ...]
    requires_human_acceptance: bool
    compatibility_mode: str


MODULE_SPECS: tuple[ModuleSpec, ...] = (
    ModuleSpec("qmd-core"),
    ModuleSpec("zo-html-pdf"),
    ModuleSpec("content-blocks"),
    ModuleSpec("figure-layout"),
    ModuleSpec("card-grid"),
    ModuleSpec(
        "functions-article",
        article_types=("function_article",),
        source_adapter="functions-article",
        render_adapter="functions-article",
        requires_human_acceptance=True,
    ),
    ModuleSpec(
        "real-world-problem",
        article_types=("real_world_problem",),
        source_adapter="real-world-problem",
        render_adapter="real-world-problem",
        requires_human_acceptance=True,
    ),
)

MODULE_REGISTRY = {spec.id: spec for spec in MODULE_SPECS}
REGISTERED_MODULES = frozenset(MODULE_REGISTRY)


def _unique(values: Sequence[str]) -> tuple[str, ...]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return tuple(result)


def module_spec(module_id: str) -> ModuleSpec:
    """Return a registered module or fail with a stable error."""

    try:
        return MODULE_REGISTRY[module_id]
    except KeyError as exc:
        raise ModuleRegistryError(f"Mô-đun chưa đăng kí: {module_id!r}.") from exc


def build_validation_plan(
    config: ProjectModuleConfig, article_type: str
) -> ValidationPlan:
    """Resolve safe adapters from project modules and compatibility settings."""

    declared = _unique((*config.required_modules, *config.optional_modules))
    unknown = sorted(set(declared) - REGISTERED_MODULES)
    if unknown:
        raise ModuleRegistryError(
            "Mô-đun chưa đăng kí: " + ", ".join(unknown) + "."
        )

    if config.compatibility_mode not in {"legacy", "native"}:
        raise ModuleRegistryError(
            f"Chế độ tương thích không hỗ trợ: {config.compatibility_mode!r}."
        )

    active = list(config.required_modules)
    if config.compatibility_mode == "legacy":
        legacy = config.legacy_validator
        if not legacy:
            raise ModuleRegistryError(
                "Chế độ legacy phải khai báo compatibility.legacy_validator."
            )
        if legacy not in declared:
            raise ModuleRegistryError(
                "Legacy validator phải xuất hiện trong modules.required hoặc modules.optional."
            )
        if legacy not in active:
            active.append(legacy)

    active_modules = _unique(active)
    applicable = [
        module_spec(module_id)
        for module_id in active_modules
        if module_spec(module_id).applies_to(article_type)
    ]
    source_adapters = _unique(
        tuple(
            spec.source_adapter
            for spec in applicable
            if spec.source_adapter is not None
        )
    )
    render_adapters = _unique(
        tuple(
            spec.render_adapter
            for spec in applicable
            if spec.render_adapter is not None
        )
    )
    requires_human_acceptance = any(
        spec.requires_human_acceptance for spec in applicable
    )

    if config.compatibility_mode == "legacy":
        legacy_spec = module_spec(config.legacy_validator or "")
        if not legacy_spec.applies_to(article_type):
            raise ModuleRegistryError(
                f"Legacy validator {legacy_spec.id!r} không áp dụng cho "
                f"article_type={article_type!r}."
            )
        if legacy_spec.source_adapter is None:
            raise ModuleRegistryError(
                f"Legacy validator {legacy_spec.id!r} không có source adapter."
            )

    return ValidationPlan(
        article_type=article_type,
        active_modules=active_modules,
        source_adapters=source_adapters,
        render_adapters=render_adapters,
        requires_human_acceptance=requires_human_acceptance,
        compatibility_mode=config.compatibility_mode,
    )


def legacy_validation_plan(
    article_type: str, legacy_validator: str
) -> ValidationPlan:
    """Build the temporary fallback plan used when legacy paths lack config."""

    spec = module_spec(legacy_validator)
    if not spec.applies_to(article_type):
        raise ModuleRegistryError(
            f"Legacy validator {legacy_validator!r} không áp dụng cho "
            f"article_type={article_type!r}."
        )
    if spec.source_adapter is None:
        raise ModuleRegistryError(
            f"Legacy validator {legacy_validator!r} không có source adapter."
        )
    return ValidationPlan(
        article_type=article_type,
        active_modules=(legacy_validator,),
        source_adapters=(spec.source_adapter,),
        render_adapters=(spec.render_adapter,) if spec.render_adapter else (),
        requires_human_acceptance=spec.requires_human_acceptance,
        compatibility_mode="legacy-fallback",
    )


def _self_test() -> None:
    class DemoConfig:
        required_modules = (
            "qmd-core",
            "zo-html-pdf",
            "content-blocks",
            "functions-article",
        )
        optional_modules = ("figure-layout", "card-grid")
        compatibility_mode = "legacy"
        legacy_validator = "functions-article"

    plan = build_validation_plan(DemoConfig(), "function_article")
    assert plan.active_modules == DemoConfig.required_modules
    assert plan.source_adapters == ("functions-article",)
    assert plan.render_adapters == ("functions-article",)
    assert plan.requires_human_acceptance is True

    fallback = legacy_validation_plan("function_article", "functions-article")
    assert fallback.compatibility_mode == "legacy-fallback"
    assert fallback.source_adapters == ("functions-article",)

    class RealWorldConfig:
        required_modules = (
            "qmd-core",
            "zo-html-pdf",
            "content-blocks",
            "real-world-problem",
        )
        optional_modules = ("figure-layout",)
        compatibility_mode = "native"
        legacy_validator = None

    real_world = build_validation_plan(RealWorldConfig(), "real_world_problem")
    assert real_world.compatibility_mode == "native"
    assert real_world.source_adapters == ("real-world-problem",)
    assert real_world.render_adapters == ("real-world-problem",)
    assert real_world.requires_human_acceptance is True

    try:
        module_spec("unknown")
    except ModuleRegistryError:
        pass
    else:
        raise AssertionError("Mô-đun chưa đăng kí phải bị từ chối.")


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("command", choices=("self-test", "list"))
    return result


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "self-test":
            _self_test()
            print("PASS: zo_qmd_registry self-test")
        else:
            for spec in MODULE_SPECS:
                print(spec.id)
        return EXIT_OK
    except (AssertionError, ModuleRegistryError) as exc:
        print(f"ERROR: {exc}")
        return EXIT_INVALID


if __name__ == "__main__":
    raise SystemExit(main())
