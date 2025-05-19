from app.handlers.analytics.analytics import router as analytics_router
from app.handlers.auth.auth import router as auth_router
from app.handlers.core.core import router as core_router

routers = [analytics_router,
           core_router,
           auth_router,
           ]
