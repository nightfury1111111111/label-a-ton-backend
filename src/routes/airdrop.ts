import { Router } from 'express'
import {leaderBoard, addFriend} from "../controllers";
import {authenticate,addFriendValidate} from "../middlewares";
const airdropRouter = Router();

airdropRouter.get("/leaderboard", authenticate, leaderBoard);
airdropRouter.post("/addfriend", authenticate, addFriendValidate, addFriend);
export default airdropRouter;