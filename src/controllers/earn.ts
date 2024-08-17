import { Request, Response} from "express";
import {User, Task} from "../models";

export const earnBoard = async(req: Request, res: Response) => {
    const user = req.body.user;
    const tasks = await Task.find({assignState: true});
    res.status(200).json({user: user, tasks: tasks});
};

export const executTask = async(req: Request, res: Response) => {
    const task = await Task.findOneAndUpdate({_id: req.body.taskId},{assginState: false});
    const user = await User.findOneAndUpdate({userId: req.body.userId},{$push: {tasks: req.body.taskId}});
}

export const addBalance = async(req: Request, res: Response) => {
    const user = await User.findOneAndUpdate({userId: req.body.userId},{$inc: {coins: req.body.reward}});
}