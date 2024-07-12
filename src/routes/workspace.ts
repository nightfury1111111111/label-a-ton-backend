/**
 * User managment routes
 *
 * @since 1.0.0
 * @version 1.0.0
 */
import { Router } from "express";
import WorkspaceController from "../controllers/workspace";
import { checkJwt } from "../middlewares/checkJwt";
import { checkRole } from "../middlewares/checkRole";

const router = Router();
const workspace = new WorkspaceController();

router.get("/test", workspace.test);

export default router;
