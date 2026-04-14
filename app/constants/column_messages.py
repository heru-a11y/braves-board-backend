class SuccessMessage:
    COLUMN_CREATED = "Column created successfully"
    COLUMN_UPDATED = "Column updated successfully"
    COLUMN_DELETED = "Column deleted successfully"
    COLUMN_REORDERED = "Column reordered successfully"
    COLUMNS_FETCHED = "Columns fetched successfully"
    COLUMN_FETCHED = "Column fetched successfully"

    BOARD_FETCHED = "Boards fetched successfully"
    BOARD_CREATED = "Board created successfully"

class ErrorMessage:
    NOT_FOUND = "Data not found"
    COLUMN_NOT_FOUND = "Column not found"
    BOARD_NOT_FOUND = "Board not found"

    INVALID_POSITION = "Invalid position"
    UNAUTHORIZED = "Unauthorized access"
    FORBIDDEN = "Forbidden action"

class ValidationMessage:
    TITLE_REQUIRED = "Title is required"
    INVALID_UUID = "Invalid UUID format"