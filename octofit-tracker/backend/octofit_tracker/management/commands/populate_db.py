from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from django.conf import settings
from pymongo import MongoClient
from datetime import datetime

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activity, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Connect to MongoDB
        client = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])
        db = client[settings.DATABASES['default']['NAME']]

        # Drop existing collections
        db.users.drop()
        db.teams.drop()
        db.activity.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Create users
        users = [
            {"email": "thundergod@mhigh.edu", "name": "Thor", "age": 1500, "team": "Blue Team"},
            {"email": "metalgeek@mhigh.edu", "name": "Tony Stark", "age": 48, "team": "Gold Team"},
            {"email": "zerocool@mhigh.edu", "name": "Steve Rogers", "age": 101, "team": "Blue Team"},
            {"email": "crashoverride@mhigh.edu", "name": "Natasha Romanoff", "age": 35, "team": "Gold Team"},
            {"email": "sleeptoken@mhigh.edu", "name": "Bruce Banner", "age": 49, "team": "Blue Team"},
        ]
        db.users.insert_many(users)

        # Create teams
        teams = [
            {"name": "Blue Team", "members": [user["email"] for user in users if user["team"] == "Blue Team"]},
            {"name": "Gold Team", "members": [user["email"] for user in users if user["team"] == "Gold Team"]},
        ]
        db.teams.insert_many(teams)

        # Create activities
        activities = [
            {"user": "thundergod@mhigh.edu", "activity_type": "Cycling", "duration": 60, "date": datetime(2025, 4, 8)},
            {"user": "metalgeek@mhigh.edu", "activity_type": "Crossfit", "duration": 120, "date": datetime(2025, 4, 7)},
            {"user": "zerocool@mhigh.edu", "activity_type": "Running", "duration": 90, "date": datetime(2025, 4, 6)},
            {"user": "crashoverride@mhigh.edu", "activity_type": "Strength", "duration": 30, "date": datetime(2025, 4, 5)},
            {"user": "sleeptoken@mhigh.edu", "activity_type": "Swimming", "duration": 75, "date": datetime(2025, 4, 4)},
        ]
        db.activity.insert_many(activities)

        # Create leaderboard entries
        leaderboard = [
            {"team": "Blue Team", "points": 300},
            {"team": "Gold Team", "points": 250},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Create workouts
        workouts = [
            {"name": "Cycling Training", "description": "Training for a road cycling event", "duration": 60},
            {"name": "Crossfit", "description": "Training for a crossfit competition", "duration": 120},
            {"name": "Running Training", "description": "Training for a marathon", "duration": 90},
            {"name": "Strength Training", "description": "Training for strength", "duration": 30},
            {"name": "Swimming Training", "description": "Training for a swimming competition", "duration": 75},
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))
