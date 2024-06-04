# data.py
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker
from faker import Faker
import random
import os
import shutil
import pandas as pd
from datetime import datetime, timedelta

Base = declarative_base()

class Event(Base):
    __tablename__ = 'events'
    ID = Column(Integer, primary_key=True)
    Venue_Name = Column(String)
    Music_Genre = Column(String)
    Zip_Code = Column(String)
    City = Column(String)
    Date = Column(Date)
    Time = Column(String)

music_genres = [
    'Pop', 'Rock', 'Country', 'Jazz', 'Classical', 'R&B', 'Hip Hop', 'Blues', 'Reggae',
    'Electronic', 'Folk', 'Metal', 'Punk', 'Indie', 'Alternative', 'International',
    'Latin', 'Soul', 'Gospel', 'Funk', 'Disco', 'Dance', 'Techno', 'House', 'Trance',
    'Ambient', 'Chillout', 'Instrumental', 'Experimental', 'World', 'New Age',
    'Soundtrack', 'Vocal', 'Easy Listening', 'Acoustic', 'Comedy', 'Children',
    'Holiday', 'Other'
]

# Pre-generate a limited set of cities and zip codes
num_unique_cities = 20
num_unique_zips = 20
fake = Faker()
cities = [fake.city() for _ in range(num_unique_cities)]
zips = [fake.zipcode() for _ in range(num_unique_zips)]

def create_and_populate_database():
    print("Starting database creation...")

    # Check if the directory exists
    if os.path.exists('data'):
        shutil.rmtree('data')
    
    # Now create the directory
    os.makedirs('data')
    
    # Create a SQLite database and a 'events' table
    db_path = 'data/database.db'
    engine = create_engine('sqlite:///' + db_path)
    Base.metadata.create_all(engine)
    
    # Create a Session
    Session = sessionmaker(bind=engine)
    
    # Use a context manager to handle the session
    with Session() as session:
        # Generate 500 samples
        num_samples = 500
        mock_data = [
            Event(
                ID=i+1,
                Venue_Name=fake.company(),
                Music_Genre=random.choice(music_genres),
                Zip_Code=random.choice(zips),
                City=random.choice(cities),
                Date=(
                    datetime.now() + timedelta(days=random.randint(-365*2, 365*2))
                ).date(),
                Time=fake.time()
            ) for i in range(num_samples)
        ]
        
        # Add some mock data
        session.add_all(mock_data)
        session.commit()
    
    print("Mock data committed to the database.")

def load_test_data():
    # Create a SQLAlchemy engine
    engine = create_engine('sqlite:///data/database.db')
    
    # Load data from the 'events' table
    data = pd.read_sql_table('events', engine)
    
    # Convert the 'Date' column to date format without time
    data['Date'] = pd.to_datetime(data['Date']).dt.date
    
    # Reset the index to start from 1
    data.index = data.index + 1
    
    # Return the entire data
    return data

print("Running create_and_populate_database...")
create_and_populate_database()
print("Finished running create_and_populate_database.")

def get_page(data, page_number, page_size):
    start = page_number * page_size
    end = start + page_size
    return data.iloc[start:end]