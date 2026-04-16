class TimerMessage:
    STARTED = "Timer berhasil dimulai"
    STOPPED = "Timer berhasil dihentikan"
    PING_UPDATED = "Ping berhasil diperbarui"
    CONFIRMED = "Aktivitas berhasil dikonfirmasi"
    AUTO_STOP_NO_ACTIVITY = "Timer otomatis berhenti: tidak ada aktivitas"
    AUTO_STOP_NO_CONFIRM = "Timer otomatis berhenti: tidak ada konfirmasi"

class TimerErrorMessage:
    TASK_NOT_FOUND = "Task tidak ditemukan"
    TIMER_ALREADY_RUNNING = "Timer sudah berjalan"
    TIMER_NOT_RUNNING = "Timer belum berjalan"
    TIMER_STATE_LOST = "State timer hilang"
    TIMER_NOT_ACTIVE = "Timer tidak aktif"
