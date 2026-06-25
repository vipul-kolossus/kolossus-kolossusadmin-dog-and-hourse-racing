from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from races.models import Race, Participant
import random


class Command(BaseCommand):
    help = 'Seed initial race data'

    def handle(self, *args, **kwargs):
        Race.objects.all().delete()

        now = timezone.now()

        dog_races_data = [
            {
                'name': 'Sprint Classic - Race 1',
                'track': 'Wentworth Park',
                'distance': '520m',
                'status': 'live',
                'start_time': now - timedelta(minutes=5),
                'prize_pool': 8500,
                'participants': [
                    {'name': 'Thunder Bolt', 'number': 1, 'odds': 2.40, 'form': '1-1-2-1', 'trainer': 'Jack Smith', 'age': 3},
                    {'name': 'Shadow Runner', 'number': 2, 'odds': 3.60, 'form': '2-3-1-2', 'trainer': 'Mary Jones', 'age': 2},
                    {'name': 'Blue Lightning', 'number': 3, 'odds': 5.50, 'form': '3-2-4-3', 'trainer': 'Tom Brown', 'age': 4},
                    {'name': 'Rocket Storm', 'number': 4, 'odds': 7.00, 'form': '4-5-3-2', 'trainer': 'Sue Davis', 'age': 3},
                    {'name': 'Silver Arrow', 'number': 5, 'odds': 4.20, 'form': '2-1-3-4', 'trainer': 'Bill White', 'age': 2},
                    {'name': 'Golden Flash', 'number': 6, 'odds': 9.00, 'form': '5-4-5-5', 'trainer': 'Ann Taylor', 'age': 5},
                ],
            },
            {
                'name': 'Night Sprint - Race 2',
                'track': 'Sandown Park',
                'distance': '440m',
                'status': 'upcoming',
                'start_time': now + timedelta(minutes=20),
                'prize_pool': 6200,
                'participants': [
                    {'name': 'Dark Star', 'number': 1, 'odds': 3.00, 'form': '1-2-1-3', 'trainer': 'Chris Lee', 'age': 3},
                    {'name': 'Midnight Racer', 'number': 2, 'odds': 4.50, 'form': '3-1-2-1', 'trainer': 'Pat Wilson', 'age': 4},
                    {'name': 'Fast Paws', 'number': 3, 'odds': 2.80, 'form': '2-2-1-2', 'trainer': 'Rob Clark', 'age': 2},
                    {'name': 'Storm Chaser', 'number': 4, 'odds': 6.00, 'form': '4-3-3-4', 'trainer': 'Lisa Moore', 'age': 3},
                    {'name': 'Quick Step', 'number': 5, 'odds': 8.50, 'form': '5-4-5-3', 'trainer': 'Dave Hall', 'age': 5},
                    {'name': 'Blaze Runner', 'number': 6, 'odds': 11.00, 'form': '6-6-4-5', 'trainer': 'Emma Young', 'age': 2},
                ],
            },
            {
                'name': 'Championship Final',
                'track': 'Albion Park',
                'distance': '600m',
                'status': 'upcoming',
                'start_time': now + timedelta(hours=1),
                'prize_pool': 15000,
                'participants': [
                    {'name': 'Champion Rex', 'number': 1, 'odds': 1.90, 'form': '1-1-1-2', 'trainer': 'John King', 'age': 3},
                    {'name': 'Speed Demon', 'number': 2, 'odds': 3.20, 'form': '2-1-2-1', 'trainer': 'Sarah Prince', 'age': 4},
                    {'name': 'Flash Gordon', 'number': 3, 'odds': 5.00, 'form': '3-3-1-3', 'trainer': 'Mike Duke', 'age': 3},
                    {'name': 'Lightning Lad', 'number': 4, 'odds': 6.50, 'form': '4-2-3-4', 'trainer': 'Helen Fox', 'age': 2},
                    {'name': 'Nitro Blast', 'number': 5, 'odds': 4.80, 'form': '2-4-2-2', 'trainer': 'Carl Stone', 'age': 3},
                    {'name': 'Turbo Paws', 'number': 6, 'odds': 12.00, 'form': '6-5-6-5', 'trainer': 'Nina Bell', 'age': 4},
                ],
            },
            {
                'name': 'Greyhound Stakes',
                'track': 'Rosehill',
                'distance': '520m',
                'status': 'finished',
                'start_time': now - timedelta(hours=2),
                'prize_pool': 9800,
                'participants': [
                    {'name': 'Swift Wind', 'number': 1, 'odds': 2.50, 'form': '1-2-1-1', 'trainer': 'Alan Grant', 'age': 3, 'position': 1},
                    {'name': 'Rapid Fire', 'number': 2, 'odds': 4.00, 'form': '2-1-3-2', 'trainer': 'Joan Webb', 'age': 4, 'position': 2},
                    {'name': 'Speedy Paws', 'number': 3, 'odds': 5.50, 'form': '3-3-2-3', 'trainer': 'Fred Cole', 'age': 2, 'position': 3},
                    {'name': 'Thunder Dog', 'number': 4, 'odds': 7.50, 'form': '4-4-4-4', 'trainer': 'Kate Ross', 'age': 3, 'position': 4},
                    {'name': 'Star Chase', 'number': 5, 'odds': 3.80, 'form': '2-2-1-3', 'trainer': 'Tom Nash', 'age': 3, 'position': 5},
                    {'name': 'Laser Beam', 'number': 6, 'odds': 9.00, 'form': '5-5-5-5', 'trainer': 'Lucy Park', 'age': 5, 'position': 6},
                ],
            },
        ]

        horse_races_data = [
            {
                'name': 'Gold Cup - Race 1',
                'track': 'Royal Ascot',
                'distance': '1600m',
                'status': 'live',
                'start_time': now - timedelta(minutes=3),
                'prize_pool': 25000,
                'participants': [
                    {'name': 'Royal Thunder', 'number': 1, 'odds': 2.20, 'form': '1-1-2-1', 'jockey': 'J. Smith', 'trainer': 'H. Brown', 'age': 5, 'weight': '58kg'},
                    {'name': 'Golden Gallop', 'number': 2, 'odds': 3.50, 'form': '2-3-1-2', 'jockey': 'P. Davis', 'trainer': 'A. Wilson', 'age': 4, 'weight': '57kg'},
                    {'name': 'Storm Rider', 'number': 3, 'odds': 5.00, 'form': '3-2-3-3', 'jockey': 'M. Jones', 'trainer': 'R. Taylor', 'age': 6, 'weight': '56kg'},
                    {'name': 'Black Diamond', 'number': 4, 'odds': 7.00, 'form': '4-4-2-4', 'jockey': 'T. Clark', 'trainer': 'S. White', 'age': 5, 'weight': '57.5kg'},
                    {'name': 'Silver Star', 'number': 5, 'odds': 4.50, 'form': '2-1-4-2', 'jockey': 'C. Lee', 'trainer': 'D. Moore', 'age': 4, 'weight': '56.5kg'},
                    {'name': 'Wind Dancer', 'number': 6, 'odds': 8.00, 'form': '5-5-5-5', 'jockey': 'B. Hall', 'trainer': 'E. King', 'age': 7, 'weight': '56kg'},
                    {'name': 'Night Fury', 'number': 7, 'odds': 11.00, 'form': '6-6-6-6', 'jockey': 'R. Scott', 'trainer': 'G. Fox', 'age': 3, 'weight': '55kg'},
                    {'name': 'Blazing Trail', 'number': 8, 'odds': 15.00, 'form': '7-7-7-7', 'jockey': 'K. Adams', 'trainer': 'N. Bell', 'age': 6, 'weight': '57kg'},
                ],
            },
            {
                'name': 'Derby Stakes',
                'track': 'Epsom Downs',
                'distance': '2400m',
                'status': 'upcoming',
                'start_time': now + timedelta(minutes=45),
                'prize_pool': 50000,
                'participants': [
                    {'name': 'Gallant Prince', 'number': 1, 'odds': 2.80, 'form': '1-2-1-1', 'jockey': 'F. Dettori', 'trainer': 'J. Gosden', 'age': 3, 'weight': '57kg'},
                    {'name': 'Mighty Eagle', 'number': 2, 'odds': 4.00, 'form': '2-1-2-3', 'jockey': 'R. Hughes', 'trainer': 'B. Hills', 'age': 4, 'weight': '57kg'},
                    {'name': 'Iron Duke', 'number': 3, 'odds': 6.50, 'form': '3-3-3-2', 'jockey': 'A. Munro', 'trainer': 'H. Cecil', 'age': 3, 'weight': '57kg'},
                    {'name': 'Crimson Tide', 'number': 4, 'odds': 3.20, 'form': '1-2-2-1', 'jockey': 'K. Fallon', 'trainer': 'M. Stoute', 'age': 4, 'weight': '57kg'},
                    {'name': 'Desert Storm', 'number': 5, 'odds': 9.00, 'form': '4-4-4-4', 'jockey': 'O. Peslier', 'trainer': 'A. Fabre', 'age': 3, 'weight': '57kg'},
                    {'name': 'Jungle King', 'number': 6, 'odds': 12.00, 'form': '5-5-5-5', 'jockey': 'C. Soumillon', 'trainer': 'A. de Royer-Dupre', 'age': 5, 'weight': '57kg'},
                ],
            },
            {
                'name': 'Champion Hurdle',
                'track': 'Cheltenham',
                'distance': '3200m',
                'status': 'upcoming',
                'start_time': now + timedelta(hours=2),
                'prize_pool': 35000,
                'participants': [
                    {'name': 'Bold Warrior', 'number': 1, 'odds': 3.00, 'form': '1-1-3-1', 'jockey': 'T. Scudamore', 'trainer': 'D. Pipe', 'age': 7, 'weight': '63kg'},
                    {'name': 'Mountain Hawk', 'number': 2, 'odds': 5.50, 'form': '2-3-1-2', 'jockey': 'R. Walsh', 'trainer': 'W. Mullins', 'age': 6, 'weight': '63kg'},
                    {'name': 'Brave Heart', 'number': 3, 'odds': 4.20, 'form': '3-2-2-3', 'jockey': 'A. McCoy', 'trainer': 'M. Pipe', 'age': 8, 'weight': '63kg'},
                    {'name': 'Thunder Cloud', 'number': 4, 'odds': 7.00, 'form': '4-4-4-4', 'jockey': 'B. Geraghty', 'trainer': 'N. Henderson', 'age': 5, 'weight': '63kg'},
                    {'name': 'Swift Arrow', 'number': 5, 'odds': 2.60, 'form': '1-1-1-2', 'jockey': 'R. Johnson', 'trainer': 'P. Nicholls', 'age': 6, 'weight': '63kg'},
                ],
            },
            {
                'name': 'Spring Carnival',
                'track': 'Flemington',
                'distance': '1800m',
                'status': 'finished',
                'start_time': now - timedelta(hours=3),
                'prize_pool': 40000,
                'participants': [
                    {'name': 'Winx Legacy', 'number': 1, 'odds': 1.80, 'form': '1-1-1-1', 'jockey': 'H. Bowman', 'trainer': 'C. Waller', 'age': 5, 'weight': '58kg', 'position': 1},
                    {'name': 'Star Kingdom', 'number': 2, 'odds': 4.50, 'form': '2-2-2-2', 'jockey': 'J. Payne', 'trainer': 'G. Rogerson', 'age': 6, 'weight': '57.5kg', 'position': 2},
                    {'name': 'Ocean Storm', 'number': 3, 'odds': 6.00, 'form': '3-3-3-3', 'jockey': 'D. Oliver', 'trainer': 'L. Freedman', 'age': 4, 'weight': '57kg', 'position': 3},
                    {'name': 'Red Baron', 'number': 4, 'odds': 8.50, 'form': '4-4-4-4', 'jockey': 'G. Boss', 'trainer': 'M. Moroney', 'age': 7, 'weight': '56.5kg', 'position': 4},
                    {'name': 'Lucky Charm', 'number': 5, 'odds': 11.00, 'form': '5-5-5-5', 'jockey': 'S. King', 'trainer': 'B. Ryan', 'age': 3, 'weight': '56kg', 'position': 5},
                ],
            },
        ]

        for race_data in dog_races_data:
            participants = race_data.pop('participants')
            race = Race.objects.create(race_type='dog', **race_data)
            for p in participants:
                Participant.objects.create(race=race, **p)

        for race_data in horse_races_data:
            participants = race_data.pop('participants')
            race = Race.objects.create(race_type='horse', **race_data)
            for p in participants:
                Participant.objects.create(race=race, **p)

        self.stdout.write(self.style.SUCCESS('Successfully seeded race data!'))
