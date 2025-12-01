#!/usr/bin/env python3

from models import db, Camper, Activity, Signup
from app import app

def seed_database():
    """Create database tables and seed with test data"""
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Verify tables exist
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"Tables created: {tables}")
        
        # Clear existing data
        db.session.query(Signup).delete()
        db.session.query(Activity).delete()
        db.session.query(Camper).delete()
        db.session.commit()
        
        # Create campers
        campers = [
            Camper(name="Caitlin", age=8),
            Camper(name="Lizzie", age=9),
            Camper(name="Nicholas Martinez", age=12),
            Camper(name="Ashley Delgado", age=11),
            Camper(name="Zoe", age=11),
            Camper(name="some name", age=10)
        ]
        
        for camper in campers:
            db.session.add(camper)
        db.session.commit()
        
        # Create activities
        activities = [
            Activity(name="Archery", difficulty=2),
            Activity(name="Swimming", difficulty=3),
            Activity(name="Swim in the lake.", difficulty=3),
            Activity(name="Hiking by the stream.", difficulty=2),
            Activity(name="Listening to the birds chirp.", difficulty=1),
            Activity(name="Kayaking", difficulty=4),
            Activity(name="Rock Climbing", difficulty=5),
            Activity(name="Nature Walk", difficulty=1)
        ]
        
        for activity in activities:
            db.session.add(activity)
        db.session.commit()
        
        # Create signups
        signups = [
            # Nicholas Martinez signed up for multiple activities
            Signup(camper_id=3, activity_id=4, time=8),  # Hiking by the stream
            Signup(camper_id=3, activity_id=5, time=1),  # Listening to the birds chirp
            
            # Ashley Delgado signed up for swimming
            Signup(camper_id=4, activity_id=3, time=9),  # Swim in the lake
            
            # Caitlin signed up for archery
            Signup(camper_id=1, activity_id=1, time=10), # Archery
            
            # Lizzie signed up for nature walk
            Signup(camper_id=2, activity_id=8, time=11), # Nature Walk
            
            # Zoe signed up for kayaking
            Signup(camper_id=5, activity_id=6, time=14), # Kayaking
        ]
        
        for signup in signups:
            db.session.add(signup)
        db.session.commit()
        
        print("✅ Database seeded successfully!")
        print(f"Created {len(campers)} campers")
        print(f"Created {len(activities)} activities") 
        print(f"Created {len(signups)} signups")
        
        # Print sample data for testing
        print("\n📋 Sample Data for Testing:")
        print("\nCampers:")
        for camper in campers[:3]:
            print(f"  - {camper.name} (age {camper.age})")
        
        print("\nActivities:")
        for activity in activities[:3]:
            print(f"  - {activity.name} (difficulty {activity.difficulty})")
        
        print("\nSignups:")
        for signup in signups[:3]:
            camper = Camper.query.get(signup.camper_id)
            activity = Activity.query.get(signup.activity_id)
            print(f"  - {camper.name} → {activity.name} at {signup.time}:00")

if __name__ == "__main__":
    seed_database()
