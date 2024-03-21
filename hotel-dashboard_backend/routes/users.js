const express = require("express");
const router = express.Router();

/* token */
let jwt = require("jsonwebtoken");
let auth = require("../middlewares/auth");
const { v4: uuidv4 } = require("uuid");

/* bcrypt */
const bcrypt = require("bcrypt");
const saltRounds = 10;

/* MongoDB Client */
const { MongoClient } = require("mongodb");
let ObjectId = require("mongodb").ObjectId;
const url =
    "mongodb+srv://qq1027784227:qq1027784227@hotel.0a4is7r.mongodb.net/";
const client = new MongoClient(url);
const db = client.db("hotels");

/* User Login */


// Get User by ID
router.get("/:id", async function (req, res, next) {
    try {
        const result = await db.collection("user").findOne({ _id: new ObjectId(req.params.id) });
        res.json(result);
    } catch (error) {
        console.error('Error retrieving user:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

module.exports = router;
