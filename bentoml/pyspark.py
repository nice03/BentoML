import typing as t
from typing import TYPE_CHECKING

from simple_di import inject
from simple_di import Provide

from .exceptions import MissingDependencyException
from ._internal.types import Tag
from ._internal.runner import Runner
from ._internal.configuration.containers import BentoMLContainer

if TYPE_CHECKING:
    from _internal.models import ModelStore

try:
    ...
except ImportError:  # pragma: no cover
    raise MissingDependencyException("")


@inject
def load(
    tag: str,
    model_store: "ModelStore" = Provide[BentoMLContainer.model_store],
):
    """
    Load a model from BentoML local modelstore with given name.

    Args:
        tag (`str`):
            Tag of a saved model in BentoML local modelstore.
        model_store (`~bentoml._internal.models.ModelStore`, default to `BentoMLContainer.model_store`):
            BentoML modelstore, provided by DI Container.

    Returns:
        an instance of `xgboost.core.Booster` from BentoML modelstore.

    Examples::
    """  # noqa


@inject
def save(
    name: str,
    model: t.Any,
    *,
    metadata: t.Union[None, t.Dict[str, t.Any]] = None,
    model_store: "ModelStore" = Provide[BentoMLContainer.model_store],
) -> str:
    """
    Save a model instance to BentoML modelstore.

    Args:
        name (`str`):
            Name for given model instance. This should pass Python identifier check.
        model (`xgboost.core.Booster`):
            Instance of model to be saved
        metadata (`t.Optional[t.Dict[str, t.Any]]`, default to `None`):
            Custom metadata for given model.
        model_store (`~bentoml._internal.models.ModelStore`, default to `BentoMLContainer.model_store`):
            BentoML modelstore, provided by DI Container.

    Returns:
        tag (`str` with a format `name:version`) where `name` is the defined name user
        set for their models, and version will be generated by BentoML.

    Examples::
    """  # noqa


class _PySparkMLlibRunner(Runner):
    @inject
    def __init__(
        self,
        tag: Tag,
        resource_quota: t.Dict[str, t.Any],
        batch_options: t.Dict[str, t.Any],
        model_store: "ModelStore" = Provide[BentoMLContainer.model_store],
    ):
        super().__init__(str(tag), resource_quota, batch_options)

    @property
    def required_models(self) -> t.List[Tag]:
        ...

    @property
    def num_concurrency_per_replica(self) -> int:
        ...

    @property
    def num_replica(self) -> int:
        ...

    # pylint: disable=arguments-differ,attribute-defined-outside-init
    def _setup(self) -> None:
        ...

    # pylint: disable=arguments-differ,attribute-defined-outside-init
    def _run_batch(self, input_data) -> t.Any:
        ...


@inject
def load_runner(
    tag: t.Union[str, Tag],
    *,
    resource_quota: t.Union[None, t.Dict[str, t.Any]] = None,
    batch_options: t.Union[None, t.Dict[str, t.Any]] = None,
    model_store: "ModelStore" = Provide[BentoMLContainer.model_store],
) -> "_PySparkMLlibRunner":
    """
    Runner represents a unit of serving logic that can be scaled horizontally to
    maximize throughput. `bentoml.xgboost.load_runner` implements a Runner class that
    wrap around a Xgboost booster model, which optimize it for the BentoML runtime.

    Args:
        tag (`str`):
            Model tag to retrieve model from modelstore
        resource_quota (`t.Dict[str, t.Any]`, default to `None`):
            Dictionary to configure resources allocation for runner.
        batch_options (`t.Dict[str, t.Any]`, default to `None`):
            Dictionary to configure batch options for runner in a service context.
        model_store (`~bentoml._internal.models.ModelStore`, default to `BentoMLContainer.model_store`):
            BentoML modelstore, provided by DI Container.

    Returns:
        Runner instances for `bentoml.pyspark` model

    Examples::
    """  # noqa
    return _PySparkMLlibRunner(
        tag=tag,
        resource_quota=resource_quota,
        batch_options=batch_options,
        model_store=model_store,
    )


