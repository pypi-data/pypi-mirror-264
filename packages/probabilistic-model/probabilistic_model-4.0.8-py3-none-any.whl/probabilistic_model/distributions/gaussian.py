import math
import random
from typing import Tuple, List, Optional, Dict, Any

import numpy as np
import portion
from random_events.events import Event, EncodedEvent, VariableMap, ComplexEvent
from random_events.variables import Continuous
from scipy.stats import gamma, norm
from typing_extensions import Self

from .distributions import ContinuousDistribution
from ..probabilistic_model import OrderType, CenterType, MomentType
from .exponential import ExponentialDistribution


class GaussianDistribution(ContinuousDistribution):
    """
    Class for Gaussian distributions.
    """

    mean: float
    """
    The mean of the Gaussian distribution.
    """

    scale: float
    """
    The variance of the Gaussian distribution.
    """

    def __init__(self, variable: Continuous, mean: float, scale: float):
        super().__init__(variable)
        self.mean = mean
        self.scale = scale

    @property
    def domain(self) -> ComplexEvent:
        return ComplexEvent([Event({self.variable: portion.open(-portion.inf, portion.inf)})])

    def _pdf(self, value: float) -> float:
        r"""
            Helper method to calculate the pdf of a Gaussian distribution.

            .. math::

            \varphi\left( \frac{x-\mu}{\sigma} \right) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{1}{2}
            \left(\frac{x-\mu}{\sigma} \right )^2}

        """
        if value == -portion.inf or value == portion.inf:
            return 0
        return 1 / math.sqrt(2 * math.pi * self.scale) * math.exp(-1 / 2 * (value - self.mean) ** 2 / self.scale)

    def _cdf(self, value: float) -> float:
        r"""
            Helper method to calculate the cdf of a Gaussian distribution.

            .. math::

            \Phi \left( \frac{x-\mu}{\sigma} \right) = \frac{1}{2} \left[ 1 +
            \mathbf{erf}\left( \frac{x-\mu}{\sigma\sqrt{2}} \right) \right]

        """
        if value == -portion.inf:
            return 0
        elif value == portion.inf:
            return 1
        return 0.5 * (1 + math.erf((value - self.mean) / math.sqrt(2 * self.scale)))

    def _mode(self) -> Tuple[ComplexEvent, float]:
        return ComplexEvent([EncodedEvent({self.variable: portion.singleton(self.mean)})]), self._pdf(self.mean)

    def sample(self, amount: int) -> List[List[float]]:
        return [[random.gauss(self.mean, self.scale)] for _ in range(amount)]

    def ppf(self, value):
        return norm.ppf(value, loc=self.mean, scale=self.scale)

    def raw_moment(self, order: int) -> float:
        r"""
        Helper method to calculate the raw moment of a Gaussian distribution.

        The raw moment is given by:

        .. math::

            E(X^n) = \sum_{j=0}^{\lfloor \frac{n}{2}\rfloor}\binom{n}{2j}\dfrac{\mu^{n-2j}\sigma^{2j}(2j)!}{j!2^j}.


        """
        raw_moment = 0  # Initialize the raw moment
        for j in range(math.floor(order / 2) + 1):
            mu_term = self.mean ** (order - 2 * j)
            sigma_term = self.scale ** j

            raw_moment += (math.comb(order, 2 * j) * mu_term * sigma_term * math.factorial(2 * j) / (
                        math.factorial(j) * (2 ** j)))

        return raw_moment

    def moment(self, order: OrderType, center: CenterType) -> MomentType:
        r"""
        Calculate the moment of the distribution using Alessandro's (made up) Equation:

        .. math::

            E(X-center)^i = \sum_{i=0}^{order} \binom{order}{i} E[X^i] * (- center)^{(order-i)}
        """
        order = order[self.variable]
        center = center[self.variable]

        # get the raw moments from 0 to i
        raw_moments = [self.raw_moment(i) for i in range(order + 1)]

        moment = 0

        # Compute the desired moment:
        for order_ in range(order + 1):
            moment += math.comb(order, order_) * raw_moments[order_] * (-center) ** (order - order_)

        return VariableMap({self.variable: moment})

    def conditional_from_simple_interval(self, interval: portion.Interval) -> Tuple[
        Optional['TruncatedGaussianDistribution'], float]:

        # calculate the probability of the interval
        probability = self._probability(EncodedEvent({self.variable: interval}))

        # if the probability is 0, return None
        if probability == 0:
            return None, 0

        # else, form the intersection of the interval and the domain
        intersection = interval
        resulting_distribution = TruncatedGaussianDistribution(self.variable, interval=intersection, mean=self.mean,
                                                               scale=self.scale)
        return resulting_distribution, probability

    def __eq__(self, other):
        return super().__eq__(other) and self.mean == other.mean and self.scale == other.scale

    @property
    def representation(self):
        return f"N({self.mean}, {self.scale})"

    def __copy__(self):
        return self.__class__(self.variable, self.mean, self.scale)

    def to_json(self) -> Dict[str, Any]:
        return {**super().to_json(), "mean": self.mean, "variance": self.scale}

    @classmethod
    def _from_json(cls, data: Dict[str, Any]) -> Self:
        variable = Continuous.from_json(data["variable"])
        return cls(variable, data["mean"], data["variance"])


