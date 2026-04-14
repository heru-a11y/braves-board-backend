class BoardMessage:
    CREATED = "Board berhasil dibuat"
    UPDATED = "Board berhasil diperbarui"
    DELETED = "Board berhasil dihapus"

    NOT_FOUND = "Papan tidak ditemukan"
    TITLE_REQUIRED = "Judul papan wajib diisi"
    INVALID_UPDATE = "Data yang diperbarui tidak valid"

class BoardResponseMessage:
    SUCCESS_GET_ALL = "Berhasil mengambil semua board"
    SUCCESS_GET_DETAIL = "Berhasil mengambil detail board"
    SUCCESS_CREATE = "Berhasil membuat board"
    SUCCESS_UPDATE = "Berhasil memperbarui board"
    SUCCESS_DELETE = "Berhasil menghapus board"