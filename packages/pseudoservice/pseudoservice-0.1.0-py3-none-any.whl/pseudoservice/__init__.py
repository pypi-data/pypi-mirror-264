try:
    from main import Launcher
except ImportError:
    from .main import Launcher

launcher = Launcher
