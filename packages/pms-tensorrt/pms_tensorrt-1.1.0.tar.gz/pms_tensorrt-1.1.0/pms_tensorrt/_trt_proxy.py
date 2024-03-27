from pms_tensorrt._const import *
from pms_tensorrt._utils import get_device_count, get_device_list, select_device
from pms_tensorrt._logger import LoguruTRTLogger, SeverityType
import tensorrt as trt
import pycuda.driver as cuda


class TRTProxy:

    def __init__(
        self,
        model_path: str,
        device_id: int,
    ) -> None:
        # init cuda
        cuda.init()

        # check gpu
        device_count = get_device_count()
        assert device_count > 0, f"There is no device to alloc."
        assert (
            device_id < self.num_devices
        ), f"num_devices: {self.num_devices}, device_id={device_id} is not available."

        self._model_path = model_path
        self._device_id = device_id
        self._target_device = get_device_list()[device_id]

        # init
        # import pycuda.autoinit
        self._device = cuda.Device(device_id)
        self._context = self._device.make_context()

        # Create Logger
        self._logger = LoguruTRTLogger()

        # Load TRT runtime and deserialize engine
        with open(model_path, "rb") as f:  # type: ignore
            self._runtime = trt.Runtime(self._logger)
            assert self._runtime
            self._engine = self._runtime.deserialize_cuda_engine(f.read())
            assert self._engine

        # Create exec context
        self._execution_context = self._engine.create_execution_context()
        assert self._execution_context

        # Create Stream
        self._stream = cuda.Stream()

    def __del__(self):
        if self._context is not None:
            self._context.pop()  # destruct context
        else:
            self._logger.log(SeverityType.ERROR, "ERROR, context is none.")

    @property
    def logger(self) -> LoguruTRTLogger:
        return self._logger

    @property
    def target_device(self) -> str:
        return self._target_device

    @property
    def engine(self) -> Any:
        return self._engine

    @property
    def execution_context(self) -> Any:
        return self._execution_context

    @property
    def stream(self) -> Any:
        return self._stream

    @property
    def num_devices(self) -> int:
        return cuda.Device.count()
