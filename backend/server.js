import express from "express"
// Setup environment
import dotenv from "dotenv"
dotenv.config()
const env = process.env
// Route imports
import routes from "./routes.js"
import cors from 'cors';
// Create Express app
const app = express()

// middleware
app.use(express.json()) // json access
app.use((req, resp, next) => {
    // logging
    console.log(req.path, req.method)
    next()
})
/*
app.use(cors({
    origin: 'http://localhost:3000'
}));

 */

const allowedOrigin = 'chrome-extension://gnihbdpfonpecgickljoadeekbkceden';

const corsOptions = {
    origin: function (origin, callback) {
        if (origin === allowedOrigin || !origin) {
            callback(null, true);
        } else {
            callback(new Error('Not allowed by CORS'));
        }
    },
    optionsSuccessStatus: 200,
    methods: 'GET,POST,OPTIONS',
    allowedHeaders: 'Content-Type'
};

app.use(cors(corsOptions));

// register routes
app.use("/api", routes)

app.use((error, _req, res, _next) => {
    // global error handling
    console.error(error)
    res.status(error.status || 500).send({ error: error.message })
})

app.listen(env.PORT, () => {
    console.log("listening on port", env.PORT)
})
