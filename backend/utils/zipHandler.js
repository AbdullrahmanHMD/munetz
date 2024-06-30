import fs from "fs"
import JSZip from "jszip"
import path from "path"

const handleZip = async (data) => {
    const zip = new JSZip()
    const zipContents = await zip.loadAsync(data)

    const fileNames = []
    // Loop through each file in the zip
    for (const [filename, fileData] of Object.entries(zipContents.files)) {
        if (!fileData.dir) {
            // Skip directories
            // Read the content of the file
            const fileContent = await fileData.async("nodebuffer")

            // Define path to save the file
            const filePath = path.join(
                "../../ai_core/python_scripts/document_summarization/docs",
                filename
            )

            // Save the file
            fs.writeFileSync(filePath, fileContent)

            fileNames.push(filename)
        }
    }
    
    return fileNames
}

export { handleZip }
