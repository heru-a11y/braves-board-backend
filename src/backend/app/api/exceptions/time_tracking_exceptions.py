from fastapi import status
from app.api.exceptions.base_exceptions import CustomException


class TimerAlreadyRunningException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Timer sudah berjalan pada tugas ini"
        )


class TimerNotRunningException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Timer tidak sedang berjalan pada tugas ini"
        )


class TimerStateLostException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Data sesi timer hilang atau tidak sinkron"
        )


class TimerNotActiveException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Tidak ada sesi timer yang aktif"
        )