import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'racing_project.settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
django.setup()

from django.test import TestCase, Client
from races.models import Race, Participant, Bet
from django.utils import timezone
from datetime import timedelta
import json


class RaceModelTest(TestCase):
    def setUp(self):
        self.race = Race.objects.create(
            name='Test Dog Race',
            race_type='dog',
            status='upcoming',
            start_time=timezone.now() + timedelta(hours=1),
            track='Test Track',
            distance='520m',
            prize_pool=5000
        )

    def test_race_creation(self):
        self.assertEqual(self.race.name, 'Test Dog Race')
        self.assertEqual(self.race.race_type, 'dog')
        self.assertEqual(self.race.status, 'upcoming')

    def test_race_str(self):
        self.assertIn('Test Dog Race', str(self.race))


class ParticipantModelTest(TestCase):
    def setUp(self):
        self.race = Race.objects.create(
            name='Test Race',
            race_type='horse',
            status='live',
            start_time=timezone.now(),
            track='Royal Ascot',
            distance='1600m',
            prize_pool=10000
        )
        self.participant = Participant.objects.create(
            race=self.race,
            name='Thunder Bolt',
            number=1,
            odds=2.50,
            trainer='John Smith',
            age=4,
            form='1-1-2-1'
        )

    def test_participant_creation(self):
        self.assertEqual(self.participant.name, 'Thunder Bolt')
        self.assertEqual(float(self.participant.odds), 2.50)

    def test_participant_str(self):
        self.assertIn('Thunder Bolt', str(self.participant))


class BetModelTest(TestCase):
    def setUp(self):
        self.race = Race.objects.create(
            name='Live Race',
            race_type='dog',
            status='live',
            start_time=timezone.now(),
            track='Track',
            distance='440m',
            prize_pool=3000
        )
        self.participant = Participant.objects.create(
            race=self.race, name='Fast Dog', number=1, odds=3.00
        )

    def test_bet_potential_winnings(self):
        bet = Bet.objects.create(
            participant=self.participant,
            race=self.race,
            bettor_name='Alice',
            amount=100,
            bet_type='win',
            odds_at_bet=self.participant.odds
        )
        self.assertEqual(float(bet.potential_winnings), 300.0)


class RaceAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.race = Race.objects.create(
            name='API Test Race',
            race_type='horse',
            status='upcoming',
            start_time=timezone.now() + timedelta(hours=1),
            track='Epsom',
            distance='2400m',
            prize_pool=20000
        )
        Participant.objects.create(race=self.race, name='Horse A', number=1, odds=2.00)
        Participant.objects.create(race=self.race, name='Horse B', number=2, odds=4.00)

    def test_races_list(self):
        res = self.client.get('/api/races/')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        self.assertIn('results', data)

    def test_race_detail(self):
        res = self.client.get(f'/api/races/{self.race.id}/')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        self.assertEqual(data['name'], 'API Test Race')
        self.assertEqual(len(data['participants']), 2)

    def test_race_filter_by_type(self):
        Race.objects.create(
            name='Dog Race', race_type='dog', status='upcoming',
            start_time=timezone.now() + timedelta(hours=2),
            track='Track', distance='500m', prize_pool=1000
        )
        res = self.client.get('/api/races/?type=horse')
        data = json.loads(res.content)
        results = data.get('results', data)
        for r in results:
            self.assertEqual(r['race_type'], 'horse')

    def test_stats_endpoint(self):
        res = self.client.get('/api/races/stats/')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        self.assertIn('total_races', data)
        self.assertIn('live_races', data)

    def test_place_bet(self):
        participant = Participant.objects.filter(race=self.race).first()
        Race.objects.filter(id=self.race.id).update(status='live')
        res = self.client.post('/api/bets/', {
            'participant': participant.id,
            'amount': 50,
            'bet_type': 'win',
            'bettor_name': 'Tester'
        }, content_type='application/json')
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.content)
        self.assertEqual(float(data['amount']), 50.0)
