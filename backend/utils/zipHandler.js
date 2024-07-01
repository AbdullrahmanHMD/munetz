import fs from "fs"
import { exec as execCb } from "child_process"
import { promisify } from "util"

const exec = promisify(execCb)

const handleZip = async (data) => {
    fs.writeFileSync("scripts/zipBinaryContent.txt", data)
    console.log("File saved successfully.")
    const script = "scripts/zipExtractor.py"
    const command = `python ${script}`
    const { stdout, stderr } = await exec(command)
    if (stderr) {
        throw new Error(stderr)
    }

    fs.unlink("scripts/zipBinaryContent.txt", (err) => {
        if (err) {
            console.warn("Failed deleting zip content file", err)
        } else {
            console.log("Zip content file deleted successfully")
        }
    })

    const fileNames = stdout
        .split(",")
        .map((name) => name.trim())
        .filter((name) => name.length > 0)
    return fileNames
}

export { handleZip }
