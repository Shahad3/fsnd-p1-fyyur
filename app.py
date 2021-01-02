#----------------------------------------------------------------------------#
# Imports

# I should do the count for upcoming shows in the venes page
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from sqlalchemy.exc import SQLAlchemyError
from datetime import date
from models import *



# ------Added-------#
from flask_migrate import Migrate

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:xyz@localhost:5432/fyyur'
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database
migrate = Migrate(app, db)

# #----------------------------------------------------------------------------#
# # Models.
# #----------------------------------------------------------------------------#

# class Cities(db.Model):
#     __tablename__ = 'City'
#     id = db.Column(db.Integer, primary_key=True) #may be possible to use enum here
#     city = db.Column(db.String(120))
#     state = db.Column(db.String(120))
#     venue = db.relationship('Venue', backref='city', lazy=True)
#     artist = db.relationship('Artist', backref='city', lazy=True)

# class Venue(db.Model):
#     __tablename__ = 'Venue'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, unique=True)
#     address = db.Column(db.String(120))
#     phone = db.Column(db.String(120))
#     image_link = db.Column(db.String(500))
#     facebook_link = db.Column(db.String(120))
#     # Do this later, num_shows should be aggregated based on number of upcoming shows per venue.
#     # num_upcoming_shows = (db.Integer, primary_key=True)
#     seeking_talent = db.Column(db.Boolean, nullable=False)
#     seeking_description = db.Column(db.String)
#     city_id = db.Column(db.Integer, db.ForeignKey('City.id'), nullable=False)
#     genere = db.Column(db.String)
#     shows = db.relationship('Shows', backref='venue', lazy=True)


#     # TODO: implement any missing fields, as a database migration using Flask-Migrate

# class Artist(db.Model):
#     __tablename__ = 'Artist'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, unique=True)
#     phone = db.Column(db.String(120))
#     genres = db.Column(db.String(120))
#     image_link = db.Column(db.String(500))
#     facebook_link = db.Column(db.String(120))
#     city_id = db.Column(db.Integer, db.ForeignKey('City.id'), nullable=False)
#     shows = db.relationship('Shows', backref='artist', lazy=True)

# class Shows(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     start_time = db.Column(db.DateTime)
#     artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
#     venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
#   # Relationships: artist one/many -> many shows / veneus one -> many shows

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

# def format_datetime(value, format='medium'):
#   # date = dateutil.parser.parse(value)
#   date = value
#   print(date)
#   if format == 'full':
#       format="EEEE MMMM, d, y 'at' h:mma"
#   elif format == 'medium':
#       format="EE MM, dd, y h:mma"
#   return babel.dates.format_datetime(date, format)

