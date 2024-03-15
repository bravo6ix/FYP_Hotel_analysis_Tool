const express = require("express");
const router = express.Router();

/* mongoose */
const mongoose = require("mongoose");
const mongoDB = "mongodb+srv://qq1027784227:qq1027784227@hotel.0a4is7r.mongodb.net/";
mongoose.connect(mongoDB);
mongoose.Promise = global.Promise;
const db = mongoose.connection;
db.on("error", console.error.bind(console, "MongoDB connection error:"));

var Schema = mongoose.Schema;
var SomeModelSchema = new Schema({
    name: String,
    location: String,
    price: String,
    rating: String,
    time: String,
});

const SomeModel = mongoose.model("SomeModel", SomeModelSchema);

/* GET all collection booking_price data follwing the data schema */
router.get('/data', async function (req, res, next) {
    try {
        const result = await db.collection("booking_price").find({}).toArray();
        return res.status(200).json(result);
    } catch (error) {
        return res.status(500).json(error);
    }
});

module.exports = router