from django.conf import settings
from django.db.models import Prefetch
from django.db.models.functions import Now

from config.celery import app
from libs.notifications.email import DefaultEmailNotification

from . import models


@app.task(task_ignore_result=True)
def check_lots_ended():
    """Check if any lots need to be closed and close them."""
    bids_queryset = models.Bid.objects.select_related("user").order_by(
        "-created",
    )
    lots_queryset = models.Lot.objects.prefetch_related(
        Prefetch("bids", queryset=bids_queryset),
    )
    expired_lots = lots_queryset.select_related("user").filter(
        status__exact=models.Lot.Status.IN_PROCCESS,
        end_date__lte=Now(),
    )
    for lot in expired_lots:
        owner = lot.user
        if not lot.bids.exists():
            send_notification_closed_lot.delay(owner, lot)
            continue
        winner = lot.bids.first().user
        send_notification_sold_lot.delay(owner, winner, lot)
    expired_lots.update(status=models.Lot.Status.FINISHED)


@app.task(task_ignore_result=True)
def send_notification_sold_lot(owner, winner, lot):
    """Send notification to owner and winner of sold lot."""
    notification = DefaultEmailNotification(
        subject=f"Lot {lot.name} was selled!",
        recipient_list=(owner, winner),
        template="lots/emails/lot_sold.html",
        app_url=settings.FRONTEND_URL,
        app_label=settings.APP_LABEL,
        lot_name=lot.name,
        lot_id=lot.pk,
    )
    notification.send()


@app.task(task_ignore_result=True)
def send_notification_closed_lot(owner, lot):
    """Send notification to owner of closed lot."""
    notification = DefaultEmailNotification(
        subject=f"Lot {lot.name} was closed!",
        recipient_list=(owner, ),
        template="lots/emails/lot_closed.html",
        app_url=settings.FRONTEND_URL,
        app_label=settings.APP_LABEL,
        lot_name=lot.name,
        lot_id=lot.pk,
    )
    notification.send()
