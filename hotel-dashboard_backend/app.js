var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');



var indexRouter = require('./routes/index');
const usersRouter = require('./routes/users');
const servicesRouter = require('./routes/services');

var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use(
  cors({
      origin: 'http://localhost:8080',
      preflightContinue: true,
  }),
);

app.use('/', indexRouter);
app.use('/api/users', usersRouter);
app.use('/api/services', servicesRouter);

// mongoDB connection
const mongodb = require('mongodb');
const MongoClient = mongodb.MongoClient;
const mongoURI = 'mongodb+srv://qq1027784227:qq1027784227@hotel.0a4is7r.mongodb.net/';
const client = new MongoClient(mongoURI, { useUnifiedTopology: true });
app.locals.db = client.db('Hotel');

// connect to mongoDB
client.connect(function(err) {
  if (err) {
    console.log('Failed to connect to MongoDB', err);
  } else {
    console.log('Connected to MongoDB');
  }
});

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;
