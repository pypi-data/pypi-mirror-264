from contextlib import contextmanager
from typing import TYPE_CHECKING, Generator

from langflow_base.services import ServiceType, service_manager

if TYPE_CHECKING:
    from langflow_base.services.cache.service import BaseCacheService
    from langflow_base.services.chat.service import ChatService
    from langflow_base.services.credentials.service import CredentialService
    from langflow_base.services.database.service import DatabaseService
    from langflow_base.services.monitor.service import MonitorService
    from langflow_base.services.plugins.service import PluginService
    from langflow_base.services.session.service import SessionService
    from langflow_base.services.settings.service import SettingsService
    from langflow_base.services.socket.service import SocketIOService
    from langflow_base.services.storage.service import StorageService
    from langflow_base.services.store.service import StoreService
    from langflow_base.services.task.service import TaskService
    from sqlmodel import Session


def get_socket_service() -> "SocketIOService":
    return service_manager.get(ServiceType.SOCKET_IO_SERVICE)  # type: ignore


def get_storage_service() -> "StorageService":
    return service_manager.get(ServiceType.STORAGE_SERVICE)  # type: ignore


def get_credential_service() -> "CredentialService":
    return service_manager.get(ServiceType.CREDENTIAL_SERVICE)  # type: ignore


def get_plugins_service() -> "PluginService":
    return service_manager.get(ServiceType.PLUGIN_SERVICE)  # type: ignore


def get_settings_service() -> "SettingsService":
    try:
        return service_manager.get(ServiceType.SETTINGS_SERVICE)  # type: ignore
    except ValueError:
        # initialize settings service
        from langflow_base.services.manager import initialize_settings_service

        initialize_settings_service()
        return service_manager.get(ServiceType.SETTINGS_SERVICE)  # type: ignore


def get_db_service() -> "DatabaseService":
    return service_manager.get(ServiceType.DATABASE_SERVICE)  # type: ignore


def get_session() -> Generator["Session", None, None]:
    db_service = get_db_service()
    yield from db_service.get_session()


@contextmanager
def session_scope():
    session = next(get_session())
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def get_cache_service() -> "BaseCacheService":
    return service_manager.get(ServiceType.CACHE_SERVICE)  # type: ignore


def get_session_service() -> "SessionService":
    return service_manager.get(ServiceType.SESSION_SERVICE)  # type: ignore


def get_monitor_service() -> "MonitorService":
    return service_manager.get(ServiceType.MONITOR_SERVICE)  # type: ignore


def get_task_service() -> "TaskService":
    return service_manager.get(ServiceType.TASK_SERVICE)  # type: ignore


def get_chat_service() -> "ChatService":
    return service_manager.get(ServiceType.CHAT_SERVICE)  # type: ignore


def get_store_service() -> "StoreService":
    return service_manager.get(ServiceType.STORE_SERVICE)  # type: ignore
