from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Count
from .models import Race, Participant, Bet
from .serializers import RaceSerializer, RaceListSerializer, ParticipantSerializer, BetSerializer


class RaceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Race.objects.all().prefetch_related('participants')

    def get_serializer_class(self):
        if self.action == 'list':
            return RaceListSerializer
        return RaceSerializer

    def get_queryset(self):
        qs = Race.objects.all().prefetch_related('participants')
        race_type = self.request.query_params.get('type')
        status_filter = self.request.query_params.get('status')
        if race_type:
            qs = qs.filter(race_type=race_type)
        if status_filter:
            qs = qs.filter(status=status_filter)
        return qs

    @action(detail=False, methods=['get'])
    def stats(self, request):
        total_races = Race.objects.count()
        live_races = Race.objects.filter(status='live').count()
        total_bets = Bet.objects.count()
        total_wagered = Bet.objects.aggregate(total=Sum('amount'))['total'] or 0
        return Response({
            'total_races': total_races,
            'live_races': live_races,
            'dog_races': Race.objects.filter(race_type='dog').count(),
            'horse_races': Race.objects.filter(race_type='horse').count(),
            'total_bets': total_bets,
            'total_wagered': float(total_wagered),
        })


class BetViewSet(viewsets.ModelViewSet):
    queryset = Bet.objects.all().select_related('participant', 'race')
    serializer_class = BetSerializer
    http_method_names = ['get', 'post', 'head', 'options']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        participant = serializer.validated_data['participant']
        if participant.race.status == 'finished':
            return Response({'error': 'Cannot place bets on finished races.'}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
