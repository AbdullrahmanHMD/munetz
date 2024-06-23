import OpenAI from "openai"
import { exec as execCb } from 'child_process';
import { promisify } from 'util';

import dotenv from "dotenv"
dotenv.config()

const exec = promisify(execCb);
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
    } catch(e) {
        res.status(e.status || 500).json({error: e.message})
    }
}

const summarizeController = async (req, res) => {
    const pdf = req.file
    const prompt = req.body.prompt || ""
    if (!pdf) {
        return res.status(400).json({message: 'No file uploaded'});
    }
    const runScript = async () => {
        const command = `python ./scripts/my_script.py ${pdf.originalname} ${pdf.path} ${prompt}`;
        const { stdout, stderr } = await exec(command);
            if (stderr) {
                throw new Error(stderr)
            }
            console.log(`stdout: ${stdout}`);
            return stdout;
    }

    try {
        const scriptResult = await runScript()
        res.status(200).json({result: scriptResult})
    } catch (e) {
        console.error(e.message)
        res.status(500).json({error: e.message})
    } finally {
        execCb('rm -f ./uploads/originalDoc.pdf') // TODO: read path from config
    }

}

export { simpleController, summarizeController }
