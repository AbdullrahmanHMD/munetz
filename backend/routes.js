import { Router } from 'express'
import { findInfoController, summarizeController } from './controllers.js';
import { upload } from './uploadConfig.js';

const router = Router()

router.post('/summarize', summarizeController(false))
router.post('/summarize/pdf', summarizeController(true))
router.post('/find-info', findInfoController)

export default router;