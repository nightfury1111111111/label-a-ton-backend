import { Router } from 'express'
import {agentsController} from "../controllers";
const agentRouter = Router();

agentRouter.post("/agents", agentsController);
export default agentRouter;