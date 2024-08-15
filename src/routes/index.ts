import { Router } from 'express'
import * as controller from "../controllers";
const router = Router()

router.get("/", controller.homeController);
router.post("/workforce", controller.workForceController);
export default router;