import { Router } from 'express'
import {earnBoard,executeTask,processBalance} from "../controllers";
import {authenticate} from "../middlewares";
const earnRouter = Router();

earnRouter.get("/earnboard", authenticate, earnBoard);
earnRouter.post("/executetask",authenticate, executeTask);
earnRouter.post("/processbalance",authenticate,processBalance);
export default earnRouter;