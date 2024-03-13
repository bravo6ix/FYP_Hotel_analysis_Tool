const express = require('express');
const mongodb = require('mongodb');

const app = express();
const port = 3000;

// MongoDB连接字符串
const mongoURI = 'mongodb+srv://qq1027784227:qq1027784227@hotel.0a4is7r.mongodb.net/';

// 连接到MongoDB数据库
mongodb.MongoClient.connect(mongoURI, { useUnifiedTopology: true })
  .then(client => {
    console.log('Connected to MongoDB');
    const db = client.db('Hotel');
    const collection = db.collection('user');

    // 定义API路由
    app.get('/api/data', (req, res) => {
      // 从数据库中获取数据
      collection.find().toArray()
        .then(data => {
          res.json(data);
        })
        .catch(error => {
          res.status(500).json({ error: 'Error retrieving data from MongoDB' });
        });
    });
  })
  .catch(error => {
    console.error('Failed to connect to MongoDB', error);
  });

// 启动Express服务器
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});