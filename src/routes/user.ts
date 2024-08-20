import { Router } from 'express'
import {home, increaseCoins, decreaseCoins} from "../controllers";
import { authenticate } from '../middlewares';
const userRouter = Router();

userRouter.get("/", authenticate, home);
userRouter.post("/increasecoins", authenticate, increaseCoins);
userRouter.get("/decreasecoins", authenticate, decreaseCoins);
export default userRouter;