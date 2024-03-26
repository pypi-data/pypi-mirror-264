from typing import TYPE_CHECKING

from langflow_base.services.factory import ServiceFactory
from langflow_base.services.session.service import SessionService

if TYPE_CHECKING:
    from langflow_base.services.cache.service import CacheService


class SessionServiceFactory(ServiceFactory):
    def __init__(self):
        super().__init__(SessionService)

    def create(self, cache_service: "CacheService"):
        return SessionService(cache_service)
