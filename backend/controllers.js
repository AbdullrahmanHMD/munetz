import OpenAI from "openai"
import { exec as execCb } from "child_process"
import { promisify } from "util"
import path from "path"

import dotenv from "dotenv"
dotenv.config()

const exec = promisify(execCb)
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

const summarizeController = (isPdfReturn) => async (req, res) => {
    const pdf = req.file
    if (!pdf) {
        return res.status(400).json({ message: "No file uploaded" })
    }
    const pdfName = pdf.filename
    const runScript = async () => {
        const command = `python ../ai_core/python_scripts/document_summarization/summarize_document.py ${pdfName}${
            isPdfReturn ? "" : " --print"
        }`
        const { stdout, stderr } = await exec(command)
        if (stderr) {
            throw new Error(stderr)
        }
        console.log(`stdout: ${stdout}`)
        return stdout
    }

    try {
        const scriptResult = await runScript()

        if (isPdfReturn) {
            // Send the file
            const relativePath =
                "../ai_core/python_scripts/document_summarization/summarized_docs"
            const absolutePath = path.resolve(relativePath)
            const resultFileName = pdfName.replace(".pdf", "_summarized.pdf")
            const filePath = `${absolutePath}/${resultFileName}`
            res.sendFile(filePath, (err) => {
                if (err) {
                    console.error("File sending failed:", err)
                    res.status(500).json({
                        error: "Failed to send file - " + err.message,
                    })
                }
            })
        } else {
            res.status(200).json({ summary: scriptResult })
        }
    } catch (e) {
        console.error(e.message)
        res.status(500).json({ error: e.message })
    } finally {
        // delete uploaded file
        execCb(
            `rm -f ../ai_core/python_scripts/document_summarization/docs/${pdfName}`
        )
        // delete summarized file
        execCb(
            `rm -f ../ai_core/python_scripts/document_summarization/summarized_docs/${pdfName.replace(
                ".pdf",
                "_summarized.pdf"
            )}`
        )
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
