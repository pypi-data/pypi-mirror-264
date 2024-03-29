import os
from pynwb import load_namespaces, get_class

# Set path of the namespace.yaml file to the expected install location
ndx_photometry_specpath = os.path.join(
    os.path.dirname(__file__), "spec", "ndx-photometry.namespace.yaml"
)

# If the extension has not been installed yet but we are running directly from
# the git repo
if not os.path.exists(ndx_photometry_specpath):
    ndx_photometry_specpath = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "..",
            "spec",
            "ndx-photometry.namespace.yaml",
        )
    )

# Load the namespace
load_namespaces(ndx_photometry_specpath)

# TODO: import your classes here or define your class using get_class to make
# them accessible at the package level
from .photometry import FibersTable, FluorophoresTable, PhotodetectorsTable, ExcitationSourcesTable, FiberPhotometryResponseSeries
(
    CommandedVoltageSeries,
    DeconvolvedFiberPhotometryResponseSeries,
    MultiCommandedVoltage,
    FiberPhotometry,
) = [
    get_class(x, "ndx-photometry")
    for x in (
        "CommandedVoltageSeries",
        "DeconvolvedFiberPhotometryResponseSeries",
        "MultiCommandedVoltage",
        'FiberPhotometry',
    )
]