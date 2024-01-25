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
    "mongodb://groupd:vlQz3qq10nGdmFSb@ac-gm2iezg-shard-00-00.eyyijsu.mongodb.net:27017,ac-gm2iezg-shard-00-01.eyyijsu.mongodb.net:27017,ac-gm2iezg-shard-00-02.eyyijsu.mongodb.net:27017/?ssl=true&replicaSet=atlas-wzwa6h-shard-0&authSource=admin&retryWrites=true&w=majority";
const client = new MongoClient(url);
const db = client.db("cubcGroupD-DB");

module.exports = router;
