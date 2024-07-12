/**
 * User managment routes
 *
 * @since 1.0.0
 * @version 1.0.0
 */
import { Router } from "express";
import UserController from "../controllers/user";
import { checkJwt } from "../middlewares/checkJwt";
import { checkRole } from "../middlewares/checkRole";

const router = Router();
const user = new UserController();

router.get("/test", user.test);

export default router;
