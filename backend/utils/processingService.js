import { exec as execCb } from "child_process"
import { promisify } from "util"

const exec = promisify(execCb)

const summarize = async (fileName, isToPDF) => {
    let quotedFileName = `"${fileName}"`
    return await runScript(
        "document_summarization/summarize_document.py",
        quotedFileName,
        isToPDF ? "" : "--print"
    )
}

const extractInfo = async (inputFileNames) => {
    return await runScript(
        "information_extraction/extract_info.py",
        inputFileNames,
    )
}

const chatbot = async (prompt) => {
    return await runScript(
        "chatbot/chatbot.py",
        `"${prompt}"`,
    )
}

const deleteSummary = (fileName) => {
    // delete summarized file
    const path =
        "../ai_core/python_scripts/shared_docs/summarized_pdf/"
    const summarizedFileName = fileName.replace(".pdf", "_summarized.pdf")
    execCb(`rm -f ${path}/"${summarizedFileName}"`)
}

const deleteOriginal = (fileName) => {
    // delete original file
    const path =
        "../ai_core/python_scripts/shared_docs/"
    execCb(`rm -f ${path}/"${fileName}"`)
}

const runScript = async (scriptName, input, args) => {
    const scriptsDirectory =
        "../ai_core/python_scripts"
    let command = `python ${scriptsDirectory}/${scriptName} ${input}`
    if (args) {
        command += ` ${args}`
    }
    const { stdout, stderr } = await exec(command)
    if (stderr) {
        throw new Error(stderr)
    }
    return stdout
}

export { summarize, deleteSummary, deleteOriginal, extractInfo, chatbot }
