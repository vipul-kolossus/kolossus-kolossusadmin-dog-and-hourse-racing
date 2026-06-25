from django.contrib import admin
from .models import Race, Participant, Bet


class ParticipantInline(admin.TabularInline):
    model = Participant
    extra = 0


@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'race_type', 'status', 'start_time', 'track']
    list_filter = ['race_type', 'status']
    search_fields = ['name', 'track']
    inlines = [ParticipantInline]


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['number', 'name', 'race', 'odds', 'position']
    list_filter = ['race__race_type', 'race__status']


@admin.register(Bet)
class BetAdmin(admin.ModelAdmin):
    list_display = ['bettor_name', 'participant', 'race', 'amount', 'bet_type', 'status', 'created_at']
    list_filter = ['status', 'bet_type']
    readonly_fields = ['potential_winnings', 'created_at']
