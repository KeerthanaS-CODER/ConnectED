const express = require("express");
const path = require("path");
const fs = require("fs"); // Add this to use the file system
const mysql = require("mysql2");
const multer = require("multer");
const app = express();
const server = require("http").createServer(app);
const io = require("socket.io")(server);

// MySQL Database Connection (unchanged)
const db = mysql.createConnection({
    host: "localhost",
    user: "root",
    password: "root",  // Replace with your password
    database: "chatapp"
});

db.connect((err) => {
    if (err) {
        console.error("Error connecting to MySQL:", err);
        return;
    }
    console.log("Connected to MySQL database!");
});

// Ensure the uploads directory exists
const uploadDir = path.join(__dirname, "uploads");
if (!fs.existsSync(uploadDir)) {
    fs.mkdirSync(uploadDir, { recursive: true }); // Create the directory if it doesn't exist
}

// Set up multer storage for file uploads
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, uploadDir); // Save files to the 'uploads' directory
    },
    filename: function (req, file, cb) {
        cb(null, Date.now() + path.extname(file.originalname)); // Save file with a unique name
    }
});

const upload = multer({ storage: storage });

// Route to handle file uploads
app.post("/upload", upload.single("file"), (req, res) => {
    if (!req.file) {
        return res.status(400).json({ success: false, message: "No file uploaded" });
    }
    res.json({
        success: true,
        filePath: `/uploads/${req.file.filename}`
    });
});

app.use("/uploads", express.static(uploadDir)); // Serve uploaded files statically

// Serve static files from the "public" directory (unchanged)
app.use(express.static(path.join(__dirname, "public")));

io.on("connection", (socket) => {
    console.log("User connected");

    socket.on("newuser", (username) => {
        socket.broadcast.emit("update", `${username} has joined the chat.`);
    });

    socket.on("chat", (message) => {
        socket.broadcast.emit("chat", message); // Send message to all other users
    });

    socket.on("exituser", (username) => {
        socket.broadcast.emit("update", `${username} has left the chat.`);
    });
});

server.listen(3011, () => {
    console.log("Server is running on port 3011");
});