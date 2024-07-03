import express from "express"
// Setup environment
import dotenv from "dotenv"
dotenv.config()
const env = process.env
// Route imports
import routes from "./routes.js"

// Create Express app
const app = express()

// middleware
app.use(express.json()) // json access
app.use((req, resp, next) => {
    // logging
    console.log(req.path, req.method)
    next()
})

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
