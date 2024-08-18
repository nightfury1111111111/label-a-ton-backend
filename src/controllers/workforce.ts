import { Request, Response} from "express";
import {User, Job, Agent} from "../models";

export const agentJobShow = async(req: Request, res: Response) => {
    const user = await User.findOne({userId: req.body.user.userId});
    
    if(!user){
        res.status(404).send({message: "No User"});
    }
    else {
        const job = await Job.find({assignState: true});
        res.status(200).send({user,job});
    }
};

export const assignJob = async(req: Request, res: Response)=>{
    const job = await Job.findOne({_id: req.body.jobId});
    if(job){
        const agent = await Agent.findOne({_id: req.body.agentId});
        if(agent){
            if(agent.level >= job.requiredLevel && agent.assignState == true){
                await Agent.findOneAndUpdate({_id: req.body.agentId},{jobId: job._id,assignState: false, $inc:{passiveIncome: job.passiveIncome}},{new: true});
                const user = await User.findOneAndUpdate({userId: req.body.user.userId},{$inc:{passiveIncome: job.passiveIncome,power: -req.body.requiredPower}},{new: true});
                res.status(200).send(user);
            }
            else{
                res.status(400).send({message: "Not Possible"});
            }
        }
        else{
            res.status(400).send({message: "Agent Not Exists"});
        }
    }
    else{
        res.status(404).send({message:"Job Not Exists"});
    }
}

export const unassignJob = async(req: Request, res: Response)=>{
    const job = await Job.findOne({_id: req.body.jobId});
    if(job){
        const agent = await Agent.findOne({_id: req.body.agentId});
        if(agent){
            if(agent.level >= job.requiredLevel && agent.assignState == false){
                await Agent.findOneAndUpdate({_id: req.body.agentId},{jobId: job._id,assignState: true, $inc:{passiveIncome: -job.passiveIncome}},{new: true});
                const user = await User.findOneAndUpdate({userId: req.body.user.userId},{$inc:{passiveIncome: -job.passiveIncome}},{new: true});
                res.status(200).send(user);
            }
            else {
                res.status(400).send({message: "Not Possible"});
            }
        }
        else{
            res.status(400).send({message: "Agent Not Exists"});
        }
    }
    else{
        res.status(404).send({message:"Job Not Exists"});
    }
}

export const buyGpu = async(req: Request, res: Response)=>{
    const user= await User.findOneAndUpdate({userId: req.body.user.userId},{$inc: {gpus: req.body.addGpu,coins: -1000*req.body.addGpu}},{new: true});
    res.status(200).send(user);
}

export const buyData = async(req: Request, res: Response)=>{
    const user= await User.findOneAndUpdate({userId: req.body.user.userId},{$inc: {datas: req.body.addData,coins: -800*req.body.addData}},{new: true});
    res.status(200).send(user);
}