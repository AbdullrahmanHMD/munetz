import dotenv from "dotenv"
import { handleZip } from "./utils/zipHandler.js"
import { getPDFs } from "./utils/scrapingService.js"
import {
    deleteOriginal,
    deleteSummary,
    extractInfo,
    summarize,
} from "./utils/processingService.js"
dotenv.config()

const getTitle = (name) => {
    const parts = name.split("-")
    parts.shift()
    return parts.join("-").replace(".pdf", "")
}

const summarizeController = (isPdfReturn) => async (req, res) => {
    const { url: pageUrl } = req.body
    if (!pageUrl) {
        return res.status(400).json({ message: "Please specify a page URL" })
    }

    let fileNames = []
    try {
        const pdfData = await getPDFs(pageUrl)
        fileNames = await handleZip(pdfData)
        const summaries = []
        for (const name of fileNames) {
            if (!name.endsWith(".pdf")) continue
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
        fileNames.forEach((name) => {
            deleteOriginal(name)
            deleteSummary(name)
        })
    }
}

const findInfoController = async (req, res) => {
    const { url: pageUrl } = req.body
    if (!pageUrl) {
        return res.status(400).json({ message: "Please specify a page URL" })
    }

    let fileNames = []
    try {
        const pdfData = await getPDFs(pageUrl)
        fileNames = await handleZip(pdfData)
        const orderedFileNames = [
            ...fileNames.filter((name) => !name.endsWith(".html")),
            fileNames.find((name) => name.endsWith(".html")),
        ]
        const fileNamesInput = orderedFileNames.map((name) => `"${name}"`).join(" ")
        console.log("input files:", fileNamesInput)
        const extractedInfo = await extractInfo(fileNamesInput)
        res.status(200).json(JSON.parse(extractedInfo))
    } catch (e) {
        console.error(e.message)
        return res.status(500).send(e)
    } finally {
        // Delete files files after returning - //TODO: rework if separate request for returning file names
        fileNames.forEach((name) => {
            deleteOriginal(name)
            deleteSummary(name)
        })
    }
}

export { summarizeController, findInfoController }
