from typing import Any
from django.shortcuts import get_object_or_404

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .charts import (
    prepare_daily_work_percent_by_caregiver_role_and_type_chart,
    prepare_work_by_caregiver_role_and_type_charts,
    prepare_work_by_caregiver_role_chart,
    prepare_work_by_type_chart,
)

from .models import Home


class HomeListView(ListView):
    model = Home
    context_object_name = "homes"


class HomeDetailView(DetailView):
    model = Home
    context_object_name = "home"

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        url_uuid = self.kwargs.get("url_uuid")  # Get the url_uuid from the URL

        if url_uuid is not None:
            queryset = queryset.filter(
                url_uuid=url_uuid,
            )  # Filter the queryset based on url_uuid

        obj = get_object_or_404(
            queryset,
        )  # Get the object or return a 404 error if not found

        return obj

    def prepare_charts(self, context):
        """Prepare charts and add them to the template context."""
        home = context["home"]

        context["work_by_type_chart"] = prepare_work_by_type_chart(home)

        context["work_by_caregiver_role_chart"] = prepare_work_by_caregiver_role_chart(
            home,
        )

        context[
            "daily_work_percent_by_caregiver_role_and_type_chart"
        ] = prepare_daily_work_percent_by_caregiver_role_and_type_chart(home)

        context = prepare_work_by_caregiver_role_and_type_charts(context)

        return context

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        home = context["home"]

        # Check if work has been recorded
        # by selecting one record
        context["work_has_been_recorded"] = home.work_performed.exists()

        # Only prepare charts if work has been recorded
        if context["work_has_been_recorded"]:
            context = self.prepare_charts(context)

        return context
