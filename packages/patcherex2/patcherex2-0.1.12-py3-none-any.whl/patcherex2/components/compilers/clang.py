import logging
from typing import List, Optional

from .compiler import Compiler

logger = logging.getLogger(__name__)


class Clang(Compiler):
    def __init__(
        self, p, clang_version=15, compiler_flags: Optional[List[str]] = None
    ) -> None:
        super().__init__(p)
        if compiler_flags is None:
            compiler_flags = []
        self._compiler = f"clang-{clang_version}"
        self._linker = f"ld.lld-{clang_version}"
        self._compiler_flags = compiler_flags
