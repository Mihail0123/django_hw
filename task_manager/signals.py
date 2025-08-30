from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from .models import Task


@receiver(pre_save, sender=Task)
def cache_old_status(sender, instance: Task, **kwargs):
    """
    Перед сохранением запоминаем старый статус,
    чтобы потом в post_save понять - был ли реальный переход.
    """
    if not instance.pk:
        instance._old_status = None
        return
    try:
        old = Task.objects.get(pk=instance.pk)
        instance._old_status = old.status
    except Task.DoesNotExist:
        instance._old_status = None


@receiver(post_save, sender=Task)
def notify_on_status_change(sender, instance: Task, created: bool, **kwargs):
    """
    После сохранения:
      - пропускаем создание (в ДЗ нужны именно переходы статуса/закрытие);
      - если статус изменился - шлем письмо владельцу;
      - если новый статус DONE - формулируем письмо как 'задача закрыта'.
    """
    if created:
        return

    old_status = getattr(instance, "_old_status", None)
    new_status = instance.status

    # ничего не отправляем, если статус не менялся (чтобы не спамить при повторных сохранениях)
    if old_status == new_status:
        return

    email = getattr(instance.owner, "email", "") or ""
    if not email:
        return  # у владельца нет email - просто молча выходим

    # тема/текст письма
    if new_status == "DONE":
        subject = f"Задача «{instance.title}» закрыта"
        message = f"Ваша задача «{instance.title}» переведена в статус DONE (закрыта)."
    else:
        subject = f"Статус задачи «{instance.title}» изменён"
        message = f"Статус изменился: {old_status or '—'} → {new_status}"

    send_mail(
        subject,
        message,
        getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@task-manager.local"),
        [email],
        fail_silently=True,
    )


@receiver(post_delete, sender=Task)
def notify_on_delete(sender, instance: Task, **kwargs):
    """
    Дополнительно: уведомление при удалении задачи.
    Если по формулировке 'закрытие' = удаление — письмо тоже придёт.
    """
    email = getattr(instance.owner, "email", "") or ""
    if not email:
        return

    subject = f"Задача «{instance.title}» удалена"
    message = f"Задача «{instance.title}» была удалена."
    send_mail(
        subject,
        message,
        getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@task-manager.local"),
        [email],
        fail_silently=True,
    )