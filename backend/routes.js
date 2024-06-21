import { Router } from 'express'
import { dummyController } from './controllers.js';
const router = Router()

// TODO: register routes
router.get('/dummy', dummyController)

export default router;