import { Router } from 'express'
import {earnBoard} from "../controllers/earn";
import {authenticate} from "../middlewares";
const earnRouter = Router();

earnRouter.get("/earnboard", authenticate, earnBoard);
export default earnRouter;