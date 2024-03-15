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
        const result = await db.collection("users").findOne({
            username: user.username,
        });
        if (result) {
            const match = bcrypt.compareSync(user.password, result.password);
            if (match) {
                delete result.password;
                const user = {};
                const token = jwt.sign(
                    {
                        user_id: req.body.email,
                        username: result.username,
                        role: result.role,
                    },
                    "process.env.TOKEN_KEY",
                    {
                        expiresIn: "1h",
                    }
                );
                user.token = token;
                return res.status(200).json(user);
            } else
                return res.status(401).json({ message: "Incorrect password" });
        } else
            return res.status(401).json({ message: "User not found" });
    } catch (error) {
        return res.status(500).json(error);
    }
});

// Get User by ID
router.get("/get/:id", auth, async function (req, res, next) {
    let user = req.user;
    delete user.iat;
    delete user.exp;

    if (!ObjectId.isValid(req.params.id))
        return res.status(404).send("Unable to find the requested resource!");

    let result = await db.collection("users").findOne({ _id: new ObjectId(req.params.id) });
    if (!result)
        return res.status(404).send("Unable to find the requested resource!");

    return res.json({ items: result });
});

// Get User by Role
router.get('/get/role/:role', auth, async function (req, res, next) {
    let user = req.user;
    delete user.iat;
    delete user.exp;

    if (user.role === 'admin')
        return res.status(403).send("Not allowed to access!");

    console.log(req.params.role);
    let result = await db.collection("users").find({ role: req.params.role }).toArray();
    if (!result) return res.status(404).send('Unable to find the requested resource!');

    return res.json({ items: result })
});

router.put("/update/:id", auth, async function (req, res) {
    let result = {};
    if (!ObjectId.isValid(req.params.id))
        return res.status(404).send("Id is not is valid!");

    if (req.params.id) {
        if (req.body.password) {
            const salt = bcrypt.genSaltSync(saltRounds);
            const hash = bcrypt.hashSync(req.body.password, salt);
            req.body.password = hash;
            try {
                const result = await db.collection('users').findOneAndReplace(
                    { _id: new ObjectId(req.params.id) },
                    req.body
                );
                return res.status(200).send("item updated");
                if (!result.value)
                return res.status(404).send("Unable to find the requested resource!");
            } catch (e) {
                return res.status(500).send(e);
            }
        } else {
            const result = await db.collection('users').findOneAndReplace(
                { _id: new ObjectId(req.params.id) },
                req.body
            );
            return res.status(200).send("item updated");
            if (!result.value)
            return res.status(404).send("Unable to find the requested resource!");
        }
    }
});

/* Check user token */
router.get("/check", auth, async function (req, res, next) {
    let user = req.user;
    delete user.iat;
    delete user.exp;
    return res.status(200).json(user);
})

/* User Create */
router.post("/create", auth, async function (req, res, next) {
    let loggedUser = req.user;
    delete loggedUser.iat;
    delete loggedUser.exp;

    if (loggedUser.role === 'admin')
        return res.status(403).send("Not allowed to create users!");

    let user = req.body;
    const salt = bcrypt.genSaltSync(saltRounds);
    const hash = bcrypt.hashSync(user.password, salt);
    try {
        const result = await db.collection("users").insertOne({
            username: user.username,
            password: hash,
            role: user.role,
            email: user.email
        });
        return res.status(201).json(result);
    } catch (e) {
        return res.status(500).json(e);
    }
});

module.exports = router;
