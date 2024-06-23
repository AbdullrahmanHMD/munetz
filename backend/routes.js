import { Router } from 'express'
import { simpleController, summarizeController } from './controllers.js';
import { upload } from './uploadConfig.js';

const router = Router()

// TODO: register routes
router.post('/simple', simpleController)
router.post('/summarize', upload.single('pdf'), summarizeController)

export default router;