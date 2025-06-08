from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Fornada, Inscricao

@receiver(post_save, sender=Fornada)
def notificar_usuarios(sender, instance, created, **kwargs):
    if created:
        inscricoes = Inscricao.objects.filter(padaria=instance.padaria)
        for insc in inscricoes:
            print(f'[NOTIFICAÇÃO] Enviar para {insc.usuario.email}: Nova fornada em {instance.padaria.nome}: {instance.descricao}')