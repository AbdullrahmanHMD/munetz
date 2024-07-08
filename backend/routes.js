import { Router } from 'express'
import { findInfoController, summarizeController } from './controllers.js';
import { upload } from './uploadConfig.js';

const router = Router()

router.post('/summarize', summarizeController(false))
router.post('/summarize/pdf', summarizeController(true))
router.post('/find-info', upload.single('pdf'), findInfoController)

export default router;