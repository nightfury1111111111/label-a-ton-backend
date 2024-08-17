import { Request, Response} from "express";
import {User} from "../models";

export const home = async(req: Request, res: Response) => {
    const user= await User.findOne({userId: req.body.data.userId});
    res.status(200).json(user);
};