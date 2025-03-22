'''
This is going to have all of the database tables
so that we can interact with them in the db.
'''
from app import app, db
# from extension_db import db

from sqlalchemy.orm import DeclarativeBase # type: ignore
from sqlalchemy.dialects.postgresql import JSONB # type: ignore

# base class for the image.
class Base(DeclarativeBase):
    pass

# converts the class to a dict for the api.
class AsDictMixin():
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Season(db.Model, AsDictMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, nullable=False)
    is_used = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<Season {self.name}>"

class Game(db.Model, AsDictMixin):
    id = db.Column(db.Integer, primary_key=True)
    season_id = db.Column(db.Integer, db.ForeignKey('season.id'))

    # get the game from the api.
    date = db.Column(db.Date, nullable=True)
    # game type 1 preseason, 2 regular season, 3 postseason
    game_type = db.Column(db.Integer, nullable=True)
    # the relationship
    season = db.relationship('Season', backref='games')

    # this is going to be somewhere to save the shift data, just make a json
    # field to dump this into.
    shift_data = db.Column(JSONB, nullable=True)

    def get_nhl_game_id(self):
        # get the first four chars of the season id (look in the database)
        season = str(self.season_id)[0:4]
        return f"{season}0{int(self.id)}"

    def __repr__(self):
        return f"<Game {self.id}>"

class Player(db.Model, AsDictMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)
    full_name = db.Column(db.String(255), nullable=True)
    position = db.Column(db.String(5), nullable=True)

    def __repr__(self):
        return f"<Player {self.id}>"


class POIU(db.Model, AsDictMixin):
    id=db.Column(db.Float, primary_key=True)
    # situation will need to be calculated from people on ice.
    situation = db.Column(db.String(100), nullable=False)

    # players will be saved in the order of their ids.
    player_one_id = db.Column(db.Integer, nullable=True)
    player_two_id = db.Column(db.Integer, nullable=True)
    player_three_id = db.Column(db.Integer, nullable=True)
    player_four_id = db.Column(db.Integer, nullable=True)
    player_five_id = db.Column(db.Integer, nullable=True)
    player_six_id = db.Column(db.Integer, nullable=True)

    # all players as a json column
    all_players = db.Column(JSONB, nullable=True)

    def __repr__(self):
        return f"<POIU {self.id}>"
    
class playerShiftTrack(db.Model, AsDictMixin):

    id = db.Column(db.Float, primary_key=True)

    game_id = db.Column(db.Integer, nullable=True)
    shift_period = db.Column(db.Integer, nullable=True)

    player_id = db.Column(db.Integer, nullable=True)
    team_id = db.Column(db.Integer, nullable=True)
    shift_number = db.Column(db.Integer, nullable=True)
    
    start_shift_number = db.Column(db.Float, nullable=True)
    end_shift_number = db.Column(db.Float, nullable=True)
    duration_number = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f"<PlayerShiftTrack {self.id}>"

class gameShiftTrack(db.Model, AsDictMixin):

    id = db.Column(db.Float, primary_key=True, autoincrement=True)

    game_id = db.Column(db.Integer, nullable=True)
    shift_period = db.Column(db.Integer, nullable=True)

    player_id_1 = db.Column(db.Integer, nullable=True)
    player_id_2 = db.Column(db.Integer, nullable=True)
    player_id_3 = db.Column(db.Integer, nullable=True)
    player_id_4 = db.Column(db.Integer, nullable=True)
    player_id_5 = db.Column(db.Integer, nullable=True)
    player_id_6 = db.Column(db.Integer, nullable=True)
    team_id = db.Column(db.Integer, nullable=True)
    shift_number = db.Column(db.Integer, nullable=True)
    
    start_shift_number = db.Column(db.Float, nullable=True)
    end_shift_number = db.Column(db.Float, nullable=True)
    duration_number = db.Column(db.Float, nullable=True)
    situation = db.Column(db.String(10), nullable=True)

    def __repr__(self):
        return f"<GameShiftTrack {self.id}>"
    

