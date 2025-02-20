from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from markupsafe import Markup
from sqladmin import ModelView, action
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError

from src.database.models import Feedback


__all__ = ["FeedbackAdminView"]


class FeedbackAdminView(ModelView, model=Feedback):
    icon = "ti ti-message-dots"
    toggle_field = "is_processed"
    name = "Отзыв"
    name_plural = "Отзывы"
    column_labels = {
        Feedback.id: "ID",
        Feedback.user_id: "ID пользователя",
        Feedback.email: "Email",
        Feedback.name: "Название",
        Feedback.comment: "Комментарий",
        Feedback.created_at: "Дата создания",
        Feedback.updated_at: "Дата изменения",
        Feedback.is_processed: "Обработан",
    }
    column_list = [
        Feedback.id,
        Feedback.user_id,
        Feedback.email,
        Feedback.name,
        Feedback.comment,
        Feedback.created_at,
        Feedback.updated_at,
        Feedback.is_processed,
    ]
    column_details_exclude_list = [Feedback.id]
    column_searchable_list = [Feedback.email, Feedback.name]
    column_sortable_list = [Feedback.created_at]
    column_default_sort = [(Feedback.created_at, True)]
    column_formatters = {
        Feedback.created_at: lambda m, _: m.created_at.strftime("%d.%m.%Y %H:%M") if m.created_at else "",
        Feedback.updated_at: lambda m, _: m.updated_at.strftime("%d.%m.%Y %H:%M") if m.updated_at else "",
    }
    column_formatters_detail = {
        Feedback.created_at: lambda m, _: m.created_at.strftime("%d.%m.%Y %H:%M") if m.created_at else "",
        Feedback.updated_at: lambda m, _: m.updated_at.strftime("%d.%m.%Y %H:%M") if m.updated_at else "",
    }

    @action(
        name="activate",
        label="Обработать",
        confirmation_message=Markup(object="Обработать отзыв?"),
        add_in_detail=True,
        add_in_list=True,
    )
    async def activate_objects(self, request: Request):
        pks = request.query_params.get("pks", "").split(",")
        if pks:
            statement = update(self.model).filter(self.model.id.in_(pks)).values(is_processed=True)
            async with self.session_maker(expire_on_commit=False) as session:
                try:
                    await session.execute(statement=statement)
                    await session.commit()
                except IntegrityError:
                    await session.rollback()
                finally:
                    await session.close()
        referer = request.headers.get("Referer")
        if referer:
            return RedirectResponse(referer)
        return RedirectResponse(request.url_for("admin:list", identity=self.identity))

    @action(
        name="deactivate",
        label="Вернуть на обработку",
        confirmation_message=Markup(object="Вернуть отзыв на обработку?"),
        add_in_detail=True,
        add_in_list=True,
    )
    async def deactivate_objects(self, request: Request):
        pks = request.query_params.get("pks", "").split(",")
        if pks:
            statement = update(self.model).filter(self.model.id.in_(pks)).values(is_processed=False)
            async with self.session_maker(expire_on_commit=False) as session:
                try:
                    await session.execute(statement=statement)
                    await session.commit()
                except IntegrityError:
                    await session.rollback()
                finally:
                    await session.close()
        referer = request.headers.get("Referer")
        if referer:
            return RedirectResponse(referer)
        return RedirectResponse(request.url_for("admin:list", identity=self.identity))
