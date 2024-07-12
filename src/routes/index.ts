/**
 * Route mananger
 *
 * @since 1.0.0
 * @version 1.0.0
 */

import { Router } from "express";
import github from "./github";
import user from "./user";
import workspace from "./workspace";

const routes = Router();

routes.use("/github", github);
routes.use("/user", user);
routes.use("/workspace", workspace);

export default routes;
