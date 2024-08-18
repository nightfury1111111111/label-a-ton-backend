import { Router } from 'express'
import { agentJobShow, assignJob,unassignJob, buyData, buyGpu } from "../controllers/workforce";
import {authenticate} from "../middlewares";
const workForceRouter = Router();

workForceRouter.get("/agentjobshow", authenticate, agentJobShow);
workForceRouter.post("/assignjob",authenticate,assignJob);
workForceRouter.post("/unassignjob",authenticate,unassignJob);
workForceRouter.post("/buygpu",authenticate,buyGpu);
workForceRouter.post("/buydata",authenticate,buyData);

export default workForceRouter;