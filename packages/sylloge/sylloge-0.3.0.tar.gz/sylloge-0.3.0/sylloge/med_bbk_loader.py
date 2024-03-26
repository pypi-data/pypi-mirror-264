import pathlib
from typing import Any, Dict, Literal, Optional, Union, overload

import dask.dataframe as dd
import pandas as pd

from .base import (
    BACKEND_LITERAL,
    BASE_DATASET_MODULE,
    BinaryZipEADataset,
    DataFrameType,
)

MED_BBK_MODULE = BASE_DATASET_MODULE.module("med_bbk")


class MED_BBK(BinaryZipEADataset[DataFrameType]):
    """Class containing the MED-BBK dataset.

    Published in `Zhang, Z. et. al. (2020) An Industry Evaluation of Embedding-based Entity Alignment <A Benchmarking Study of Embedding-based Entity Alignment for Knowledge Graphs>`_,
    *COLING*
    """

    #: The link to the zip file
    _ZIP_LINK: str = (
        "https://github.com/ZihengZZH/industry-eval-EA/raw/main/benchmark/industry.zip"
    )

    #: The hex digest for the zip file
    _SHA512: str = "da1ee2b025070fd6890fb7e77b07214af3767b5ae85bcdc1bb36958b4b8dd935bc636e3466b94169158940a960541f96284e3217d32976bfeefa56e29d4a9e0d"

    @overload
    def __init__(
        self: "MED_BBK[pd.DataFrame]",
        backend: Literal["pandas"] = "pandas",
        use_cache: bool = True,
        cache_path: Optional[Union[str, pathlib.Path]] = None,
    ):
        ...

    @overload
    def __init__(
        self: "MED_BBK[dd.DataFrame]",
        backend: Literal["dask"] = "dask",
        use_cache: bool = True,
        cache_path: Optional[Union[str, pathlib.Path]] = None,
    ):
        ...

    def __init__(
        self,
        backend: BACKEND_LITERAL = "pandas",
        use_cache: bool = True,
        cache_path: Optional[Union[str, pathlib.Path]] = None,
    ):
        """Initialize an MED-BBK dataset.

        :param backend: Whether to use "pandas" or "dask"
        :param use_cache: whether to use cache or not
        :param cache_path: Path where cache will be stored/loaded
        """
        # ensure zip file is present
        zip_path = MED_BBK_MODULE.ensure(
            url=MED_BBK._ZIP_LINK,
            download_kwargs=dict(hexdigests=dict(sha512=MED_BBK._SHA512)),  # noqa: C408
        )

        inner_path = "industry"
        actual_cache_path = self.create_cache_path(
            MED_BBK_MODULE, inner_path, cache_path
        )
        super().__init__(  # type: ignore[misc]
            cache_path=actual_cache_path,
            use_cache=use_cache,
            zip_path=zip_path,
            inner_path=pathlib.PurePosixPath(inner_path),
            backend=backend,  # type: ignore[arg-type]
            dataset_names=("MED", "BBK"),
        )

    def initial_read(self, backend: BACKEND_LITERAL) -> Dict[str, Any]:
        # MED is KG2 and BBK is KG1
        inital_dict = super().initial_read(backend=backend)
        return {
            "rel_triples": inital_dict["rel_triples"][::-1],
            "attr_triples": inital_dict["attr_triples"][::-1],
            "ent_links": inital_dict["ent_links"],
        }

    @property
    def _canonical_name(self) -> str:
        return f"{self.__class__.__name__}"

    @property
    def _param_repr(self) -> str:
        return ""
