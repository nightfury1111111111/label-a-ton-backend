import { Request, Response} from "express";
import {User, Task} from "../models";

export const earnBoard = async(req: Request, res: Response) => {
    const tasks = await Task.find({assignState: true});
    res.status(200).send(tasks);
};

export const executeTask = async(req: Request, res: Response) => {
    if(req.body.task.assignState && !req.body.user.tasks.includes(req.body.taskId)){
        await Task.findByIdAndUpdate({_id: req.body.taskId},{assignState: false});
        await User.findByIdAndUpdate({_id: req.body.user._id},{$push: {tasks: req.body.taskId}});
        res.status(200).send({message:"Success"});
    }
    else{
        res.status(400).send({message: "Not Possible"});
    }
}

export const processBalance = async(req: Request, res: Response) => {
    if(!req.body.task.assignState && req.body.user.tasks.includes(req.body.taskId)){

        // To Do Integration with Mira Network and Process the feedback

        await User.findByIdAndUpdate({_id: req.body.user._id},{$inc: {coins: req.body.task.reward},$pull: {tasks: req.body.taskId}});
        await Task.deleteOne({_id: req.body.task._id});
        res.status(200).send({message: "Success"});
    }
    else{
        res.status(400).send({message: "Not Possible"});
    }
}