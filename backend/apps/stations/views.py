from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models.functions import TruncDate
from django.db.models import Count

class AdminOverviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        today = timezone.now().date()

        # Compter le nombre d’inscriptions pour chaque jour des 7 derniers jours
        registrations_by_day = (
            User.objects
            .filter(date_joined__date__gte=today - timezone.timedelta(days=6))
            .annotate(day=TruncDate('date_joined'))
            .values('day')
            .annotate(count=Count('id'))
            .order_by('day')
        )

        # Créer une liste de 7 entiers pour le graphique
        day_counts = {item['day']: item['count'] for item in registrations_by_day}
        weekly_counts = []
        for i in range(6, -1, -1):
            day = today - timezone.timedelta(days=i)
            weekly_counts.append(day_counts.get(day, 0))

        # Récupérer d'autres stats si nécessaire
        total_users = User.objects.count()
        admins = User.objects.filter(role__name='admin').count()
        citizens = User.objects.filter(role__name='citizen').count()
        active_users = User.objects.filter(is_active=True).count()
        inactive_users = User.objects.filter(is_active=False).count()

        last_users = User.objects.order_by('-date_joined').values(
            'id', 'username', 'email', 'date_joined'
        )[:5]

        return Response({
            "total_users": total_users,
            "admins": admins,
            "citizens": citizens,
            "active_users": active_users,
            "inactive_users": inactive_users,
            "weekly_registrations": weekly_counts,
            "last_users": list(last_users),
        })
