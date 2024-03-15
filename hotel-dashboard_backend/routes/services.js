const express = require('express');
const mongodb = require('mongodb');
const router = express.Router();

/* MongoDB Client */
const { MongoClient } = require("mongodb");
let ObjectId = require("mongodb").ObjectId;
const url =
    "mongodb+srv://qq1027784227:qq1027784227@hotel.0a4is7r.mongodb.net/";
const client = new MongoClient(url);
const db = client.db("hotels");


/* GET all booking_price collection data */
router.get('/data', async function (req, res, next) {
    try {
        const result = await db.collection("booking_price").find({}).toArray();
        return res.status(200).json(result);
    } catch (error) {
        return res.status(500).json(error);
    }
});

module.exports = router;