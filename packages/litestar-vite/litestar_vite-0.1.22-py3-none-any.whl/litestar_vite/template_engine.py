from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

import markupsafe
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.template.base import TemplateEngineProtocol

from litestar_vite.loader import ViteAssetLoader

if TYPE_CHECKING:
    from pathlib import Path

    from jinja2 import Environment

    from litestar_vite.config import ViteConfig

T = TypeVar("T", bound=TemplateEngineProtocol)


class ViteTemplateEngine(JinjaTemplateEngine):
    """Jinja Template Engine with Vite Integration."""

    def __init__(
        self,
        directory: Path | list[Path] | None = None,
        engine_instance: Environment | None = None,
        config: ViteConfig | None = None,
    ) -> None:
        """Jinja2 based TemplateEngine.

        Args:
            directory: Direct path or list of directory paths from which to serve templates.
            engine_instance: A jinja Environment instance.
            config: Vite config
        """
        super().__init__(directory=directory, engine_instance=engine_instance)
        if config is None:
            msg = "Please configure the `ViteConfig` instance."
            raise ValueError(msg)
        self.config = config

        self.asset_loader = ViteAssetLoader.initialize_loader(config=self.config)
        self.engine.globals.update({"vite_hmr": self.get_hmr_client, "vite": self.get_asset_tag})

    def get_hmr_client(self) -> markupsafe.Markup:
        """Generate the script tag for the Vite WS client for HMR.

        Only used when hot module reloading is enabled, in production this method returns an empty string.

        Arguments:
            context: The template context.

        Returns:
            str: The script tag or an empty string.
        """
        return markupsafe.Markup(
            f"{self.asset_loader.generate_react_hmr_tags()}{self.asset_loader.generate_ws_client_tags()}",
        )

    def get_asset_tag(
        self,
        path: str | list[str],
        scripts_attrs: dict[str, str] | None = None,
    ) -> markupsafe.Markup:
        """Generate all assets include tags for the file in argument.

        Generates all scripts tags for this file and all its dependencies
        (JS and CSS) by reading the manifest file (for production only).
        In development Vite imports all dependencies by itself.
        Place this tag in <head> section of your page
        (this function marks automatically <script> as "async" and "defer").

        Arguments:
            context: The template context.
            path: Path to a Vite asset to include.
            scripts_attrs: script attributes

        Keyword Arguments:
            scripts_attrs {Optional[Dict[str, str]]}: Override attributes added to scripts tags. (default: {None})

        Returns:
            str: All tags to import this asset in your HTML page.
        """
        return markupsafe.Markup(self.asset_loader.generate_asset_tags(path, scripts_attrs=scripts_attrs))
