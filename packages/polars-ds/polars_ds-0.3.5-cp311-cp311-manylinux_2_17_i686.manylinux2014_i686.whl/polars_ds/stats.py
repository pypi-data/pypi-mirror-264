from __future__ import annotations
import polars as pl
import math
from .type_alias import Alternative, str_to_expr
from typing import Optional, Union
from polars.utils.udfs import _get_shared_lib_location

_lib = _get_shared_lib_location(__file__)


@pl.api.register_expr_namespace("stats")
class StatsExt:

    """
    This class contains tools for dealing with well-known statistical tests and random sampling inside Polars DataFrame.

    Polars Namespace: stats

    Example: pl.col("a").stats.ttest_ind(pl.col("b"), equal_var = True)
    """

    def __init__(self, expr: pl.Expr):
        self._expr: pl.Expr = expr

    def ttest_ind_from_stats(
        self,
        other_mean: float,
        other_var: float,
        other_cnt: int,
        alternative: Alternative = "two-sided",
        equal_var: bool = False,
    ) -> pl.Expr:
        """
        Performs 2 sample student's t test or Welch's t test, using only scalar statistics from other.
        This is more suitable for t-tests between rolling data and some other fixed data, from which you
        can compute the mean, var, and count only once.

        Parameters
        ----------
        other_mean
            The mean of other
        other_var
            The var of other
        other_cnt
            The count of other, used only in welch's t test
        alternative : {"two-sided", "less", "greater"}
            Alternative of the hypothesis test
        equal_var
            If true, perform standard student t 2 sample test. Otherwise, perform Welch's
            t test.
        """
        if equal_var:
            m1 = self._expr.mean()
            m2 = pl.lit(other_mean, pl.Float64)
            v1 = self._expr.var()
            v2 = pl.lit(other_var, pl.Float64)
            cnt = self._expr.count().cast(pl.UInt64)
            return m1.register_plugin(
                lib=_lib,
                symbol="pl_ttest_2samp",
                args=[m2, v1, v2, cnt, pl.lit(alternative, dtype=pl.String)],
                is_elementwise=False,
                returns_scalar=True,
            )
        else:
            s1 = self._expr.filter(self._expr.is_finite())
            m1 = s1.mean()
            m2 = pl.lit(other_mean, pl.Float64)
            v1 = s1.var()
            v2 = pl.lit(other_var, pl.Float64)
            n1 = s1.count().cast(pl.UInt64)
            n2 = pl.lit(other_cnt, pl.UInt64)
            return m1.register_plugin(
                lib=_lib,
                symbol="pl_welch_t",
                args=[m2, v1, v2, n1, n2, pl.lit(alternative, dtype=pl.String)],
                is_elementwise=False,
                returns_scalar=True,
            )

    def ttest_ind(
        self, other: pl.Expr, alternative: Alternative = "two-sided", equal_var: bool = False
    ) -> pl.Expr:
        """
        See query_ttest_ind
        """
        if equal_var:
            m1 = self._expr.mean()
            m2 = other.mean()
            v1 = self._expr.var()
            v2 = other.var()
            cnt = self._expr.count().cast(pl.UInt64)
            return m1.register_plugin(
                lib=_lib,
                symbol="pl_ttest_2samp",
                args=[m2, v1, v2, cnt, pl.lit(alternative, dtype=pl.String)],
                returns_scalar=True,
            )
        else:
            s1 = self._expr.filter(self._expr.is_finite())
            s2 = other.filter(other.is_finite())
            m1 = s1.mean()
            m2 = s2.mean()
            v1 = s1.var()
            v2 = s2.var()
            n1 = s1.count().cast(pl.UInt64)
            n2 = s2.count().cast(pl.UInt64)
            return m1.register_plugin(
                lib=_lib,
                symbol="pl_welch_t",
                args=[m2, v1, v2, n1, n2, pl.lit(alternative, dtype=pl.String)],
                returns_scalar=True,
            )

    def ttest_1samp(self, pop_mean: float, alternative: Alternative = "two-sided") -> pl.Expr:
        """
        Performs a standard 1 sample t test using reference column and expected mean. This function
        sanitizes the self column first. The df is the count of valid values.

        Parameters
        ----------
        pop_mean
            The expected population mean in the hypothesis test
        alternative : {"two-sided", "less", "greater"}
            Alternative of the hypothesis test
        """
        s1 = self._expr.filter(self._expr.is_finite())
        sm = s1.mean()
        pm = pl.lit(pop_mean, dtype=pl.Float64)
        var = s1.var()
        cnt = s1.count().cast(pl.UInt64)
        alt = pl.lit(alternative, dtype=pl.String)
        return sm.register_plugin(
            lib=_lib,
            symbol="pl_ttest_1samp",
            args=[pm, var, cnt, alt],
            returns_scalar=True,
        )

    def f_stats(self, *variables: pl.Expr) -> pl.Expr:
        """
        Computes multiple F statistics at once by using self as the grouping (class) column. This
        does not output p values. If the p value is desired, use `f_test`. This will return
        all the stats as a scalar list in order.

        Parameters
        ----------
        *variables
            The variables (Polars df columns) to compute the F statistics
        """
        return self._expr.register_plugin(
            lib=_lib,
            symbol="pl_f_stats",
            args=list(variables),
            returns_scalar=True,
        )

    def f_test(self, var: pl.Expr) -> pl.Expr:
        """
        Performs the ANOVA F-test using self as the grouping column.

        Parameters
        ----------
        var
            The column to run ANOVA F-test on
        """
        return self._expr.register_plugin(
            lib=_lib,
            symbol="pl_f_test",
            args=[var],
            returns_scalar=True,
        )

    def normal_test(self) -> pl.Expr:
        """
        Perform a normality test which is based on D'Agostino and Pearson's test
        that combines skew and kurtosis to produce an omnibus test of normality.
        Null values, NaN and inf are dropped when running this computation.

        References
        ----------
        D'Agostino, R. B. (1971), "An omnibus test of normality for
            moderate and large sample size", Biometrika, 58, 341-348
        D'Agostino, R. and Pearson, E. S. (1973), "Tests for departure from
            normality", Biometrika, 60, 613-622
        """
        valid: pl.Expr = self._expr.filter(self._expr.is_finite())
        skew = valid.skew()
        # Pearson Kurtosis, see here: https://en.wikipedia.org/wiki/D%27Agostino%27s_K-squared_test
        kur = valid.kurtosis(fisher=False)
        return skew.register_plugin(
            lib=_lib,
            symbol="pl_normal_test",
            args=[kur, valid.count().cast(pl.UInt32)],
            returns_scalar=True,
        )

    def ks_stats(self, var: pl.Expr, alpha: float = 0.05) -> pl.Expr:
        """
        See query_ks_2samp
        """
        y = self._expr.filter(self._expr.is_finite()).sort().cast(pl.Float64)
        other_ = var.filter(var.is_finite()).sort().cast(pl.Float64)
        return y.register_plugin(
            lib=_lib,
            symbol="pl_ks_2samp",
            args=[other_, pl.lit(alpha, pl.Float64)],
            returns_scalar=True,
        )

    def ks_binary_classif(self, target: pl.Expr, alpha: float = 0.05) -> pl.Expr:
        """
        Given a binary target, compute the ks statistics by comparing the feature when target = 1
        with the same feature when target != 1.

        Parameters
        ----------
        target
            A Polars Expression representing the binary target
        """
        y = self._expr.filter(self._expr.is_finite()).cast(pl.Float64)
        y1 = y.filter(target == 1).sort()
        y2 = y.filter(target < 1).sort()
        return y1.register_plugin(
            lib=_lib,
            symbol="pl_ks_2samp",
            args=[y2, pl.lit(alpha, pl.Float64)],
            returns_scalar=True,
        )

    def chi2(self, var: pl.Expr) -> pl.Expr:
        """
        Computes the Chi Squared statistic and p value between two categorical values by treating
        self as the first column and var as the second.

        Note that it is up to the user to make sure that the two columns contain categorical
        values. This method is equivalent to SciPy's chi2_contingency, except that it also
        computes the contingency table internally for the user.

        Parameters
        ----------
        var
            The second column to run chi squared test on
        """

        return self._expr.register_plugin(
            lib=_lib,
            symbol="pl_chi2",
            args=[var],
            returns_scalar=True,
        )

    def _rand_int(self, lower: int, upper: int, seed: Optional[int] = None) -> pl.Expr:
        """
        See random_int
        """
        return self._expr.register_plugin(
            lib=_lib,
            symbol="pl_rand_int",
            args=[pl.lit(lower, pl.Int32), pl.lit(upper, pl.Int32), pl.lit(seed, pl.UInt64)],
            is_elementwise=True,
        )

    def _random(
        self,
        lower: Union[pl.Expr, float] = 0.0,
        upper: Union[pl.Expr, float] = 1.0,
        seed: Optional[int] = None,
    ) -> pl.Expr:
        """
        See random
        """
        lo = pl.lit(lower, pl.Float64) if isinstance(lower, float) else lower
        up = pl.lit(upper, pl.Float64) if isinstance(upper, float) else upper
        return self._expr.register_plugin(
            lib=_lib,
            symbol="pl_random",
            args=[lo, up, pl.lit(seed, pl.UInt64)],
            is_elementwise=True,
        )

    def _rand_binomial(self, n: int, p: int, seed: Optional[int] = None) -> pl.Expr:
        """
        See random_binomial
        """
        return self._expr.register_plugin(
            lib=_lib,
            symbol="pl_rand_binomial",
            args=[pl.lit(n, pl.Int32), pl.lit(p, pl.Float64), pl.lit(seed, pl.UInt64)],
            is_elementwise=True,
        )

    def _rand_normal(
        self,
        mean: Union[pl.Expr, float] = 0.0,
        std: Union[pl.Expr, float] = 1.0,
        seed: Optional[int] = None,
    ) -> pl.Expr:
        """
        See random_normal
        """
        m = pl.lit(mean, pl.Float64) if isinstance(mean, float) else mean
        s = pl.lit(std, pl.Float64) if isinstance(std, float) else std
        return self._expr.register_plugin(
            lib=_lib,
            symbol="pl_rand_normal",
            args=[m, s, pl.lit(seed, pl.UInt64)],
            is_elementwise=True,
        )

    def _rand_exp(self, lambda_: float, seed: Optional[int] = None) -> pl.Expr:
        """
        See random_exp
        """
        return self._expr.register_plugin(
            lib=_lib,
            symbol="pl_rand_exp",
            args=[pl.lit(lambda_, pl.Float64), pl.lit(seed, pl.UInt64)],
            is_elementwise=True,
        )

    def _rand_str(
        self, min_size: int = 1, max_size: int = 10, seed: Optional[int] = None
    ) -> pl.Expr:
        """
        See random_str
        """
        return self._expr.register_plugin(
            lib=_lib,
            symbol="pl_rand_str",
            args=[
                pl.lit(min_size, pl.UInt32),
                pl.lit(max_size, pl.UInt32),
                pl.lit(seed, pl.UInt64),
            ],
            is_elementwise=True,
        )

    def rand_int(
        self,
        low: Union[int, pl.Expr] = 0,
        high: Optional[Union[int, pl.Expr]] = 10,
        seed: Optional[int] = None,
        respect_null: bool = False,
    ) -> pl.Expr:
        """
        Generates random integers uniformly from the range [low, high). Throws an error if low == high
        or if low is None and high is None.

        This treats self as the reference column.

        Parameters
        ----------
        low
            Lower end of random sample. If high is none, low will be set to 0.
        high
            Higher end of random sample. If this is None, then it will be replaced n_unique of reference.
        seed
            A seed to fix the random numbers. If none, use the system's entropy.
        respect_null
            If true, null in reference column will be null in the new column
        """

        if high is None:
            lo = pl.lit(0, dtype=pl.Int32)
            hi = self._expr.n_unique.cast(pl.UInt32)
        else:
            if isinstance(low, pl.Expr):
                lo = low
            elif isinstance(low, int):
                lo = pl.lit(low, dtype=pl.Int32)
            else:
                raise ValueError("Input `low` must be expression or int.")

            if isinstance(high, pl.Expr):
                hi = high
            elif isinstance(high, int):
                hi = pl.lit(high, dtype=pl.Int32)
            else:
                raise ValueError("Input `high` must be expression or int.")

        return self._expr.register_plugin(
            lib=_lib,
            symbol="pl_rand_int_w_ref",
            args=[lo, hi],
            kwargs={"seed": seed, "respect_null": respect_null},
            is_elementwise=True,
        )

    def rand_uniform(
        self,
        low: Optional[Union[float, pl.Expr]] = 0.0,
        high: Optional[Union[float, pl.Expr]] = 1.0,
        seed: Optional[int] = None,
        respect_null: bool = False,
    ) -> pl.Expr:
        """
        Creates random points from a uniform distribution within [low, high).
        This will throw an error if low == high.

        This treats self as the reference column.

        Parameters
        ----------
        low
            Lower end of random sample. If none, use reference col's min.
        high
            Higher end of random sample. If none, use reference col's max.
        seed
            A seed to fix the random numbers. If none, use the system's entropy.
        respect_null
            If true, null in reference column will be null in the new column
        """
        if isinstance(low, pl.Expr):
            lo = low
        elif isinstance(low, float):
            lo = pl.lit(low, dtype=pl.Float64)
        else:
            lo = self._expr.min().cast(pl.Float64)

        if isinstance(high, pl.Expr):
            hi = high
        elif isinstance(high, float):
            hi = pl.lit(high, dtype=pl.Float64)
        else:
            hi = self._expr.max().cast(pl.Float64)

        return self._expr.register_plugin(
            lib=_lib,
            symbol="pl_rand_uniform_w_ref",
            args=[lo, hi],
            kwargs={"seed": seed, "respect_null": respect_null},
            is_elementwise=True,
        )

    def perturb(self, epsilon: float, positive: bool = False):
        """
        Perturb self by a small amount. This only applies to float columns.

        Parameters
        ----------
        epsilon
            The small amount to perturb.
        positive
            If true, randomly add a small amount in [0, epsilon). If false, it will use the range
            [-epsilon/2, epsilon/2)
        """
        if math.isinf(epsilon) or math.isnan(epsilon):
            raise ValueError("Input `epsilon should be a valid finite value.`")

        ep = abs(epsilon)
        if positive:
            lo = pl.lit(0.0, dtype=pl.Float64)
            hi = pl.lit(ep, dtype=pl.Float64)
        else:
            half = ep / 2
            lo = pl.lit(-half, dtype=pl.Float64)
            hi = pl.lit(half, dtype=pl.Float64)

        return self._expr.register_plugin(
            lib=_lib,
            symbol="pl_perturb",
            args=[lo, hi],
            is_elementwise=True,
        )

    def rand_binomial(
        self, n: int, p: float, seed: Optional[int] = None, respect_null: bool = False
    ) -> pl.Expr:
        """
        Creates random points from a binomial distribution with n and p.

        This treats self as the reference column.

        Parameters
        ----------
        n
            n in a binomial distribution
        p
            p in a binomial distribution
        seed
            A seed to fix the random numbers. If none, use the system's entropy.
        respect_null
            If true, null in reference column will be null in the new column
        """

        nn = pl.lit(n, dtype=pl.UInt32)
        pp = pl.lit(p, dtype=pl.Float64)
        return self._expr.register_plugin(
            lib=_lib,
            symbol="pl_rand_binomial_w_ref",
            args=[nn, pp],
            kwargs={"seed": seed, "respect_null": respect_null},
            is_elementwise=True,
        )

    def rand_exp(
        self,
        lambda_: Optional[Union[float, pl.Expr]] = None,
        seed: Optional[int] = None,
        respect_null: bool = False,
    ) -> pl.Expr:
        """
        Creates random points from a exponential distribution with parameter `lambda_`.

        This treats self as the reference column.

        Parameters
        ----------
        lambda_
            If none, it will be 1/reference col's mean. Note that if
            lambda < 0 this will throw an error and lambda = 0 will only return infinity.
        seed
            A seed to fix the random numbers. If none, use the system's entropy.
        respect_null
            If true, null in reference column will be null in the new column
        """
        if isinstance(lambda_, pl.Expr):
            la = lambda_
        elif isinstance(lambda_, float):
            la = pl.lit(lambda_, dtype=pl.Float64)
        else:
            la = 1.0 / self._expr.mean()

        return self._expr.register_plugin(
            lib=_lib,
            symbol="pl_rand_exp_w_ref",
            args=[la],
            kwargs={"seed": seed, "respect_null": respect_null},
            is_elementwise=True,
        )

    def rand_normal(
        self,
        mean: Optional[Union[float, pl.Expr]] = None,
        std: Optional[Union[float, pl.Expr]] = None,
        seed: Optional[int] = None,
        respect_null: bool = False,
    ) -> pl.Expr:
        """
        Creates random points from a normal distribution with the given
        mean and std.

        This treats self as the reference column.

        Parameters
        ----------
        mean
            Mean of the normal distribution. If none, use reference col's mean.
        std
            Std of the normal distribution. If none, use reference col's std.
        seed
            A seed to fix the random numbers. If none, use the system's entropy.
        respect_null
            If true, null in reference column will be null in the new column
        """
        if isinstance(mean, pl.Expr):
            me = mean
        elif isinstance(mean, (float, int)):
            me = pl.lit(mean, dtype=pl.Float64)
        else:
            me = self._expr.mean()

        if isinstance(std, pl.Expr):
            st = std
        elif isinstance(std, (float, int)):
            st = pl.lit(std, dtype=pl.Float64)
        else:
            st = self._expr.std()

        return self._expr.register_plugin(
            lib=_lib,
            symbol="pl_rand_normal_w_ref",
            args=[me, st],
            kwargs={"seed": seed, "respect_null": respect_null},
            is_elementwise=True,
        )

    def rand_null(self, pct: float, seed: Optional[int] = None) -> pl.Expr:
        """
        Creates random null values in self. If self contains nulls originally, they
        will stay null.

        Parameters
        ----------
        pct
            Percentage of nulls to randomly generate. This percentage is based on the
            length of the column, so may not be the actual percentage of nulls depending
            on how many values are originally null.
        seed
            A seed to fix the random numbers. If none, use the system's entropy.
        """
        if pct <= 0.0 or pct >= 1.0:
            raise ValueError("Input `pct` must be > 0 and < 1")

        to_null = self.rand_uniform(0.0, 1.0, seed=seed) < pct
        return pl.when(to_null).then(None).otherwise(self._expr)

    def rand_str(
        self,
        min_size: int = 1,
        max_size: int = 10,
        seed: Optional[int] = None,
        respect_null: bool = False,
    ) -> pl.Expr:
        """
        Creates self.len() many random strings with alpha-numerical values. Unfortunately that
        means this currently only generates strings satisfying [0-9a-zA-Z]. The string's
        length will also be uniformly.

        This treats self as the reference column.

        Parameters
        ----------
        min_size
            The minimum length of the string to be generated. The length of the string will be
            uniformly generated in [min_size, max_size), except when min_size = max_size, in
            which case only fixed length strings will be generated.
        max_size
            The maximum length of the string to be generated.
        seed
            A seed to fix the random numbers. If none, use the system's entropy.
        respect_null
            If true, null in reference column will be null in the new column
        """
        if min_size <= 0 or (max_size < min_size):
            raise ValueError("String size must be positive and max_size must be >= min_size.")

        min_s = pl.lit(min_size, dtype=pl.UInt32)
        max_s = pl.lit(max_size, dtype=pl.UInt32)
        return self._expr.register_plugin(
            lib=_lib,
            symbol="pl_rand_str_w_ref",
            args=[min_s, max_s],
            kwargs={"seed": seed, "respect_null": respect_null},
            is_elementwise=True,
        )

    def t_mean(self, lower: float, upper: float) -> pl.Expr:
        """
        Computes the trimmed mean of the variable.

        Parameters
        ----------
        lower
            The lower end, smaller values will be trimmed
        upper
            The upper end, larger values will be trimmed
        """
        return self._expr.filter(self._expr.is_between(lower, upper)).mean()

    def t_var(self, lower: float, upper: float, ddof: int = 1) -> pl.Expr:
        """
        Computes the trimmed var of the variable.

        Parameters
        ----------
        lower
            The lower end, smaller values will be trimmed
        upper
            The upper end, larger values will be trimmed
        """
        return self._expr.filter(self._expr.is_between(lower, upper)).var(ddof)

    def w_mean(self, weights: pl.Expr, is_normalized: bool = False) -> pl.Expr:
        """
        Computes the weighted mean of self, where weights is an expr represeting
        a weight column. The weights column must have the same length as self.

        All weights are assumed to be > 0. This will not check if weight is zero.

        Parameters
        ----------
        weights
            An expr representing weights. Must be of same length as self.
        is_normalized
            If true, the weights are assumed to sum to 1. If false, will divide by sum of the weights
        """
        out = self._expr.dot(weights)
        if is_normalized:
            return out
        return out / weights.sum()

    def w_var(self, weights: pl.Expr, is_normalized: bool = False) -> pl.Expr:
        """
        Computes the weighted var of self, where weights is an expr represeting
        a weight column. The weights column must have the same length as self.

        All weights are assumed to be > 0. This will not check if weight is zero.

        Parameters
        ----------
        weights
            An expr representing weights. Must be of same length as self.
        is_normalized
            If true, the weights are assumed to sum to 1. If false, will divide by sum of the weights
        """
        centered_squared = (self._expr - self._expr.mean()).pow(2)
        out = weights.dot(centered_squared)
        if is_normalized:
            denom = (self._expr.count() - 1) / self._expr.count()
        else:
            denom = weights.sum() * (self._expr.count() - 1) / self._expr.count()

        return out / denom

    def w_gmean(self, weights: pl.Expr, is_normalized: bool = False) -> pl.Expr:
        """
        Computes the weighted geometric mean.

        Parameters
        ----------
        weights
            An expr representing weights. Must be of same length as self.
        is_normalized
            If true, the weights are assumed to sum to 1. If false, will divide by sum of the weights
        """
        if is_normalized:
            return (self._expr.ln().dot(weights)).exp()
        else:
            return (self._expr.ln().dot(weights) / (weights.sum())).exp()