# app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  venues = {}
  cities = Cities.query.all()
  for city in cities:
    venues[city.id] = Venue.query.filter_by(city_id = city.id).all()
  # for city in cities:
  #   print(city.city)
  #   data2['city'] = city.city
  #   data2['state'] = city.state
  #   data2['venues'] = Venue.query.filter_by(city_id = city.id).all()
  #   print(data)
  #   data.append(data2)
  # data.venues = Venues.query.all()
  return render_template('pages/venues.html', areas=cities, venues=venues);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_word = request.form.get('search_term', '')
  # Sources:https://stackoverflow.com/questions/20363836/postgresql-ilike-query-with-sqlalchemy
  # https://stackoverflow.com/questions/16573095/case-insensitive-flask-sqlalchemy-query
  response = Venue.query.filter(Venue.name.ilike(f'%{search_word}%')).all()
  # response = Venue.query.filter_by(name = search_word).all()
  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  response = Venue.query.get(venue_id)
  response.genres = response.genere[1:-1].split(',')
  # source:https://www.programiz.com/python-programming/datetime/current-datetime
  today = date.today()
  response.past_shows = []
  response.upcoming_shows = []
  for show in response.shows:
    if(show.start_time > today):
      response.upcoming_shows.append(show)
    else:
      response.past_shows.append(show)
    response.past_per = db.session.query(Artist).join(Artist.shows).join(Shows.venue).all()  
  # data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  return render_template('pages/show_venue.html', venue=response)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  # https://stackoverflow.com/questions/20831871/how-to-avoid-inserting-duplicate-entries-when-adding-values-via-a-sqlalchemy-rel
  form = VenueForm()

  # state options
  # source:https://stackoverflow.com/questions/37133774/how-can-i-select-only-one-column-using-sqlalchemy
  states = db.session.query(Cities.id, Cities.state).all()
  # source:https://stackoverflow.com/questions/59603650/passing-a-variable-into-a-wtforms-class
  form.state.choices=states
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # source:https://wtforms.readthedocs.io/en/2.3.x/crash_course/
  form = VenueForm(request.form)

  # source:https://stackoverflow.com/questions/32938475/flask-sqlalchemy-check-if-row-exists-in-table
  city_name = db.session.query(Cities.city).filter_by(id=form.state.data).scalar() # is not None
  if (city_name == form.city.data):
    print("exist")
    city_id = form.state.data
  else:
    print("No")
    state = db.session.query(Cities.state).filter_by(id=form.state.data).scalar()
    city = Cities(city=form.city.data, state=state)
    # source:https://stackoverflow.com/questions/1316952/sqlalchemy-flush-and-get-inserted-id
    db.session.add(city)
    db.session.flush()
    db.session.refresh(city)
    city_id = city.id

  # print(city_id)
  gen = form.genres.data[:-1]
  venue = Venue(name=form.name.data, address=form.address.data, phone=form.phone.data, facebook_link=form.facebook_link.data, city_id=city_id, seeking_talent=False, genere=gen)
  # todo = Todo(description=description)
  try:
    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    flash('An error occurred. Venue ' + form.name.data + ' could not be listed.')

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>/delete', methods=['POST'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
    flash('Venue was successfully listed!')
    return render_template('pages/home.html')
    

  # source: https://stackoverflow.com/questions/2136739/error-handling-in-sqlalchemy
  except SQLAlchemyError as e:
    error = str(e.__dict__['orig'])
    print(error)
    return render_template('errors/500.html'), 500

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data= Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_word = request.form.get('search_term', '')
  response = Artist.query.filter(Artist.name.ilike(f'%{search_word}%')).all()
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  data = Artist.query.get(artist_id)
  today = date.today()
  data.past_shows = []
  data.upcoming_shows = []
  data.genres = data.genres[1:-1].split(',')
  for show in data.shows:
    if(show.start_time > today):
      data.upcoming_shows.append(show)
    else:
      data.past_shows.append(show)
  # data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()

  # TODO: populate form with fields from artist with ID <artist_id>
  response = Artist.query.get(artist_id)
  response.genres = response.genres[1:-1].split(',')
  # state options
  # source:https://stackoverflow.com/questions/37133774/how-can-i-select-only-one-column-using-sqlalchemy
  states = db.session.query(Cities.id, Cities.state).all()
  # source:https://stackoverflow.com/questions/59603650/passing-a-variable-into-a-wtforms-class
  form.state.choices=states
  form.name.data = response.name
  form.city.data = response.city.city
  form.phone.data = response.phone
  form.facebook_link.data = response.facebook_link
  return render_template('forms/edit_artist.html', form=form, artist=response)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  form = ArtistForm(request.form)
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  artist = Artist.query.filter_by(id=artist_id).first()
  # source:https://stackoverflow.com/questions/32938475/flask-sqlalchemy-check-if-row-exists-in-table
  city_name = db.session.query(Cities.city).filter_by(id=form.state.data).scalar() # is not None
  if (city_name == form.city.data):
    print("exist")
    city_id = form.state.data
  else:
    print("No")
    state = db.session.query(Cities.state).filter_by(id=form.state.data).scalar()
    city = Cities(city=form.city.data, state=state)
    # source:https://stackoverflow.com/questions/1316952/sqlalchemy-flush-and-get-inserted-id
    db.session.add(city)
    db.session.flush()
    db.session.refresh(city)
    city_id = city.id

  # print(city_id)
  gen = form.genres.data[:-1]
  artist.name=form.name.data
  artist.phone=form.phone.data
  artist.facebook_link=form.facebook_link.data
  artist.city_id=city_id
  artist.genres=gen
  # todo = Todo(description=description)
  db.session.commit()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  # TODO: populate form with values from venue with ID <venue_id>
  response = Venue.query.get(venue_id)
  response.genres = response.genere[1:-1].split(',')
  # state options
  # source:https://stackoverflow.com/questions/37133774/how-can-i-select-only-one-column-using-sqlalchemy
  states = db.session.query(Cities.id, Cities.state).all()
  # source:https://stackoverflow.com/questions/59603650/passing-a-variable-into-a-wtforms-class
  form.state.choices=states
  form.name.data = response.name
  form.city.data = response.city.city
  form.address.data = response.address
  form.phone.data = response.phone
  form.facebook_link.data = response.facebook_link
  return render_template('forms/edit_venue.html', form=form, venue=response)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