class TruncatedGaussianDistribution(GaussianDistribution):
    """
    Class for Truncated Gaussian distributions.
    """

    def __init__(self, variable: Continuous, interval: portion.Interval, mean: float, scale: float):
        super().__init__(variable, mean, scale)
        self.interval = interval

    @property
    def domain(self) -> ComplexEvent:
        return ComplexEvent([Event({self.variable: self.interval})])

    @property
    def lower(self) -> float:
        return self.interval.lower

    @property
    def upper(self) -> float:
        return self.interval.upper

    @property
    def normalizing_constant(self) -> float:
        r"""
            Helper method to calculate

            .. math::

            Z = {\mathbf{\Phi}\left ( \frac{self.interval.upper-\mu}{\sigma} \right )-\mathbf{\Phi}
            \left( \frac{self.interval.lower-\mu}{\sigma} \right )}

        """
        return super()._cdf(self.upper) - super()._cdf(self.lower)

    def _pdf(self, value: float) -> float:

        if value in self.interval:
            return super()._pdf(value) / self.normalizing_constant
        else:
            return 0

    def _cdf(self, value: float) -> float:

        if value in self.interval:
            return (super()._cdf(value) - super()._cdf(self.lower)) / self.normalizing_constant
        elif value <= self.lower:
            return 0
        else:
            return 1

    def _mode(self) -> Tuple[ComplexEvent, float]:
        if self.mean in self.interval:
            mode, likelihood = [EncodedEvent({self.variable: portion.singleton(self.mean)})], self._pdf(self.mean)
        elif self.mean < self.lower:
            mode, likelihood = [EncodedEvent({self.variable: portion.singleton(self.lower)})], self._pdf(self.lower)
        else:
            mode, likelihood = [EncodedEvent({self.variable: portion.singleton(self.upper)})], self._pdf(self.upper)
        return ComplexEvent(mode), likelihood

    def rejection_sample(self, amount: int) -> List[List[float]]:
        """
        .. note::
            This uses rejection sampling and hence is inefficient.

        """
        samples = super().sample(amount)
        samples = [sample for sample in samples if sample[0] in self.interval]
        rejected_samples = amount - len(samples)
        if rejected_samples > 0:
            samples.extend(self.rejection_sample(rejected_samples))
        return samples

    def moment(self, order: OrderType, center: CenterType) -> MomentType:
        r"""
                Helper method to calculate the moment of a Truncated Gaussian distribution.

                .. note::
                This method follows the equation (2.8) in :cite:p:`ogasawara2022moments`.

                .. math::

                    \mathbb{E} \left[ \left( X-center \right)^{order} \right]\mathds{1}_{\left[ lower , upper \right]}(x)
                    = \sigma^{order} \frac{1}{\Phi(upper)-\Phi(lower)} \sum_{k=0}^{order} \binom{order}{k} I_k (-center)^{(order-k)}.

                    where:

                    .. math::

                        I_k = \frac{2^{\frac{k}{2}}}{\sqrt{\pi}}\Gamma \left( \frac{k+1}{2} \right) \left[ sgn \left(upper\right)
                         \mathds{1}\left \{ k=2 \nu \right \} + \mathds{1} \left\{k = 2\nu -1 \right\} \frac{1}{2}
                          F_{\Gamma} \left( \frac{upper^2}{2},\frac{k+1}{2} \right) - sgn \left(lower\right) \mathds{1}\left \{ k=2 \nu \right \}
                         + \mathds{1} \left\{k = 2\nu -1 \right\} \frac{1}{2} F_{\Gamma} \left( \frac{lower^2}{2},\frac{k+1}{2} \right) \right]

                :return: The moment of the distribution.

                """

        order = order[self.variable]
        center = center[self.variable]

        lower_bound = self.transform_to_standard_normal(self.lower)  # normalize the lower bound
        upper_bound = self.transform_to_standard_normal(self.upper)  # normalize the upper bound
        normalized_center = self.transform_to_standard_normal(center)  # normalize the center
        truncated_moment = 0

        for k in range(order + 1):

            multiplying_constant = math.comb(order, k) * 2 ** (k / 2) * math.gamma((k + 1) / 2) / math.sqrt(math.pi)

            if k % 2 == 0:
                bound_selection_lower = np.sign(lower_bound)
                bound_selection_upper = np.sign(upper_bound)
            else:
                bound_selection_lower = 1
                bound_selection_upper = 1

            gamma_term_lower = -0.5 * gamma.cdf(lower_bound ** 2 / 2, (k + 1) / 2) * bound_selection_lower
            gamma_term_upper = 0.5 * gamma.cdf(upper_bound ** 2 / 2, (k + 1) / 2) * bound_selection_upper

            truncated_moment += (
                        multiplying_constant * (gamma_term_lower + gamma_term_upper) * (-normalized_center) ** (
                            order - k))

        truncated_moment *= (math.sqrt(self.scale) ** order) / self.normalizing_constant

        return VariableMap({self.variable: truncated_moment})

    def __eq__(self, other):
        return super().__eq__(other) and self.interval == other.interval

    @property
    def representation(self):
        return f"N({self.mean},{self.scale} | {self.interval})"

    def __copy__(self):
        return self.__class__(self.variable, self.interval, self.mean, self.scale)

    def to_json(self) -> Dict[str, Any]:
        return {**super().to_json(), "interval": portion.to_data(self.interval)}

    @classmethod
    def _from_json(cls, data: Dict[str, Any]) -> Self:
        variable = Continuous.from_json(data["variable"])
        interval = portion.from_data(data["interval"])
        return cls(variable, interval, data["mean"], data["variance"])

    def transform_to_standard_normal(self, number: float) -> float:
        """
        Transform the number to the standard normal distribution.
        :param number: The number to transform
        :return: The transformed bound
        """
        if number <= -portion.inf:
            transformed_bound = -float("inf")
        elif number >= portion.inf:
            transformed_bound = float("inf")
        else:
            transformed_bound = (number - self.mean) / np.sqrt(self.scale)
        return transformed_bound

    def robert_rejection_sample(self, amount: int) -> np.ndarray:
        """
        Use robert rejection sampling to sample from the truncated Gaussian distribution.

        :param amount: The amount of samples to generate
        :return: The samples
        """
        # handle the case where the distribution is not the standard normal
        new_interval = self.interval.replace(lower=self.transform_to_standard_normal(self.interval.lower),
                                             upper=self.transform_to_standard_normal(self.interval.upper))
        standard_distribution = self.__class__(self.variable, new_interval, 0, 1)

        # enforce an upper bound if it is infinite
        if standard_distribution.interval.upper >= float("inf"):
            standard_distribution.interval = (standard_distribution.interval.
                                              replace(upper=standard_distribution.interval.lower + 10))

        # enforce a lower bound if it is infinite
        if standard_distribution.interval.lower <= -float("inf"):
            standard_distribution.interval = (standard_distribution.interval.
                                              replace(lower=standard_distribution.interval.upper - 10))

        # sample from double truncated standard normal instead
        samples = standard_distribution.robert_rejection_sample_from_standard_normal_with_double_truncation(amount)

        # transform samples to this distributions mean and scale
        samples *= np.sqrt(self.scale)
        samples += self.mean

        return samples

    def robert_rejection_sample_from_standard_normal_with_double_truncation(self, amount: int) -> np.ndarray:
        """
        Use robert rejection sampling to sample from the truncated standard normal distribution.
        Resamples as long as the amount of samples is not reached.

        :param amount: The amount of samples to generate
        :return: The samples
        """
        assert self.scale == 1 and self.mean == 0
        # sample from uniform distribution over this distribution's interval
        accepted_samples = np.array([])
        while len(accepted_samples) < amount:
            accepted_samples = np.append(
                accepted_samples,
                self.robert_rejection_sample_from_standard_normal_with_double_truncation_helper(amount - len(accepted_samples)))
        return accepted_samples

    def robert_rejection_sample_from_standard_normal_with_double_truncation_helper(self, amount: int) -> np.ndarray:
        """
        Use robert rejection sampling to sample from the truncated standard normal distribution.

        :param amount: The maximum number of samples to generate. The actual number of samples can be lower due to
            rejection sampling.
        :return: The samples
        """
        uniform_samples = np.random.uniform(self.interval.lower, self.interval.upper, amount)

        # if the mean in the interval
        if 0 in self.interval:
            limiting_function = np.exp((uniform_samples ** 2) / -2)

        # if the mean is below the interval
        elif self.interval.upper <= 0:
            limiting_function = np.exp((self.interval.upper ** 2 - uniform_samples ** 2) / 2)

        # if the mean is above the interval
        elif self.interval.lower >= 0:
            limiting_function = np.exp((self.interval.lower ** 2 - uniform_samples ** 2) / 2)
        else:
            raise ValueError("This should never happen")

        # generate standard uniform samples as acceptance probabilities
        acceptance_probabilities = np.random.uniform(0, 1, amount)

        # accept samples that are below the limiting function
        accepted_samples = uniform_samples[acceptance_probabilities <= limiting_function]
        return accepted_samples

    def sample(self, amount: int) -> List[List[float]]:
        if self.interval.upper >= portion.inf and self.interval.lower <= -portion.inf:
            return super().sample(amount)
        return self.robert_rejection_sample(amount).reshape(-1, 1).tolist()
