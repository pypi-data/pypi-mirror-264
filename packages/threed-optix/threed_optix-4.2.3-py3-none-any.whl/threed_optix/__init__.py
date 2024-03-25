from .client import ThreedOptixAPI, Client
from .analyses import Analysis
from .simulations import Setup
from .parts import Part, Surface, LightSource, Detector
from . import utils
from . import package_utils
from . import optimize
analysis_names = package_utils.vars.ANALYSIS_NAMES

def dev():
    package_utils.vars.API_URL = package_utils.vars.API_URL.replace('3', '5')
def release():
    package_utils.vars.API_URL = package_utils.vars.API_URL.replace('3', '4')
def prod():
    package_utils.vars.API_URL = "https://api.3doptix.com/v1"
