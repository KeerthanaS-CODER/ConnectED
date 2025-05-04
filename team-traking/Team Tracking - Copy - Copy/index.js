const express = require('express');
const cors = require('cors');
const { MongoClient } = require('mongodb');

const app = express();
const port = 3000;


const uri = 'mongodb+srv://2022it0117:pW1xTLEm5WTmb9zg@tracking.dzec1.mongodb.net/Tracking?retryWrites=true&w=majority';

let db;


app.use(cors());
app.use(express.json());
app.use(express.static('public'));


MongoClient.connect(uri)
  .then(client => {
    console.log('Connected to Database');
    db = client.db('Tracking'); 

    
    db.command({ ping: 1 }, (err, result) => {
      if (err) {
        console.error('Failed to ping database:', err);
      } else {
        console.log('Database ping successful:', result);
      }
    });

    
    app.listen(port, () => {
      console.log(`Server running at http://localhost:${port}`);
    });
  })
  .catch(error => {
    console.error('Failed to connect to the database:', error);
    process.exit(1); 
  });


app.get('/team/:teamName', async (req, res) => {
  const teamName = req.params.teamName;
  try {
    if (!db) {
      return res.status(500).json({ error: 'Database not connected' });
    }
    const team = await db.collection('teams').findOne({ teamName: teamName });
    if (team) {
      res.json(team);
    } else {
      res.status(404).json({ error: 'Team not found' });
    }
  } catch (err) {
    console.error('Error fetching team data:', err.message);
    res.status(500).json({ error: 'Internal Server Error', details: err.message });
  }
});
