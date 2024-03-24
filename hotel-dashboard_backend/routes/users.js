const express = require("express");
const router = express.Router();

/* token */
let jwt = require("jsonwebtoken");
let auth = require("../middlewares/auth");
const { v4: uuidv4 } = require("uuid");

/* bcrypt */
const bcrypt = require("bcrypt");
const saltRounds = 10;

/* mongodb */
const { MongoClient } = require("mongodb");
let ObjectId = require("mongodb").ObjectId;
const url =
    "mongodb+srv://qq1027784227:qq1027784227@hotel.0a4is7r.mongodb.net/";
const client = new MongoClient(url);
const db = client.db("hotels");

/* GET users listing. */
router.get("/", function (req, res, next) {
  res.send("respond with a resource");
});

/* GET users listing. */

/* GET all users */
router.get("/all-users", async function (req, res, next) {
  try {
    const result = await db.collection("users").find({}).toArray();
    return res.status(200).json(result);
  } catch (error) {
    return res.status(500).json(error);
  }
});

/* GET user by id */
router.get("/:id", async function (req, res, next) {
  try {
    const result = await db
      .collection("users")
      .find({ _id: ObjectId(req.params.id) })
      .toArray();
    return res.status(200).json(result);
  } catch (error) {
    return res.status(500).json(error);
  }
});

/* GET user by email */
router.get("/email/:email", async function (req, res, next) {
  try {
    const result = await db
      .collection("users")
      .find({ email: req.params.email })
      .toArray();
    return res.status(200).json(result);
  } catch (error) {
    return res.status(500).json(error);
  }
});

/* GET user by username */
router.get("/username/:username", async function (req, res, next) {
  try {
    const result = await db
      .collection("users")
      .find({ username: req.params.username })
      .toArray();
    return res.status(200).json(result);
  } catch (error) {
    return res.status(500).json(error);
  }
});

/* POST user login */
router.post("/login",  async function (req, res, next) {
  try {
    const result = await db
      .collection("users")
      .find({ email: req.body.email })
      .toArray();
    if (result.length > 0) {
      if (bcrypt.compareSync(req.body.password, result[0].password)) {
        const token = jwt.sign(
          {
            userId: result[0]._id,
            email: result[0].email,
            username: result[0].username,
          },
          process.env.ACCESS_TOKEN_SECRET,
          { expiresIn: "1h" }
        );
        return res.status(200).json({ token: token });
      } else {
        return res.status(401).json({ error: "Invalid password" });
      }
    } else {
      return res.status(404).json({ error: "User not found" });
    }
  } catch (error) {
    return res.status(500).json(error);
  }
});

module.exports = router;
