import { Router } from 'express'
import { findInfoController, simpleController, summarizeController } from './controllers.js';
import { upload } from './uploadConfig.js';

const router = Router()

// TODO: register routes
router.post('/simple', simpleController)
router.post('/summarize', upload.single('pdf'), summarizeController(false))
router.post('/summarize/pdf', upload.single('pdf'), summarizeController(true))
router.post('/find-info', upload.single('pdf'), findInfoController)

export default router;