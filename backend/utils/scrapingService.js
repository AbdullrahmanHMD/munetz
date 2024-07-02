import axios from "axios";

export const getPDFs = async (pageUrl) => {
    const response = await axios({
        url: 'https://lxmzr818ca.execute-api.eu-central-1.amazonaws.com/main/scraper',
        method: 'POST',
        headers: {
            'x-api-key': process.env.AWS_API_KEY,
            'Content-Type': 'application/json'
        },
        data: {
            url: pageUrl,
        },
        responseType: 'arraybuffer' // Important to handle binary data
    })

    return response.data
}