const express = require("express");
const router = express.Router();

/* token */
let jwt = require("jsonwebtoken");
let auth = require("../middlewares/auth");
const { v4: uuidv4 } = require("uuid");

/* bcrypt */
const bcrypt = require("bcrypt");
// const saltRounds = 10;

/* MongoDB Client */
const { MongoClient } = require("mongodb");
let ObjectId = require("mongodb").ObjectId;
const url =
    "mongodb+srv://qq1027784227:qq1027784227@hotel.0a4is7r.mongodb.net/";
const client = new MongoClient(url);
const db = client.db("hotels");

/* User Login */
router.post('/login', async (req, res) => {
    const { username, password } = req.body;

    try {
      // 获取数据库集合实例
      const usersCollection = db.collection('users');

      // 在集合中查找匹配的用户
      const user = await usersCollection.findOne({ username });

      if (!user) {
        return res.status(404).json({ message: 'User not found' });
      }

      // 验证密码
      const passwordMatch = await bcrypt.compare(password, user.password);

      if (!passwordMatch) {
        return res.status(401).json({ message: 'Invalid password' });
      }

      // 登录成功
      res.status(200).json({ message: 'Login successful' });
    } catch (err) {
      console.error('Login error', err);
      res.status(500).json({ message: 'Internal server error' });
    }
  });


module.exports = router;
