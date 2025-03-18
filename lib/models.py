from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, Boolean, create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

# Naming convention for foreign keys
convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

# Base class for SQLAlchemy models
Base = declarative_base(metadata=metadata)

# Database connection (SQLite by default)
engine = create_engine('sqlite:///theater.db')

# Session setup
Session = sessionmaker(bind=engine)
session = Session()

class Audition(Base):
    __tablename__ = 'auditions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    actor = Column(String, nullable=False)
    location = Column(String, nullable=False)
    phone = Column(Integer, nullable=True)  # Phone is optional
    hired = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey('roles.id', ondelete="CASCADE"))  # Removed index=True

    # Relationship to Role
    role = relationship("Role", back_populates="auditions")

    def call_back(self):
        """Marks the audition as hired."""
        self.hired = True
        session.commit()  # Save the change

class Role(Base):
    __tablename__ = 'roles'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    character_name = Column(String, nullable=False)  # Removed unique=True

    # Relationship to Auditions
    auditions = relationship("Audition", back_populates="role", cascade="all, delete-orphan")

    def actors(self):
        """Returns a list of actor names who auditioned for this role."""
        return [audition.actor for audition in session.query(Audition).filter_by(role_id=self.id).all()]

    def locations(self):
        """Returns a list of audition locations for this role."""
        return [audition.location for audition in session.query(Audition).filter_by(role_id=self.id).all()]

    def lead(self):
        """Returns the first hired audition for this role or a message if no one is hired."""
        lead_actor = session.query(Audition).filter_by(role_id=self.id, hired=True).order_by(Audition.id).first()
        return lead_actor.actor if lead_actor else "No actor has been hired for this role"

    def understudy(self):
        """Returns the second hired audition for this role or a message if no understudy is available."""
        hired_auditions = session.query(Audition).filter_by(role_id=self.id, hired=True).order_by(Audition.id).all()
        return hired_auditions[1].actor if len(hired_auditions) > 1 else "No actor has been hired for understudy for this role"

# Create the database tables if they don't exist
Base.metadata.create_all(engine)
