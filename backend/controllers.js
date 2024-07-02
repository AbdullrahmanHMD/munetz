import OpenAI from "openai"
import dotenv from "dotenv"
import { handleZip } from "./utils/zipHandler.js"
import { getPDFs } from "./utils/scrapingService.js"
import {
    deleteOriginal,
    deleteSummary,
    summarize,
} from "./utils/summarizationService.js"
dotenv.config()

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY })

const simpleController = async (req, res) => {
    const { prompt } = req.body
    try {
        const completion = await openai.chat.completions.create({
            messages: [{ role: "system", content: prompt }],
            model: "gpt-3.5-turbo",
        })
        const answer = completion.choices[0].message.content
        res.status(200).json({ answer })
    } catch (e) {
        res.status(e.status || 500).json({ error: e.message })
    }
}

const getTitle = (name) => {
    const parts = name.split("-")
    parts.shift()
    return parts.join("-").replace('.pdf', '')
}

const summarizeController = (isPdfReturn) => async (req, res) => {
    const { url: pageUrl } = req.body
    if (!pageUrl) {
        return res.status(400).json({ message: "Please specify a page URL" })
    }

    var pdfNames = []
    try {
        const pdfData = await getPDFs(pageUrl)
        pdfNames = await handleZip(pdfData)
        const summaries = []
        for (const name of pdfNames) {
            const summary = await summarize(name, isPdfReturn)
            const title = getTitle(name)
            summaries.push({ title: title, content: summary })
        }
        if (isPdfReturn) {
            // TODO: handle sending PDFs (send as zip?)
        } else {
            res.status(200).json({ summaries })
        }
    } catch (e) {
        console.error(e.message)
        return res.status(500).send(e)
    } finally {
        // Delete files files after returning - //TODO: rework if separate request for returning file names
        pdfNames.forEach((name) => {
            deleteOriginal(name)
            deleteSummary(name)
        })
    }
}

const findInfoController = async (req, res) => {
    const pdf = req.file
    const prompt = req.body.prompt
    if (!pdf) {
        return res.status(400).json({ message: "No file uploaded" })
    }
    if (!prompt || !prompt.length) {
        return res.status(400).json({ message: "No prompt entered" })
    }
    const runScript = async () => {
        const command = `python ./scripts/find_info.py ${pdf.originalname} ${pdf.path} ${prompt}`
        const { stdout, stderr } = await exec(command)
        if (stderr) {
            throw new Error(stderr)
        }
        console.log(`stdout: ${stdout}`)
        return stdout
    }

    try {
        const scriptResult = await runScript()
        res.status(200).json({ result: scriptResult })
    } catch (e) {
        console.error(e.message)
        res.status(500).json({ error: e.message })
    } finally {
        execCb("rm -f ./uploads/originalDoc.pdf") // TODO: read path from config
    }
}

export { simpleController, summarizeController, findInfoController }
