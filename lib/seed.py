from models import Base, engine, Session, Role, Audition

# Create a new session
session = Session()

# Clear existing data (optional, to avoid duplicates)
session.query(Audition).delete()
session.query(Role).delete()
session.commit()

# Insert roles
roles = [
    Role(character_name="Hamlet"),
    Role(character_name="Ophelia"),
    Role(character_name="Macbeth"),
    Role(character_name="Lady Macbeth"),
]

session.add_all(roles)
session.commit()  # Save roles to get their IDs

#  Insert auditions
auditions = [
    Audition(actor="John Elton", location="New York", phone=123456789, hired=False, role_id=roles[0].id),
    Audition(actor="Jane Smith", location="Los Angeles", phone=987654321, hired=True, role_id=roles[0].id),
    Audition(actor="Michael Johnson", location="Chicago", phone=555123456, hired=False, role_id=roles[1].id),
    Audition(actor="Emily Davis", location="Boston", phone=444987654, hired=True, role_id=roles[1].id),
    Audition(actor="Chris Brown", location="Miami", phone=333555777, hired=True, role_id=roles[2].id),
    Audition(actor="Sophia Lee", location="Seattle", phone=222333444, hired=False, role_id=roles[3].id),
]

session.add_all(auditions)
session.commit()  # Save all auditions

print("Database successfully seeded!")

#  Close session
session.close()
