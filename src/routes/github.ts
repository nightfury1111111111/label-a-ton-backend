/**
 * User managment routes
 *
 * @since 1.0.0
 * @version 1.0.0
 */
import { Router } from "express";
import GithubController from "../controllers/github";
import { checkJwt } from "../middlewares/checkJwt";
import { checkRole } from "../middlewares/checkRole";

const router = Router();
const github = new GithubController();

router.get("/test", github.test);

export default router;
