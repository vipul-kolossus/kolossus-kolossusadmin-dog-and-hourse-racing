from django.db import models
from django.utils import timezone


class Race(models.Model):
    RACE_TYPE_CHOICES = [
        ('dog', 'Dog Racing'),
        ('horse', 'Horse Racing'),
    ]
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('live', 'Live'),
        ('finished', 'Finished'),
    ]

    name = models.CharField(max_length=200)
    race_type = models.CharField(max_length=10, choices=RACE_TYPE_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='upcoming')
    start_time = models.DateTimeField()
    track = models.CharField(max_length=200)
    distance = models.CharField(max_length=50)
    prize_pool = models.DecimalField(max_digits=12, decimal_places=2, default=5000.00)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return f"{self.name} - {self.race_type} - {self.status}"


class Participant(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='participants')
    name = models.CharField(max_length=100)
    number = models.IntegerField()
    odds = models.DecimalField(max_digits=6, decimal_places=2)
    trainer = models.CharField(max_length=100, blank=True)
    jockey = models.CharField(max_length=100, blank=True)
    age = models.IntegerField(default=3)
    weight = models.CharField(max_length=20, blank=True)
    form = models.CharField(max_length=20, blank=True, help_text='Recent form e.g. 1-2-3-1')
    position = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['number']

    def __str__(self):
        return f"#{self.number} {self.name} ({self.race.name})"


class Bet(models.Model):
    BET_TYPE_CHOICES = [
        ('win', 'Win'),
        ('place', 'Place'),
        ('each_way', 'Each Way'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('won', 'Won'),
        ('lost', 'Lost'),
    ]

    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='bets')
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='bets')
    bettor_name = models.CharField(max_length=100, default='Guest')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bet_type = models.CharField(max_length=10, choices=BET_TYPE_CHOICES, default='win')
    odds_at_bet = models.DecimalField(max_digits=6, decimal_places=2)
    potential_winnings = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.potential_winnings = self.amount * self.odds_at_bet
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Bet on {self.participant.name} - {self.amount} ({self.bet_type})"
