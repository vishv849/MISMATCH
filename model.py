from app import db
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime

user_interests = Table('UserInterests', db.metadata,
    Column('UserID', Integer, ForeignKey('users.UserID'), primary_key=True),
    Column('InterestID', Integer, ForeignKey('interests.InterestID'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'
    UserID = Column(Integer, primary_key=True)
    SomaiyaEmail = Column(String(255), unique=True, nullable=False)
    InstagramHandle = Column(String(255))
    PhoneNumber = Column(String(20))
    Department = Column(String(255))
    AboutYou = Column(Text)
    ProfilePhoto = Column(String(255))
    RegistrationDate = Column(DateTime, default=datetime.utcnow)
    LastLogin = Column(DateTime)
    password = Column(String(255)) #added password

    interests = relationship("Interest", secondary=user_interests, back_populates="users")
    messages_sent = relationship("Message", foreign_keys='Message.SenderID', back_populates="sender")
    messages_received = relationship("Message", foreign_keys='Message.ReceiverID', back_populates="receiver")
    reports_submitted = relationship("Report", foreign_keys='Report.ReporterID', back_populates="reporter")
    reports_received = relationship("Report", foreign_keys='Report.ReportedUserID', back_populates="reported_user")
    matches_user1 = relationship("Match", foreign_keys='Match.User1ID', back_populates="user1")
    matches_user2 = relationship("Match", foreign_keys='Match.User2ID', back_populates="user2")

    def __repr__(self):
        return f'<User {self.SomaiyaEmail}>'

class Interest(db.Model):
    __tablename__ = 'interests'
    InterestID = Column(Integer, primary_key=True)
    InterestName = Column(String(255), unique=True, nullable=False)

    users = relationship("User", secondary=user_interests, back_populates="interests")

    def __repr__(self):
        return f'<Interest {self.InterestName}>'

class Match(db.Model):
    __tablename__ = 'matches'
    MatchID = Column(Integer, primary_key=True)
    User1ID = Column(Integer, ForeignKey('users.UserID'), nullable=False)
    User2ID = Column(Integer, ForeignKey('users.UserID'), nullable=False)
    MatchDate = Column(DateTime, default=datetime.utcnow)
    Status = Column(Enum('Pending', 'Accepted', 'Rejected', 'Blocked'), default='Pending')

    user1 = relationship("User", foreign_keys=[User1ID], back_populates="matches_user1")
    user2 = relationship("User", foreign_keys=[User2ID], back_populates="matches_user2")

    def __repr__(self):
        return f'<Match {self.User1ID} - {self.User2ID}>'

class Message(db.Model):
    __tablename__ = 'messages'
    MessageID = Column(Integer, primary_key=True)
    SenderID = Column(Integer, ForeignKey('users.UserID'), nullable=False)
    ReceiverID = Column(Integer, ForeignKey('users.UserID'), nullable=False)
    MessageText = Column(Text)
    Timestamp = Column(DateTime, default=datetime.utcnow)

    sender = relationship("User", foreign_keys=[SenderID], back_populates="messages_sent")
    receiver = relationship("User", foreign_keys=[ReceiverID], back_populates="messages_received")

    def __repr__(self):
        return f'<Message from {self.SenderID} to {self.ReceiverID}>'

class Report(db.Model):
    __tablename__ = 'reports'
    ReportID = Column(Integer, primary_key=True)
    ReporterID = Column(Integer, ForeignKey('users.UserID'), nullable=False)
    ReportedUserID = Column(Integer, ForeignKey('users.UserID'), nullable=False)
    ReportReason = Column(Text)
    ReportDate = Column(DateTime, default=datetime.utcnow)
    Status = Column(Enum('Pending', 'Resolved'), default='Pending')

    reporter = relationship("User", foreign_keys=[ReporterID], back_populates="reports_submitted")
    reported_user = relationship("User", foreign_keys=[ReportedUserID], back_populates="reports_received")

    def __repr__(self):
        return f'<Report by {self.ReporterID} against {self.ReportedUserID}>'

class ContactForm(db.Model):
    __tablename__ = 'contactforms'
    ContactID = Column(Integer, primary_key=True)
    Name = Column(String(255))
    SomaiyaEmail = Column(String(255))
    Subject = Column(String(255))
    Message = Column(Text)
    SubmissionDate = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ContactForm from {self.Name}>'