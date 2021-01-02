from app import db


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Cities(db.Model):
    __tablename__ = 'City'
    id = db.Column(db.Integer, primary_key=True) #may be possible to use enum here
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    venue = db.relationship('Venue', backref='city', lazy=True)
    artist = db.relationship('Artist', backref='city', lazy=True)

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String)
    city_id = db.Column(db.Integer, db.ForeignKey('City.id'), nullable=False)
    genere = db.Column(db.String)
    shows = db.relationship('Shows', backref='venue', lazy=True)


    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    city_id = db.Column(db.Integer, db.ForeignKey('City.id'), nullable=False)
    shows = db.relationship('Shows', backref='artist', lazy=True)

class Shows(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
  # Relationships: artist one/many -> many shows / veneus one -> many shows