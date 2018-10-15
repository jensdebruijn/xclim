import numpy as np
import pandas as pd
import pytest
import xarray as xr
from xclim.indices import tg_mean
from xclim import checks


class TestDateHandling:

    def test_assert_daily(self):
        n = 365  # one day short of a full year
        times = pd.date_range('2000-01-01', freq='1D', periods=n)
        da = xr.DataArray(np.arange(n), [('time', times)])
        assert tg_mean(da)

    # Bad frequency
    def test_bad_frequency(self):
        with pytest.raises(ValueError):
            n = 365
            times = pd.date_range('2000-01-01', freq='12H', periods=n)
            da = xr.DataArray(np.arange(n), [('time', times)])
            tg_mean(da)

    # Missing one day between the two years
    def test_missing_one_day_between_two_years(self):
        with pytest.raises(ValueError):
            n = 365
            times = pd.date_range('2000-01-01', freq='1D', periods=n)
            times = times.append(pd.date_range('2001-01-01', freq='1D', periods=n))
            da = xr.DataArray(np.arange(2*n), [('time', times)])
            tg_mean(da)

    # Duplicate dates
    def test_duplicate_dates(self):
        with pytest.raises(ValueError):
            n = 365
            times = pd.date_range('2000-01-01', freq='1D', periods=n)
            times = times.append(pd.date_range('2000-12-29', freq='1D', periods=n))
            da = xr.DataArray(np.arange(2*n), [('time', times)])
            tg_mean(da)


def test_missing_any_fill():
    n = 66
    times = pd.date_range('2001-12-30', freq='1D', periods=n)
    da = xr.DataArray(np.arange(n), [('time', times)])
    miss = checks.missing_any_fill(da, 'MS')
    np.testing.assert_array_equal(miss, [True, False, False, True])

    n = 378
    times = pd.date_range('2001-12-31', freq='1D', periods=n)
    da = xr.DataArray(np.arange(n), [('time', times)])
    miss = checks.missing_any_fill(da, 'YS')
    np.testing.assert_array_equal(miss, [True, False, True])

    miss = checks.missing_any_fill(da, 'Q-NOV')
    np.testing.assert_array_equal(miss, [True, False, False, False, True])
