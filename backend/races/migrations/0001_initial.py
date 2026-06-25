from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('race_type', models.CharField(choices=[('dog', 'Dog Racing'), ('horse', 'Horse Racing')], max_length=10)),
                ('status', models.CharField(choices=[('upcoming', 'Upcoming'), ('live', 'Live'), ('finished', 'Finished')], default='upcoming', max_length=10)),
                ('start_time', models.DateTimeField()),
                ('track', models.CharField(max_length=200)),
                ('distance', models.CharField(max_length=50)),
                ('prize_pool', models.DecimalField(decimal_places=2, default=5000.0, max_digits=12)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['start_time'],
            },
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('number', models.IntegerField()),
                ('odds', models.DecimalField(decimal_places=2, max_digits=6)),
                ('trainer', models.CharField(blank=True, max_length=100)),
                ('jockey', models.CharField(blank=True, max_length=100)),
                ('age', models.IntegerField(default=3)),
                ('weight', models.CharField(blank=True, max_length=20)),
                ('form', models.CharField(blank=True, help_text='Recent form e.g. 1-2-3-1', max_length=20)),
                ('position', models.IntegerField(blank=True, null=True)),
                ('race', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='races.race')),
            ],
            options={
                'ordering': ['number'],
            },
        ),
        migrations.CreateModel(
            name='Bet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bettor_name', models.CharField(default='Guest', max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('bet_type', models.CharField(choices=[('win', 'Win'), ('place', 'Place'), ('each_way', 'Each Way')], default='win', max_length=10)),
                ('odds_at_bet', models.DecimalField(decimal_places=2, max_digits=6)),
                ('potential_winnings', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('won', 'Won'), ('lost', 'Lost')], default='pending', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bets', to='races.participant')),
                ('race', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bets', to='races.race')),
            ],
        ),
    ]
