import { Request, Response} from "express";
import {User, Task} from "../models";

export const earnBoard = async(req: Request, res: Response) => {
    const user = req.body.user;
    const tasks = await Task.find({assignState: true});
    console.log(tasks);
    res.status(200).json({user: user, tasks: tasks});
};

export const executTask = async(req: Request, res: Response) => {

    const task = await Task.findOneAndUpdate({_id: req.body.taskId},{assignState: false});
    const user = await User.findOneAndUpdate({userId: req.body.user.userId},{$push: {tasks: req.body.taskId}},{new: true});
    res.status(200).send({msg:"Success!!!"});
}

export const processBalance = async(req: Request, res: Response) => {
    const task = await Task.findOne({_id: req.body.taskId});
    if(task){
        // To Do  Integration with Mira Network
        console.log(task.reward);
        const user = await User.findOneAndUpdate({userId: req.body.user.userId},{$inc: {coins: task.reward},$pull: {tasks: req.body.taskId}},{new: true});
        console.log(user);
        await Task.deleteOne({_id: task._id});
        res.status(200).send({message: "success"});
    }
    else{
        res.status(404).send({message: "No Task"});
    }
}