def query_ttest_ind(
    var1: Union[str, pl.Expr],
    var2: Union[str, pl.Expr],
    alternative: Alternative = "two-sided",
    equal_var: bool = False,
) -> pl.Expr:
    """
    Performs 2 sample student's t test or Welch's t test. Functionality-wise this is desgined
    to be equivalent to SciPy's ttest_ind, with fewer options. The result is not exact but
    within 1e-10 precision from SciPy's.

    In the case of student's t test, the data is assumed to have no nulls, and n = self._expr.count()
    is used. Note self._expr.count() only counts non-null elements after polars 0.20.
    The degree of freedom will be 2n - 2. As a result, nulls might cause problems.

    In the case of Welch's t test, data will be sanitized (nulls, NaNs, Infs will be dropped
    before the test), and df will be counted based on the length of sanitized data.

    Parameters
    ----------
    var1
        Variable 1
    var2
        Variable 2
    alternative : {"two-sided", "less", "greater"}
        Alternative of the hypothesis test
    equal_var
        If true, perform standard student t 2 sample test. Otherwise, perform Welch's
        t test.
    """
    return str_to_expr(var1).stats.ttest_ind(
        str_to_expr(var2), alternative=alternative, equal_var=equal_var
    )


def query_ttest_ind_from_stats(
    var1: Union[str, pl.Expr],
    mean: float,
    var: float,
    cnt: int,
    alternative: Alternative = "two-sided",
    equal_var: bool = False,
) -> pl.Expr:
    """
    Performs 2 sample student's t test or Welch's t test, using only scalar statistics from other.
    This is more suitable for t-tests between rolling data and some other fixed data, from which you
    can compute the mean, var, and count only once.

    Parameters
    ----------
    var1
        The variable 1
    mean
        The mean of var2
    var
        The var of var2
    cnt
        The count of var2, used only in welch's t test
    alternative : {"two-sided", "less", "greater"}
        Alternative of the hypothesis test
    equal_var
        If true, perform standard student t 2 sample test. Otherwise, perform Welch's
        t test.
    """
    return str_to_expr(var1).stats.ttest_ind_from_stats(
        other_mean=mean, other_var=var, other_cnt=cnt, alternative=alternative, equal_var=equal_var
    )