# source:https://wtforms.readthedocs.io/en/2.3.x/crash_course/
  form = VenueForm(request.form)
  venue = Venue.query.filter_by(id=venue_id).first()
  # source:https://stackoverflow.com/questions/32938475/flask-sqlalchemy-check-if-row-exists-in-table
  city_name = db.session.query(Cities.city).filter_by(id=form.state.data).scalar() # is not None
  if (city_name == form.city.data):
    print("exist")
    city_id = form.state.data
  else:
    print("No")
    state = db.session.query(Cities.state).filter_by(id=form.state.data).scalar()
    city = Cities(city=form.city.data, state=state)
    # source:https://stackoverflow.com/questions/1316952/sqlalchemy-flush-and-get-inserted-id
    db.session.add(city)
    db.session.flush()
    db.session.refresh(city)
    city_id = city.id

  # print(city_id)
  gen = form.genres.data[:-1]
  venue.name=form.name.data
  venue.address=form.address.data
  venue.phone=form.phone.data
  venue.facebook_link=form.facebook_link.data
  venue.city_id=city_id
  venue.genere=gen
  # todo = Todo(description=description)
  db.session.commit()

  
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  states = db.session.query(Cities.id, Cities.state).all()
  form.state.choices=states
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = ArtistForm(request.form)
  # source:https://stackoverflow.com/questions/32938475/flask-sqlalchemy-check-if-row-exists-in-table
  city_name = db.session.query(Cities.city).filter_by(id=form.state.data).scalar() # is not None
  if (city_name == form.city.data):
    print("exist")
    city_id = form.state.data
  else:
    print("No")
    state = db.session.query(Cities.state).filter_by(id=form.state.data).scalar()
    city = Cities(city=form.city.data, state=state)
    # source:https://stackoverflow.com/questions/1316952/sqlalchemy-flush-and-get-inserted-id
    db.session.add(city)
    db.session.flush()
    db.session.refresh(city)
    city_id = city.id

  gen = form.genres.data[:-1]
  artist = Artist(name=form.name.data, phone=form.phone.data, facebook_link=form.facebook_link.data, city_id=city_id, genres=gen)
  # todo = Todo(description=description)
  try:
    db.session.add(artist)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    flash('An error occurred. Venue ' + form.name.data + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data= Shows.query.all()
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  form = ShowForm(request.form)
  show = Shows(start_time=form.start_time.data, artist_id=form.artist_id.data, venue_id=form.venue_id.data)
  # todo = Todo(description=description)
  try:
    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')
  except:
    flash('An error occurred. Show could not be listed.')
  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
