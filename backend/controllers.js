const dummyController = (_req, res) => {
    res.status(200).json({ message: "dummy request received" })
}


export { dummyController }