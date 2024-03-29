from numbers import Number
from typing import Any, Literal, Optional

import numpy as np
from pydantic import StrictStr, validator

from .config_utils import BaseConfig


class SPSAConfig(BaseConfig):
    learning_rate: float = 5
    learning_rate_exponent: float = 0.6
    perturbation: float = 1e-2
    perturbation_exponent: float = 0.1
    eps: float = 1e-14
    max_iter: int = 100
    params_tol: float = 1e-8
    fun_tol: float = 1e-7


class SerializedObservableConfig(BaseConfig):
    paulis: dict[str, Literal["X", "Y", "Z"]]
    coeff: Any  # (int | float | complex)

    @validator("coeff")
    def validate_coeff(cls, coeff):
        if not isinstance(coeff, Number):
            raise ValueError("Pauli operator coefficient should be a number")
        return coeff


class ObservableConfig(BaseConfig):
    name: StrictStr
    serialized_observables: list[SerializedObservableConfig]


class OptimizerConfig(BaseConfig):
    enabled: bool = False
    observable: Optional[ObservableConfig] = None
    optimizer: Literal["spsa"] = "spsa"
    evaluation_mode: Literal["contract"] = "contract"
    optimizer_name: Literal["spsa"] = "spsa"
    optimizer_settings: SPSAConfig = SPSAConfig()
    initial_param_values: dict[str, float] = {}
    initial_param_noise: float = 0.1

    @validator("observable", always=True, pre=True)
    def validate_observable(cls, observable, values):
        if values["enabled"] and observable is None:
            raise ValueError("If optimizer is enabled, an observable must be specified")

        if not values["enabled"]:
            return None
        return observable

    @validator("initial_param_noise")
    def validate_initial_param_noise(cls, initial_param_noise, values):
        if initial_param_noise < 0:
            raise ValueError("initial_param_noise must be non-negative")

        if not values["initial_param_values"] and np.isclose(initial_param_noise, 0):
            raise ValueError(
                "The parameter initial_param_noise is zero, and no initial parameter values are given in "
                "initial_param_values. This means that all parameters will start at exactly zero, "
                "which can often create problems in the optimization. Please provide initial values"
                " or let initial_param_noise be non-zero."
            )

        return initial_param_noise
