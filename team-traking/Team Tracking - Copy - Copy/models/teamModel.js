const { MongoClient } = require('mongodb');

// Replace with your actual MongoDB connection string from MongoDB Atlas
const uri = 'mongodb+srv://2022it0117:pW1xTLEm5WTmb9zg@tracking.dzec1.mongodb.net/Tracking?retryWrites=true&w=majority';

let db;

// Connect to MongoDB and get the database instance
async function connectToDb() {
  if (db) return db;
  
  try {
    const client = await MongoClient.connect(uri, { useNewUrlParser: true, useUnifiedTopology: true });
    db = client.db('Tracking'); // Replace with your actual database name
    return db;
  } catch (error) {
    console.error('Failed to connect to the database:', error);
    throw error;
  }
}

// Fetch team data by team name
async function getTeamByName(teamName) {
  const db = await connectToDb();
  try {
    const team = await db.collection('teams').findOne({ teamName: teamName });
    return team;
  } catch (error) {
    console.error('Error fetching team data:', error);
    throw error;
  }
}

module.exports = {
  getTeamByName
};
