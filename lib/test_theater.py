from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Audition, Role

# Create an in-memory SQLite database for testing
engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Test data
role1 = Role(character_name="Hamlet")
session.add(role1)
session.commit()

audition1 = Audition(actor="John Doe", location="Theater A", role=role1)
audition2 = Audition(actor="Jane Smith", location="Theater B", role=role1)
session.add(audition1)
session.add(audition2)
session.commit()

# Test the relationship
assert audition1.role == role1
assert role1.auditions == [audition1, audition2]

# Test the call_back method
audition1.call_back()
assert audition1.hired is True

# Test the lead method
assert role1.lead() == audition1

# Test the understudy method
audition2.call_back()
assert role1.understudy() == audition2

print("All tests passed!")
