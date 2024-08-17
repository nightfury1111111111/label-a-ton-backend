import { Router } from 'express'
import { workForceController } from "../controllers";
const workForceRouter = Router();

workForceRouter.post("/workforce", workForceController);
export default workForceRouter;