from sqladmin import ModelView

from src.database.models.user import User


__all__ = ["UserAdminView"]


class UserAdminView(ModelView, model=User):
    icon = "ti ti-user"

    name = "Пользователь"
    name_plural = "Пользователи"
    column_labels = {
        User.id: "ID",
        User.email: "Email",
        User.password_hash: "Пароль",
        User.created_at: "Дата создания",
        User.updated_at: "Дата изменения",
        User.is_deleted: "Удален",
        User.deleted_at: "Дата удаления",
        User.projects: "Проекты",
    }

    column_list = [User.email, User.created_at, User.updated_at, User.is_deleted]
    column_sortable_list = [User.email, User.created_at]
    column_default_sort = [(User.created_at, True)]
    column_formatters = {
        User.created_at: lambda m, _: m.created_at.strftime("%d.%m.%Y %H:%M") if m.created_at else "",
        User.updated_at: lambda m, _: m.updated_at.strftime("%d.%m.%Y %H:%M") if m.updated_at else "",
    }
    column_formatters_detail = {
        User.created_at: lambda m, _: m.created_at.strftime("%d.%m.%Y %H:%M") if m.created_at else "",
        User.updated_at: lambda m, _: m.updated_at.strftime("%d.%m.%Y %H:%M") if m.updated_at else "",
    }
