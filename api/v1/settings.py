from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Any

router = APIRouter(
    prefix="/settings",
    tags=["settings"],
    responses={404: {"description": "Not found"}},
)


class SettingItem(BaseModel):
    key: str
    label: str
    value: Any
    type: str  # "string", "boolean", "number", "select", etc.
    description: str
    editable: bool
    options: List[str] | None = None  # for select-type
    model_config = ConfigDict(from_attributes=True)


# Static, in-memory settings —— intentionally minimal & frontend-consumable
# Reserved for future extension hooks (e.g., reload config, persist to DB, integrate with vault)
STATIC_SETTINGS: List[SettingItem] = [
    SettingItem(
        key="theme",
        label="UI Theme",
        value="light",
        type="select",
        description="Preferred interface appearance",
        editable=True,
        options=["light", "dark", "auto"],
    ),
    SettingItem(
        key="auto_sync",
        label="Auto-Sync Tasks",
        value=True,
        type="boolean",
        description="Enable periodic background sync with remote sources",
        editable=True,
    ),
    SettingItem(
        key="default_status",
        label="Default Task Status",
        value="pending",
        type="string",
        description="Initial status assigned to newly created tasks",
        editable=True,
    ),
    SettingItem(
        key="search_debounce_ms",
        label="Search Debounce (ms)",
        value=300,
        type="number",
        description="Delay before triggering search as user types",
        editable=True,
    ),
    SettingItem(
        key="version",
        label="Platform Version",
        value="0.1.0",
        type="string",
        description="Current build identifier",
        editable=False,
    ),
    SettingItem(
        key="scheme_id",
        label="Configuration Scheme ID",
        value="PROMPT-F78CD1-000083",
        type="string",
        description="Immutable identifier for this configuration variant",
        editable=False,
    ),
]


@router.get("")
def get_settings() -> Dict[str, List[SettingItem]]:
    """
    Returns static, frontend-friendly list of configurable settings.
    Designed for /settings page UI — no side effects, no persistence.
    Reserved for future integration: config reload, DB-backed values, or external secret injection.
    """
    return {"items": STATIC_SETTINGS}