def query_ks_2samp(
    var1: Union[str, pl.Expr],
    var2: Union[str, pl.Expr],
    alpha: float = 0.05,
    is_binary: bool = False,
) -> pl.Expr:
    """
    Computes two-sided KS statistics between var1 and var2. This will
    sanitize data (only non-null finite values are used) before doing the computation. If
    is_binary true, it will compare the statistics by comparing var2(var1=0) and var2(var1=1).

    Note, this returns a stastics and a threshold value. The threshold value is not the p-value, but
    rather it is used in the following way: if the statistic is > the threshold value, then the null
    hypothesis should be rejected. This is suitable only for large sameple sizes. See the reference.

    Parameters
    ----------
    var1
        Variable 1
    var2
        Variable 2
    alpha
        The confidence level used to estimate p-value
    is_binary
        If true, instead of running ks(var1, var2), it runs ks(var2(var1=0), var2(var1=1))

    Reference
    ---------
    https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test#Two-sample_Kolmogorov%E2%80%93Smirnov_test
    """
    if is_binary:
        return str_to_expr(var2).stats.ks_binary_classif(str_to_expr(var1), alpha=alpha)
    return str_to_expr(var1).stats.ks_stats(str_to_expr(var2), alpha=alpha)


def random(lower: float = 0.0, upper: float = 1.0, seed: Optional[int] = None) -> pl.Expr:
    """
    Generates random numbers uniformly.

    Parameters
    ----------
    lower
        The lower bound, inclusive
    upper
        The upper bound, exclusive
    seed
        The random seed. None means no seed.
    """
    if lower == upper:
        raise ValueError("Input `lower` must be smaller than `higher`")

    lo, hi = lower, upper
    if lower > upper:
        lo, hi = upper, lower

    return pl.len().cast(pl.UInt32).stats._random(lower=lo, upper=hi, seed=seed)


