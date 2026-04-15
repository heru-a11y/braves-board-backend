class SuccessMessage:
    COLUMN_CREATED = "Kolom berhasil dibuat"
    COLUMN_UPDATED = "Kolom berhasil diperbarui"
    COLUMN_DELETED = "Kolom berhasil dihapus"
    COLUMN_REORDERED = "Urutan kolom berhasil diperbarui"
    COLUMNS_FETCHED = "Berhasil mengambil data kolom"
    COLUMN_FETCHED = "Berhasil mengambil data kolom"

    BOARD_FETCHED = "Berhasil mengambil data board"
    BOARD_CREATED = "Board berhasil dibuat"

class ErrorMessage:
    NOT_FOUND = "Data tidak ditemukan"
    COLUMN_NOT_FOUND = "Kolom tidak ditemukan"
    BOARD_NOT_FOUND = "Board tidak ditemukan"

    INVALID_POSITION = "Posisi tidak valid"
    UNAUTHORIZED = "Akses tidak diizinkan"
    FORBIDDEN = "Aksi tidak diperbolehkan"

class ValidationMessage:
    TITLE_REQUIRED = "Judul wajib diisi"
    INVALID_UUID = "Format UUID tidak valid"