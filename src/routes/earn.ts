import { Router } from 'express'
import {earnBoard,executTask,processBalance} from "../controllers/earn";
import {authenticate} from "../middlewares";
const earnRouter = Router();

earnRouter.get("/earnboard", authenticate, earnBoard);
earnRouter.post("/executetask",authenticate, executTask);
earnRouter.post("/processbalance",authenticate,processBalance);
export default earnRouter;