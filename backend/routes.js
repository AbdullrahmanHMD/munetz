import { Router } from 'express'
import { chatbotController, findInfoController, summarizeController } from './controllers.js';
import { upload } from './uploadConfig.js';

const router = Router()

router.post('/summarize', summarizeController(false))
router.post('/summarize/pdf', summarizeController(true))
router.post('/find-info', findInfoController)
router.post('/chatbot', chatbotController)

export default router;