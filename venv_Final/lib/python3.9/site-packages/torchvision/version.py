__version__ = '0.12.0'
git_version = 'c6c1fb6a67627fa1ecdb9aec38728b849a31e36e'
from torchvision.extension import _check_cuda_version
if _check_cuda_version() > 0:
    cuda = _check_cuda_version()
