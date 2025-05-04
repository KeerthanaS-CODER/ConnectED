const express = require('express');
const router = express.Router();
const { MongoClient } = require('mongodb');

// Replace with your actual MongoDB connection string
const uri = 'mongodb+srv://2022it0117:pW1xTLEm5WTmb9zg@tracking.dzec1.mongodb.net/Tracking?retryWrites=true&w=majority';
let db;

// Connect to MongoDB
MongoClient.connect(uri, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(client => {
    console.log('Connected to Database');
    db = client.db('Tracking'); // Replace with your actual database name
  })
  .catch(error => console.error(error));

// Fetch team data by team name
router.get('/:teamName', async (req, res) => {
  const teamName = req.params.teamName;
  try {
    const team = await db.collection('teams').findOne({ teamName: teamName });
    if (team) {
      res.json(team);
    } else {
      res.status(404).json({ error: 'Team not found' });
    }
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

module.exports = router;
