import { Request, Response} from "express";
import {User, Agent} from "../models";

export const agentsList = (req: Request, res: Response) => {
    res.status(200).send({user: req.body.user});
};

export const agentsCreate = async(req: Request, res: Response) => {
    const agent= new Agent({agentName: req.body.agentName});
    await agent.save().then();
    const user = await User.findOneAndUpdate({_id: req.body.user._id},{$push: {agents: agent._id},$inc: {passiveIncome: 1}},{new: true});
    res.status(200).send({user});
}

export const agentsPair = async(req: Request, res: Response)=>{
    try{
        const agents = req.body.agents;
        if(agents.length===2){
            const tempAgent = await Agent.findOne({_id: req.body.agents[1]});
            console.log(tempAgent);
            if(tempAgent){
                const agent = await Agent.findOneAndUpdate({_id: req.body.agents[0]},{$inc: {passiveIncome: tempAgent.passiveIncome,level: 1}},{new: true});
                const user = await User.findOneAndUpdate({userId: req.body.user.userId},{$pull: {agents: tempAgent._id}},{new: true});
                await Agent.deleteOne({_id: tempAgent._id});
                res.status(200).send(agent);
            }
            else{
                res.status(404).send({message: "Invalid Info"});
            }
        }
        else{
            res.status(404).send({message: "Invalid Info"});
        }
    }
    catch(err){
        res.status(404).send(err);
    }
}

export const agentUpgrade = async(req: Request, res: Response)=>{
    
}