class Shot(db.Model, AsDictMixin):
    # keys
    shotID = db.Column(db.Float, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))

    # game relationships
    game = db.relationship('Game', backref='shots')

    # relationships that can be made.
    season = db.Column(db.Float, nullable=True)
    shooterPlayerId = db.Column(db.Float, nullable=True)

    # POIU relationships we can foreign key them later.
    shooting_poiu_id = db.Column(db.Integer, nullable=True)
    defending_poiu_id = db.Column(db.Integer, nullable=True)

    # data
    arenaAdjustedShotDistance = db.Column(db.Float, nullable=True)
    arenaAdjustedXCord = db.Column(db.Float, nullable=True)
    arenaAdjustedXCordABS = db.Column(db.Float, nullable=True)
    arenaAdjustedYCord = db.Column(db.Float, nullable=True)
    arenaAdjustedYCordAbs = db.Column(db.Float, nullable=True)
    averageRestDifference = db.Column(db.Float, nullable=True)
    awayEmptyNet = db.Column(db.Float, nullable=True)
    awayPenalty1Length = db.Column(db.Float, nullable=True)
    awayPenalty1TimeLeft = db.Column(db.Float, nullable=True)
    awaySkatersOnIce = db.Column(db.Float, nullable=True)
    awayTeamCode = db.Column(db.String(100), nullable=False)
    awayTeamGoals = db.Column(db.Float, nullable=True)
    defendingTeamAverageTimeOnIce = db.Column(db.Float, nullable=True)
    defendingTeamAverageTimeOnIceOfDefencemen = db.Column(db.Float, nullable=True)
    defendingTeamAverageTimeOnIceOfDefencemenSinceFaceoff = db.Column(db.Float, nullable=True)
    defendingTeamAverageTimeOnIceOfForwards = db.Column(db.Float, nullable=True)
    defendingTeamAverageTimeOnIceOfForwardsSinceFaceoff = db.Column(db.Float, nullable=True)
    defendingTeamAverageTimeOnIceSinceFaceoff = db.Column(db.Float, nullable=True)
    defendingTeamDefencemenOnIce = db.Column(db.Float, nullable=True)
    defendingTeamForwardsOnIce = db.Column(db.Float, nullable=True)
    defendingTeamMaxTimeOnIce = db.Column(db.Float, nullable=True)
    defendingTeamMaxTimeOnIceOfDefencemen = db.Column(db.Float, nullable=True)
    defendingTeamMaxTimeOnIceOfDefencemenSinceFaceoff = db.Column(db.Float, nullable=True)
    defendingTeamMaxTimeOnIceOfForwards = db.Column(db.Float, nullable=True)
    defendingTeamMaxTimeOnIceOfForwardsSinceFaceoff = db.Column(db.Float, nullable=True)
    defendingTeamMaxTimeOnIceSinceFaceoff = db.Column(db.Float, nullable=True)
    defendingTeamMinTimeOnIce = db.Column(db.Float, nullable=True)
    defendingTeamMinTimeOnIceOfDefencemen = db.Column(db.Float, nullable=True)
    defendingTeamMinTimeOnIceOfDefencemenSinceFaceoff = db.Column(db.Float, nullable=True)
    defendingTeamMinTimeOnIceOfForwards = db.Column(db.Float, nullable=True)
    defendingTeamMinTimeOnIceOfForwardsSinceFaceoff = db.Column(db.Float, nullable=True)
    defendingTeamMinTimeOnIceSinceFaceoff = db.Column(db.Float, nullable=True)
    distanceFromLastEvent = db.Column(db.Float, nullable=True)
    event = db.Column(db.String(100), nullable=False)
    goal = db.Column(db.Float, nullable=True)
    goalieIdForShot = db.Column(db.Float, nullable=True)
    goalieNameForShot = db.Column(db.String(100), nullable=False)
    homeEmptyNet = db.Column(db.Float, nullable=True)
    homePenalty1Length = db.Column(db.Float, nullable=True)
    homePenalty1TimeLeft = db.Column(db.Float, nullable=True)
    homeSkatersOnIce = db.Column(db.Float, nullable=True)
    homeTeamCode = db.Column(db.String(100), nullable=False)
    homeTeamGoals = db.Column(db.Float, nullable=True)
    homeTeamWon = db.Column(db.Float, nullable=True)
    id = db.Column(db.Float, nullable=True)
    isHomeTeam = db.Column(db.Float, nullable=True)
    isPlayoffGame = db.Column(db.Float, nullable=True)
    lastEventCategory = db.Column(db.String(100), nullable=False)
    lastEventShotAngle = db.Column(db.Float, nullable=True)
    lastEventShotDistance = db.Column(db.Float, nullable=True)
    lastEventTeam = db.Column(db.String(100), nullable=False)
    lastEventxCord = db.Column(db.Float, nullable=True)
    lastEventxCord_adjusted = db.Column(db.Float, nullable=True)
    lastEventyCord = db.Column(db.Float, nullable=True)
    lastEventyCord_adjusted = db.Column(db.Float, nullable=True)
    location =  db.Column(db.String(100), nullable=False)
    offWing = db.Column(db.Float, nullable=True)
    period = db.Column(db.Float, nullable=True)
    playerNumThatDidEvent = db.Column(db.Float, nullable=True)
    playerNumThatDidLastEvent = db.Column(db.Float, nullable=True)
    playerPositionThatDidEvent = db.Column(db.String(100), nullable=False)
    shooterLeftRight = db.Column(db.String(100), nullable=False)
    shooterName = db.Column(db.String(100), nullable=False)

    shooterTimeOnIce = db.Column(db.Float, nullable=True)
    shooterTimeOnIceSinceFaceoff = db.Column(db.Float, nullable=True)
    shootingTeamAverageTimeOnIce = db.Column(db.Float, nullable=True)
    shootingTeamAverageTimeOnIceOfDefencemen = db.Column(db.Float, nullable=True)
    shootingTeamAverageTimeOnIceOfDefencemenSinceFaceoff = db.Column(db.Float, nullable=True)
    shootingTeamAverageTimeOnIceOfForwards = db.Column(db.Float, nullable=True)
    shootingTeamAverageTimeOnIceOfForwardsSinceFaceoff = db.Column(db.Float, nullable=True)
    shootingTeamAverageTimeOnIceSinceFaceoff = db.Column(db.Float, nullable=True)
    shootingTeamDefencemenOnIce = db.Column(db.Float, nullable=True)
    shootingTeamForwardsOnIce = db.Column(db.Float, nullable=True)
    shootingTeamMaxTimeOnIce = db.Column(db.Float, nullable=True)
    shootingTeamMaxTimeOnIceOfDefencemen = db.Column(db.Float, nullable=True)
    shootingTeamMaxTimeOnIceOfDefencemenSinceFaceoff = db.Column(db.Float, nullable=True)
    shootingTeamMaxTimeOnIceOfForwards = db.Column(db.Float, nullable=True)
    shootingTeamMaxTimeOnIceOfForwardsSinceFaceoff = db.Column(db.Float, nullable=True)
    shootingTeamMaxTimeOnIceSinceFaceoff = db.Column(db.Float, nullable=True)
    shootingTeamMinTimeOnIce = db.Column(db.Float, nullable=True)
    shootingTeamMinTimeOnIceOfDefencemen = db.Column(db.Float, nullable=True)
    shootingTeamMinTimeOnIceOfDefencemenSinceFaceoff = db.Column(db.Float, nullable=True)
    shootingTeamMinTimeOnIceOfForwards = db.Column(db.Float, nullable=True)
    shootingTeamMinTimeOnIceOfForwardsSinceFaceoff = db.Column(db.Float, nullable=True)
    shootingTeamMinTimeOnIceSinceFaceoff = db.Column(db.Float, nullable=True)
    shotAngle = db.Column(db.Float, nullable=True)
    shotAngleAdjusted = db.Column(db.Float, nullable=True)
    shotAnglePlusRebound = db.Column(db.Float, nullable=True)
    shotAnglePlusReboundSpeed = db.Column(db.Float, nullable=True)
    shotAngleReboundRoyalRoad = db.Column(db.Float, nullable=True)
    shotDistance = db.Column(db.Float, nullable=True)
    shotGeneratedRebound = db.Column(db.Float, nullable=True)
    shotGoalieFroze = db.Column(db.Float, nullable=True)
    shotOnEmptyNet = db.Column(db.Float, nullable=True)
    shotPlayContinuedInZone = db.Column(db.Float, nullable=True)
    shotPlayContinuedOutsideZone = db.Column(db.Float, nullable=True)
    shotPlayStopped = db.Column(db.Float, nullable=True)
    shotRebound = db.Column(db.Float, nullable=True)
    shotRush = db.Column(db.Float, nullable=True)
    shotType = db.Column(db.String(100), nullable=False)
    shotWasOnGoal = db.Column(db.Float, nullable=True)
    speedFromLastEvent = db.Column(db.Float, nullable=True)
    team = db.Column(db.String(100), nullable=False)
    teamCode = db.Column(db.String(100), nullable=False)
    time = db.Column(db.Float, nullable=True)
    timeDifferenceSinceChange = db.Column(db.Float, nullable=True)
    timeSinceFaceoff = db.Column(db.Float, nullable=True)
    timeSinceLastEvent = db.Column(db.Float, nullable=True)
    timeUntilNextEvent = db.Column(db.Float, nullable=True)
    xCord = db.Column(db.Float, nullable=True)
    xCordAdjusted = db.Column(db.Float, nullable=True)
    xFroze = db.Column(db.Float, nullable=True)
    xGoal = db.Column(db.Float, nullable=True)
    xPlayContinuedInZone = db.Column(db.Float, nullable=True)
    xPlayContinuedOutsideZone = db.Column(db.Float, nullable=True)
    xPlayStopped = db.Column(db.Float, nullable=True)
    xRebound = db.Column(db.Float, nullable=True)
    xShotWasOnGoal = db.Column(db.Float, nullable=True)
    yCord = db.Column(db.Float, nullable=True)
    yCordAdjusted = db.Column(db.Float, nullable=True)

    # note still needs to the POIU table references.


    def __repr__(self):
        return F"<Shot {self.id}>"

# get or create model
# this is common to do in databases
# reference here https://stackoverflow.com/questions/2546207/does-sqlalchemy-have-an-equivalent-of-djangos-get-or-create
def get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).one_or_none()
    if instance:
        return instance, False
    else:
        kwargs |= defaults or {}
        instance = model(**kwargs)
        try:
            session.add(instance)
            session.commit()
        except Exception:  # The actual exception depends on the specific database so we catch all exceptions. This is similar to the official documentation: https://docs.sqlalchemy.org/en/latest/orm/session_transaction.html
            session.rollback()
            instance = session.query(model).filter_by(**kwargs).one()
            return instance, False
        else:
            return instance, True


def create_all_database_tables():
    print("Creating Database Tables...")
    with app.app_context():
        db.create_all()
    print("Successfully created all tables!")




