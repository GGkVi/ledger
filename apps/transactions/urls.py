from django.urls import path

from apps.transactions import views

urlpatterns = [
    path(
        "transaction/<int:account_id>/list",
        views.TransactionListView.as_view(),
        name="transaction_list",
    ),
    path(
        "transaction/<int:account_id>/create",
        views.TransactionCreateView.as_view(),
        name="transaction_Create",
    ),
    path(
        "transaction/<int:id>/update/",
        views.TransactionUpdateView.as_view(),
        name="transaction_update",
    ),
    path(
        "transaction/<int:id>/delete",
        views.TransactionDeleteView.as_view(),
        name="transaction_delete",
    ),
]