# import importlib
# import json
# import logging
# import os
# import typing as t
#
# import bentoml._internal.constants as _const
#
# from ._internal.models.base import MODEL_NAMESPACE, Model
# from ._internal.types import GenericDictType, PathType
# from ._internal.utils import LazyLoader
# from .exceptions import BentoMLException
#
# logger = logging.getLogger(__name__)
#
# _exc = _const.IMPORT_ERROR_MSG.format(
#     fwr="pyspark.mllib",
#     module=__name__,
#     inst="First install Apache Spark, https://spark.apache.org/downloads.html."
#     " Then run `pip install pyspark`",
# )
#
# if t.TYPE_CHECKING:  # pragma: no cover
#     # pylint: disable=unused-import
#     import pyspark
#     import pyspark.ml as ml
#     import pyspark.sql as sql
# else:
#     pyspark = LazyLoader("pyspark", globals(), "pyspark", exc_msg=_exc)
#     ml = LazyLoader("ml", globals(), "pyspark.ml", exc_msg=_exc)
#     sql = LazyLoader("sql", globals(), "pyspark.sql", exc_msg=_exc)
#
# # NOTE: the usage of SPARK_SESSION_NAMESPACE is to provide a consistent session
# #  among imports if users need to use SparkSession.
# SPARK_SESSION_NAMESPACE: str = "PySparkMLlibModel"
#
# DEPRECATION_MLLIB_WARNING: str = """
# {model} is using the older library `pyspark.mllib`.
# Consider to upgrade your model to use `pyspark.ml`.
# BentoML will still try to load {model} with `pyspark.sql.SparkSession`,
# but expect unintended behaviour.
# """
#
#
# class PySparkMLlibModel(Model):
#     """
#     Model class for saving/loading :obj:`pyspark` models
#     using :obj:`pyspark.ml` and :obj:`pyspark.mllib`
#
#     Args:
#         model (`pyspark.ml.Model`):
#             Every PySpark model is of type :obj:`pyspark.ml.Model`
#         spark_session (`pyspark.sql.SparkSession`, `optional`, default to `None`):
#             Optional SparkSession used to load PySpark model representation.
#         metadata (`GenericDictType`,  `optional`, default to `None`):
#             Class metadata
#
#     Raises:
#         MissingDependencyException:
#             :obj:`pyspark` is required by PySparkMLlibModel
#
#     .. WARNING::
#
#         :obj:`spark_session` should only be used when your current model is running
#         older version of `pyspark.ml` (`pyspark.mllib`). Consider to upgrade your mode
#         beforehand to use `pyspark.ml`.
#
#     Example usage under :code:`train.py`::
#
#         TODO:
#
#     One then can define :code:`bento.py`::
#
#         TODO:
#     """
#
#     _model: "pyspark.ml.Model"
#
#     def __init__(
#         self,
#         model: "pyspark.ml.Model",
#         spark_session: t.Optional["pyspark.sql.SparkSession"] = None,
#         metadata: t.Optional[GenericDictType] = None,
#     ):
#         super(PySparkMLlibModel, self).__init__(model, metadata=metadata)
#         # NOTES: referred to docstring, spark_session is mainly used
#         #  for backward compatibility.
#         self._spark_sess = spark_session
#
#     @classmethod
#     def load(cls, path: PathType) -> "pyspark.ml.Model":
#
#         model_path: str = str(os.path.join(path, MODEL_NAMESPACE))
#
#         # NOTE (future ref): A large model metadata might
#         #  comprise of multiple `part` files, instead of assigning,
#         #  loop through the directory.
#         metadata_path: str = str(os.path.join(model_path, "metadata/part-00000"))
#
#         try:
#             with open(metadata_path, "r") as meta_file:
#                 metadata = json.load(meta_file)
#         except IOError:
#             raise BentoMLException(
#                 "Incorrectly serialized model was loaded. Unable to load metadata"
#             )
#         if "class" not in metadata:
#             raise BentoMLException("malformed metadata file.")
#         model_class = metadata["class"]
#
#         # process imports from metadata
#         stripped_apache_module: t.List[str] = model_class.split(".")[2:]
#         py_module = "py" + ".".join(stripped_apache_module[:-1])  # skip org.apache
#         class_name = stripped_apache_module[-1]
#
#         loaded_model = getattr(importlib.import_module(py_module), class_name)
#         if not issubclass(loaded_model, ml.Model):
#             logger.warning(DEPRECATION_MLLIB_WARNING.format(model=loaded_model))
#             _spark_sess = sql.SparkSession.builder.appName(
#                 SPARK_SESSION_NAMESPACE
#             ).getOrCreate()
#             model = loaded_model.load(_spark_sess.sparkContext, model_path)
#         else:
#             model = loaded_model.load(model_path)
#
#         return model
#
#     def save(self, path: PathType) -> None:
#         if not isinstance(self._model, ml.Model):
#             logger.warning(DEPRECATION_MLLIB_WARNING.format(model=self._model))
#             self._model.save(self._spark_sess, os.path.join(path, MODEL_NAMESPACE))
#         else:
#             self._model.save(os.path.join(path, MODEL_NAMESPACE))