def random_int(lower: int, upper: int, seed: Optional[int] = None) -> pl.Expr:
    """
    Generates random integer between lower and upper.

    Parameters
    ----------
    lower
        The lower bound, inclusive
    upper
        The upper bound, exclusive
    seed
        The random seed. None means no seed.
    """
    if lower == upper:
        raise ValueError("Input `lower` must be smaller than `higher`")

    lo, hi = lower, upper
    if lower > upper:
        lo, hi = upper, lower

    return pl.len().cast(pl.UInt32).stats._rand_int(lower=lo, upper=hi, seed=seed)


def random_str(min_size: int, max_size: int) -> pl.Expr:
    """
    Generates random strings of length between min_size and max_size.

    Parameters
    ----------
    min_size
        The min size of the string, inclusive
    max_size
        The max size of the string, inclusive
    seed
        The random seed. None means no seed.
    """
    mi, ma = min_size, max_size
    if min_size > max_size:
        mi, ma = max_size, min_size

    return pl.len().cast(pl.UInt32).stats._rand_str(min_size=mi, max_size=ma, seed=None)


def random_binomial(n: int, p: int, seed: Optional[int] = None) -> pl.Expr:
    """
    Generates random integer following a binomial distribution.

    Parameters
    ----------
    n
        The n in a binomial distribution
    p
        The p in a binomial distribution
    seed
        The random seed. None means no seed.
    """
    if n < 1:
        raise ValueError("Input `n` must be > 1.")

    return pl.len().cast(pl.UInt32).stats._rand_binomial(n=n, p=p, seed=seed)


def random_exp(lambda_: float, seed: Optional[int] = None) -> pl.Expr:
    """
    Generates random numbers following an exponential distribution.

    Parameters
    ----------
    lambda_
        The lambda in an exponential distribution
    seed
        The random seed. None means no seed.
    """
    return pl.len().cast(pl.UInt32).stats._rand_exp(lambda_=lambda_, seed=seed)


def random_normal(mean: float, std: float, seed: Optional[int] = None) -> pl.Expr:
    """
    Generates random number following a normal distribution.

    Parameters
    ----------
    mean
        The mean in a normal distribution
    std
        The std in a normal distribution
    seed
        The random seed. None means no seed.
    """
    return pl.len().cast(pl.UInt32).stats._rand_normal(mean=mean, std=std, seed=seed)
