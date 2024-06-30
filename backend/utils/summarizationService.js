import { exec as execCb } from "child_process"
import { promisify } from "util"

const exec = promisify(execCb)

const summarize = async (fileName, isToPDF) => {
    return await runScript(
        "summarize_document.py",
        fileName,
        isToPDF ? "" : "--print"
    )
}

const deleteSummary = (fileName) => {
    // delete summarized file
    const path =
        "../../ai_core/python_scripts/document_summarization/summarized_docs/"
    const summarizedFileName = fileName.replace(".pdf", "_summarized.pdf")
    execCb(`rm -f ${path}/${summarizedFileName}`)
}

const deleteOriginal = (fileName) => {
    // delete original file
    const path =
        "../../ai_core/python_scripts/document_summarization/docs/"
    execCb(`rm -f ${path}/${fileName}`)
}

const runScript = async (scriptName, input, args) => {
    const scriptsDirectory =
        "../../ai_core/python_scripts/document_summarization"
    const command = `python ${scriptsDirectory}/${scriptName} ${input} ${args}`
    const { stdout, stderr } = await exec(command)
    if (stderr) {
        throw new Error(stderr)
    }
    console.log(`stdout: ${stdout}`)
    return stdout
}

export { summarize, deleteSummary, deleteOriginal }
