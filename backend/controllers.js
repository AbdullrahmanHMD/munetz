import OpenAI from "openai"
import dotenv from "dotenv"
dotenv.config()

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY })


const simpleController = async (req, res) => {
    const { prompt } = req.body
    try {
        const completion = await openai.chat.completions.create({
            messages: [{ role: "system", content: prompt }],
            model: "gpt-4o",
        })
        const answer = completion.choices[0].message.content
        res.status(200).json({ answer })
    } catch(e) {
        res.status(e.status || 500).json({error: e.message})
    }
}

export { simpleController }
