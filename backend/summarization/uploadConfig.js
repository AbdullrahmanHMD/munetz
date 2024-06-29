import multer from "multer";

const storage = multer.diskStorage({
    destination: function (_req, _file, cb) {
        cb(null, './uploads') // TODO: read from config
    },
    filename: function (_req, file, cb) {
        cb(null, "originalDoc.pdf") // TODO: read from config
    }
});

const upload = multer({ 
    storage: storage,
    fileFilter: function (req, file, cb) {
        if (file.mimetype === 'application/pdf') {
            cb(null, true);
        } else {
            cb(new Error('Only PDF files are allowed!'), false);
        }
    }
});

export { upload }