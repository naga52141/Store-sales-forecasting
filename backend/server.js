const express = require("express");
const multer = require("multer");
const cors = require("cors");
const { exec } = require("child_process");
const path = require("path");
const fs = require("fs");

const app = express();
const port = 4000;

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, "../frontend")));

// ✅ Correct Multer Storage Setup
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, "backend/uploads/"); // Ensure this directory exists
    },
    filename: function (req, file, cb) {
        cb(null, "upload-" + Date.now() + ".csv");
    },
});

// ✅ Set up Multer for single file uploads (consistent naming)
const upload = multer({
    storage: storage,
    limits: { fileSize: 10 * 1024 * 1024 }, // 10 MB limit
});

// ✅ Upload & Run SARIMA Model
app.post("/upload", upload.single("file"), (req, res) => { // <-- Ensure "file" matches frontend
    if (!req.file) {
        return res.status(400).json({ error: "No file uploaded" });
    }

    const filePath = req.file.path;
    console.log("Uploaded file path:", filePath);

    exec(`python3 backend/models/sarima.py "${filePath}"`, (error, stdout, stderr) => {
        if (error) {
            console.error("SARIMA Error:", stderr);
            return res.status(500).json({ error: "SARIMA model failed" });
        }

        try {
            const result = JSON.parse(stdout);
            res.json(result);
        } catch (err) {
            console.error("JSON Parse Error:", err);
            res.status(500).json({ error: "Invalid JSON from SARIMA model" });
        }

        // ✅ Delete uploaded file after processing
        fs.unlink(filePath, (err) => {
            if (err) console.error("Error deleting file:", err);
        });
    });
});

// ✅ Serve Frontend
app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, "../frontend/index.html"));
});

// ✅ Start Server
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
