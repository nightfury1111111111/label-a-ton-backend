import { Router } from 'express'
import {airdopController} from "../controllers";
import {authenticate} from "../middlewares";
const airdropRouter = Router();

airdropRouter.get("/", authenticate, airdopController);
export default airdropRouter;