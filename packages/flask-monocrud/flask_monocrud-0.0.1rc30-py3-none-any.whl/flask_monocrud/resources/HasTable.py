from typing import Any

class HasTable:
    table_polling: bool = False
    table_polling_interval: int = 5

    def get_table(self) -> list[dict[str, Any]]:
        return []

    def get_relations(self) -> list[dict[str, Any]]:
        return []

    def get_table_actions(self) -> list[dict[str, Any]]:
        return []

    def get_table_filters(self) -> list[dict[str, Any]]:
        return []

    def get_table_tabs(self) -> list[dict[str, Any]]:
        return []