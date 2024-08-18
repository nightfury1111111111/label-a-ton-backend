import { Router } from 'express'
import {agentsList, agentsCreate, agentsPair} from "../controllers/agents";
import {authenticate} from "../middlewares";
const agentRouter = Router();

agentRouter.get("/agentlist", authenticate, agentsList);
agentRouter.post("/agentcreate", authenticate, agentsCreate);
agentRouter.post("/agentpair", authenticate, agentsPair);

export default agentRouter;