from models import session, Role, Audition

# Get all roles
roles = session.query(Role).all()
for role in roles:
    print(f"Role: {role.character_name}, Actors: {role.actors()}")

# Find who was hired for Hamlet
hamlet_role = session.query(Role).filter_by(character_name="Hamlet").first()
if hamlet_role:
    print("\nLead actor for Hamlet:", hamlet_role.lead())
    print("Understudy for Hamlet:", hamlet_role.understudy())

# Hire an actor (Example: Michael Johnson)
audition = session.query(Audition).filter_by(actor="Michael Johnson").first()
if audition:
    audition.call_back()  # Mark as hired
    print("\nMichael Johnson is now hired!")
