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
router.post("/login", async function (req, res, next) {
    let user = req.body;

    try {
        // Find user with requested email
        let userFromDb = await db.collection("user").findOne({ email: user.email });
        if (!userFromDb) {
            return res.status(400).send("User not found");
        }

        // Compare passwords
        let passwordMatch = bcrypt.compareSync(user.password, userFromDb.password);
        if (!passwordMatch) {
            return res.status(400).send("Invalid password");
        }

        // Create JWT
        let token = jwt.sign({ email: userFromDb.email }, 'process.env.TOKEN_KEY', { expiresIn: '1h' });

        // Send back token
        res.json({ token: token });
    } catch (error) {
        next(error);
    }
});


module.exports = router;
