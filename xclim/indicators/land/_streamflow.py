"""Streamflow indicator definitions."""

from __future__ import annotations

from xclim.core.cfchecks import check_valid
from xclim.core.indicator import (
    ReducingIndicator,
    ResamplingIndicator,
)
from xclim.core.units import declare_units
from xclim.indices import (
    base_flow_index,
    flow_index,
    generic,
    high_flow_frequency,
    low_flow_frequency,
    rb_flashiness_index,
)

__all__ = [
    "base_flow_index",
    "doy_strfmax",
    "doy_strfmin",
    "flow_index",
    "high_flow_frequency",
    "low_flow_frequency",
    "rb_flashiness_index",
]


class Streamflow(ResamplingIndicator):
    """Streamflow class."""

    context = "hydro"
    src_freq = "D"
    keywords = "streamflow hydrology"

    # TODO: TJS: The signature of this method seems wrong. Should it be `def cfcheck(cls, q):` or something else? Is it a static method?
    @staticmethod
    def cfcheck(strf):
        check_valid(strf, "standard_name", "water_volume_transport_in_river_channel")


base_flow_index = Streamflow(
    title="Base flow index",
    identifier="base_flow_index",
    units="",
    long_name="Base flow index",
    description="Minimum of the 7-day moving average flow divided by the mean flow.",
    abstract="Minimum of the 7-day moving average flow divided by the mean flow.",
    compute=base_flow_index,
)


rb_flashiness_index = Streamflow(
    title="Richards-Baker Flashiness Index",
    identifier="rb_flashiness_index",
    units="",
    var_name="rbi",
    long_name="Richards-Baker Flashiness Index",
    description="{freq} of Richards-Baker Index, an index measuring the flashiness of flow.",
    abstract="Measurement of flow oscillations relative to average flow, "
    "quantifying the frequency and speed of flow changes.",
    compute=rb_flashiness_index,
)


doy_strfmax = Streamflow(
    title="Day of year of the maximum streamflow",
    identifier="doy_qmax",
    var_name="strf{indexer}_doy_strfmax",
    long_name="Day of the year of the maximum streamflow over {indexer}",
    description="Day of the year of the maximum streamflow over {indexer}.",
    units="",
    compute=declare_units(da="[discharge]")(generic.select_resample_op),
    parameters={"op": generic.doymax, "out_units": None},
)


doy_strfmin = Streamflow(
    title="Day of year of the minimum streamflow",
    identifier="doy_strfmin",
    var_name="strf{indexer}_doy_strfmin",
    long_name="Day of the year of the minimum streamflow over {indexer}",
    description="Day of the year of the minimum streamflow over {indexer}.",
    units="",
    compute=declare_units(da="[discharge]")(generic.select_resample_op),
    parameters={"op": generic.doymin, "out_units": None},
)

flow_index = ReducingIndicator(
    realm="land",
    context="hydro",
    title="Flow index",
    identifier="flow_index",
    var_name="strf_flow_index",
    long_name="Flow index",
    description="{p}th percentile normalized by the median flow.",
    units="1",
    compute=flow_index,
)


high_flow_frequency = Streamflow(
    title="High flow frequency",
    identifier="high_flow_frequency",
    var_name="strf_high_flow_frequency",
    long_name="High flow frequency",
    description="{freq} frequency of flows greater than {threshold_factor} times the median flow.",
    units="days",
    compute=high_flow_frequency,
)


low_flow_frequency = Streamflow(
    title="Low flow frequency",
    identifier="low_flow_frequency",
    var_name="strf_low_flow_frequency",
    long_name="Low flow frequency",
    description="{freq} frequency of flows smaller than a fraction ({threshold_factor}) of the mean flow.",
    units="days",
    compute=low_flow_frequency,
)
