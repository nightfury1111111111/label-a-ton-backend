import { Router } from 'express'
import {signinController} from "../controllers";
import {signupController} from "../controllers";
import {loginValidate} from "../middlewares";
const auth = Router();

auth.post("/signin", loginValidate, signinController);
auth.post("/signup", loginValidate, signupController);
export default auth;