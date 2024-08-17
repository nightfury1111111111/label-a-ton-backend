import { Router } from 'express'
import {homeController} from "../controllers";
import { authenticate } from '../middlewares';
const homeRouter = Router();

homeRouter.get("/", authenticate, homeController);
export default homeRouter;