from rest_framework import serializers
from .models import Race, Participant, Bet


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ['id', 'name', 'number', 'odds', 'trainer', 'jockey', 'age', 'weight', 'form', 'position']


class RaceSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True, read_only=True)
    participant_count = serializers.SerializerMethodField()

    class Meta:
        model = Race
        fields = ['id', 'name', 'race_type', 'status', 'start_time', 'track', 'distance', 'prize_pool', 'participants', 'participant_count', 'created_at']

    def get_participant_count(self, obj):
        return obj.participants.count()


class RaceListSerializer(serializers.ModelSerializer):
    participant_count = serializers.SerializerMethodField()

    class Meta:
        model = Race
        fields = ['id', 'name', 'race_type', 'status', 'start_time', 'track', 'distance', 'prize_pool', 'participant_count']

    def get_participant_count(self, obj):
        return obj.participants.count()


class BetSerializer(serializers.ModelSerializer):
    participant_name = serializers.CharField(source='participant.name', read_only=True)
    race_name = serializers.CharField(source='race.name', read_only=True)

    class Meta:
        model = Bet
        fields = ['id', 'participant', 'race', 'bettor_name', 'amount', 'bet_type', 'odds_at_bet', 'potential_winnings', 'status', 'created_at', 'participant_name', 'race_name']
        read_only_fields = ['potential_winnings', 'status', 'created_at']

    def create(self, validated_data):
        participant = validated_data['participant']
        validated_data['odds_at_bet'] = participant.odds
        validated_data['race'] = participant.race
        return super().create(validated_data)
