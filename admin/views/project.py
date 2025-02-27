from sqladmin import ModelView

from src.database.models import Project


__all__ = ["ProjectAdminView"]


class ProjectAdminView(ModelView, model=Project):
    icon = "ti ti-folder"

    name = "Проект"
    name_plural = "Проекты"
    column_labels = {
        Project.id: "ID",
        Project.name: "Название",
        Project.type: "Тип",
        Project.created_at: "Дата создания",
        Project.updated_at: "Дата изменения",
        Project.user: "Пользователь",
    }
    column_details_exclude_list = [Project.user_id]

    column_list = [Project.name, Project.type, Project.created_at, Project.updated_at]
    column_sortable_list = [Project.name, Project.created_at]
    column_default_sort = [(Project.created_at, True)]
    column_formatters = {
        Project.created_at: lambda m, _: m.created_at.strftime("%d.%m.%Y %H:%M") if m.created_at else "",
        Project.updated_at: lambda m, _: m.updated_at.strftime("%d.%m.%Y %H:%M") if m.updated_at else "",
    }
    column_formatters_detail = {
        Project.created_at: lambda m, _: m.created_at.strftime("%d.%m.%Y %H:%M") if m.created_at else "",
        Project.updated_at: lambda m, _: m.updated_at.strftime("%d.%m.%Y %H:%M") if m.updated_at else "",
    }
