import { Router } from 'express'
import { simpleController } from './controllers.js';
const router = Router()

// TODO: register routes
router.post('/simple', simpleController)

export default router;