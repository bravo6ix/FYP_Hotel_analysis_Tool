const express = require('express');
const mongodb = require('mongodb');
const mongoose = require('mongoose');
const router = express.Router();

/* MongoDB Client */
const { MongoClient } = require("mongodb");
let ObjectId = require("mongodb").ObjectId;
const url =
    "mongodb+srv://qq1027784227:qq1027784227@hotel.0a4is7r.mongodb.net/";
const client = new MongoClient(url);
const db = client.db("hotels");

/* GET all booking_price collection data */
router.get('/all-data', async function (req, res, next) {
    try {
        const result = await db.collection("booking_price").find({}).toArray();
        return res.status(200).json(result);
    } catch (error) {
        return res.status(500).json(error);
    }
});

/* GET booking per sum by month with price data */
router.get('/month-sum-price', async function (req, res, next) {
    try {
        const result = await db.collection("booking_price").aggregate([
            {
                $group: {
                    _id: { month: "$month" },
                    totalAmount: { $sum: '$price' }
                }
            },
            {
                $project: {
                    month: '$_id.month',
                    totalAmount: 1,
                    _id: 0
                }
            },
            {
                $sort: { month: 1 }
            }
        ]).toArray();

        res.json(result);
    } catch (error) {
        console.error('Error calculating monthly total price:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

/* Get all booking_price collection Sum of Price */
router.get('/sum-price', async function (req, res) {
    try {
        const result = await db.collection("booking_price").aggregate([
            {
                $group: {
                    _id: null,
                    totalAmount: { $sum: '$price' }
                }
            }
        ]).toArray();

        if (result.length > 0) {
            res.json({ totalAmount: result[0].totalAmount });
        } else {
            res.json({ totalAmount: 0 });
        }
    } catch (error) {
        console.error('Error calculating total price:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

// !!!!!!!!! test ~~~~~~~~~~~~~
// Get hotel names by Hong Kong Island District
router.get('/hotels/test', async (req, res) => {
    const district = 'Hong Kong Island';

    try {
        const hotels = await db.collection('booking_price').find({ district }).toArray();
        const hotelNames = hotels.map(hotel => hotel.hotel_name);
        res.json(hotelNames);
    } catch (error) {
        console.error('Error fetching hotels:', error);
        res.status(500).send('Error fetching hotels');
    }
});

// Get hotel names by Hong Kong Island District and count numbers
router.get('/hotels/hongkongisland', async (req, res) => {
    const district = 'Hong Kong Island';
    try {
        const hotels = await db.collection('booking_price').find({ district }).toArray();
        const hotelCounts = hotels.reduce((acc, hotel) => {
            acc[hotel.hotel_name] = (acc[hotel.hotel_name] || 0) + 1;
            return acc;
        }, {});
        const wordCloudData = Object.entries(hotelCounts).map(([name, value]) => ({ name, value }));
        res.json(wordCloudData);
    } catch (error) {
        console.error('Error fetching hotels:', error);
        res.status(500).send('Error fetching hotels');
    }
});

// Get Hong Kong Island District and total price per month
router.get('/hotels/hongkongisland/total-price-per-month', async (req, res) => {
    const district = 'Hong Kong Island';
    try {
        const pipeline = [
            {
                $match: {
                    district: district
                }
            },
            {
                $group: {
                    _id: "$month",
                    totalPrice: { $sum: "$price" }
                }
            },
            {
                $project: {
                    _id: 0,
                    month: "$_id",
                    totalPrice: 1
                }
            },
            {
                $sort: {
                    month: 1
                }
            }
        ];
        const result = await db.collection('booking_price').aggregate(pipeline).toArray();
        res.json(result);
    } catch (error) {
        console.error('Error fetching total price per month:', error);
        res.status(500).send('Error fetching total price per month');
    }
});

// Get hotel names by Kowloon District and count numbers
router.get('/hotels/kowloon', async (req, res) => {
    const district = 'Kowloon City';
    try {
        const hotels = await db.collection('booking_price').find({ district }).toArray();
        const hotelCounts = hotels.reduce((acc, hotel) => {
            acc[hotel.hotel_name] = (acc[hotel.hotel_name] || 0) + 1;
            return acc;
        }, {});
        const wordCloudData = Object.entries(hotelCounts).map(([name, value]) => ({ name, value }));
        res.json(wordCloudData);
    } catch (error) {
        console.error('Error fetching hotels:', error);
        res.status(500).send('Error fetching hotels');
    }
});
// Get Kowloon District and total price per month
router.get('/hotels/kowloon/total-price-per-month', async (req, res) => {
    const district = 'Kowloon City';
    try {
        const pipeline = [
            {
                $match: {
                    district: district
                }
            },
            {
                $group: {
                    _id: "$month",
                    totalPrice: { $sum: "$price" }
                }
            },
            {
                $project: {
                    _id: 0,
                    month: "$_id",
                    totalPrice: 1
                }
            },
            {
                $sort: {
                    month: 1
                }
            }
        ];
        const result = await db.collection('booking_price').aggregate(pipeline).toArray();
        res.json(result);
    } catch (error) {
        console.error('Error fetching total price per month:', error);
        res.status(500).send('Error fetching total price per month');
    }
});


// Get hotel names by Tsim Sha Tsui District and count numbers
router.get('/hotels/tsimshatsui', async (req, res) => {
    const district = 'Tsim Sha Tsui';
    try {
        const hotels = await db.collection('booking_price').find({ district }).toArray();
        const hotelCounts = hotels.reduce((acc, hotel) => {
            acc[hotel.hotel_name] = (acc[hotel.hotel_name] || 0) + 1;
            return acc;
        }, {});
        const wordCloudData = Object.entries(hotelCounts).map(([name, value]) => ({ name, value }));
        res.json(wordCloudData);
    } catch (error) {
        console.error('Error fetching hotels:', error);
        res.status(500).send('Error fetching hotels');
    }
});

// Get Tsim Sha Tsui District and total price per month
router.get('/hotels/tsimshatsui/total-price-per-month', async (req, res) => {
    const district = 'Tsim Sha Tsui';
    try {
        const pipeline = [
            {
                $match: {
                    district: district
                }
            },
            {
                $group: {
                    _id: "$month",
                    totalPrice: { $sum: "$price" }
                }
            },
            {
                $project: {
                    _id: 0,
                    month: "$_id",
                    totalPrice: 1
                }
            },
            {
                $sort: {
                    month: 1
                }
            }
        ];
        const result = await db.collection('booking_price').aggregate(pipeline).toArray();
        res.json(result);
    } catch (error) {
        console.error('Error fetching total price per month:', error);
        res.status(500).send('Error fetching total price per month');
    }
});

// Get hotel names by Tsim Sha Tsui District and count numbers
router.get('/hotels/yautsimmong', async (req, res) => {
    const district = 'Yau Tsim Mong';
    try {
        const hotels = await db.collection('booking_price').find({ district }).toArray();
        const hotelCounts = hotels.reduce((acc, hotel) => {
            acc[hotel.hotel_name] = (acc[hotel.hotel_name] || 0) + 1;
            return acc;
        }, {});
        const wordCloudData = Object.entries(hotelCounts).map(([name, value]) => ({ name, value }));
        res.json(wordCloudData);
    } catch (error) {
        console.error('Error fetching hotels:', error);
        res.status(500).send('Error fetching hotels');
    }
});

// Get Tsim Sha Tsui District and total price per month
router.get('/hotels/yautsimmong/total-price-per-month', async (req, res) => {
    const district = 'Yau Tsim Mong';
    try {
        const pipeline = [
            {
                $match: {
                    district: district
                }
            },
            {
                $group: {
                    _id: "$month",
                    totalPrice: { $sum: "$price" }
                }
            },
            {
                $project: {
                    _id: 0,
                    month: "$_id",
                    totalPrice: 1
                }
            },
            {
                $sort: {
                    month: 1
                }
            }
        ];
        const result = await db.collection('booking_price').aggregate(pipeline).toArray();
        res.json(result);
    } catch (error) {
        console.error('Error fetching total price per month:', error);
        res.status(500).send('Error fetching total price per month');
    }
});

// Get average-hotel-price
router.get('/average-price-per-month', async (req, res) => {
    try {
        const collection = client.db('hotels').collection('booking_price');
        const prices = await collection.aggregate([
            {
                $group: {
                    _id: "$month",
                    avgPrice: { $avg: "$price" }
                }
            },
            {
                $sort: { "_id": 1 }
            }
        ]).toArray();

        // Convert _id to month and round avgPrice to 2 decimal places
        const result = prices.map(({ _id, avgPrice }) => ({
            month: _id,
            avgPrice: Math.round(avgPrice * 100) / 100
        }));

        res.json(result);
    } catch (error) {
        console.error('Error fetching average price:', error);
        res.status(500).send('Error fetching average price');
    }
});

module.exports = router;