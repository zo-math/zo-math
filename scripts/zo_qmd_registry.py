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
    """Resolve safe adapters from the project's declared modules."""

    declared = _unique((*config.required_modules, *config.optional_modules))
    unknown = sorted(set(declared) - REGISTERED_MODULES)
    if unknown:
        raise ModuleRegistryError(
            "Mô-đun chưa đăng kí: " + ", ".join(unknown) + "."
        )

    active_modules = _unique(config.required_modules)
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

    return ValidationPlan(
        article_type=article_type,
        active_modules=active_modules,
        source_adapters=source_adapters,
        render_adapters=render_adapters,
        requires_human_acceptance=requires_human_acceptance,
        compatibility_mode="native",
    )



def _self_test() -> None:
    class FunctionConfig:
        required_modules = (
            "qmd-core",
            "zo-html-pdf",
            "content-blocks",
            "functions-article",
        )
        optional_modules = ("figure-layout", "card-grid")

    function_plan = build_validation_plan(FunctionConfig(), "function_article")
    assert function_plan.active_modules == FunctionConfig.required_modules
    assert function_plan.source_adapters == ("functions-article",)
    assert function_plan.render_adapters == ("functions-article",)
    assert function_plan.requires_human_acceptance is True
    assert function_plan.compatibility_mode == "native"

    class RealWorldConfig:
        required_modules = (
            "qmd-core",
            "zo-html-pdf",
            "content-blocks",
            "real-world-problem",
        )
        optional_modules = ("figure-layout",)

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
