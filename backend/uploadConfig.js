import multer from "multer";

const storage = multer.diskStorage({
    destination: function (_req, _file, cb) {
        cb(null, '../ai_core/python_scripts/document_summarization/docs') // TODO: read from config
    },
    filename: function (_req, file, cb) {
        cb(null, `${Date.now().toString()}-${file.originalname}`) // TODO: read from config
    }
});

const upload = multer({ 
    storage: storage,
    fileFilter: function (_req, file, cb) {
        if (file.mimetype === 'application/pdf') {
            cb(null, true);
        } else {
            cb(new Error('Only PDF files are allowed!'), false);
        }
    }
});

export { upload }