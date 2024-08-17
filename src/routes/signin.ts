import { Router } from 'express'
import {signinController} from "../controllers";
import {loginValidate} from "../middlewares";
const signin = Router();

signin.post("/signin", loginValidate, signinController);
export default signin;