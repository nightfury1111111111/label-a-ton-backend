import { Request, Response, NextFunction } from 'express';
import {Agent, User, Job, Task} from "../models"; 

// Validation for User Login

export const loginValidate = (req: Request, res: Response, next: NextFunction) => {
  try{
    if(! req.body.userId.trim()){
      res.status(400).send({message: "UserId must be filled"});
    }
    else{
      next();
    }
  }
  catch(err){
    res.status(404).send(err);
  }
};

// Validation for User SignUp

export const signUpValidate = async(req: Request, res: Response, next: NextFunction) => {
  try{
    if(! req.body.userId.trim()){
      res.status(400).send({message: "UserId must be filled"});
    }
    else{
      const tempUser = await User.findOne({userId: req.body.userId});
      if(tempUser){
        res.status(400).send({message: "Already Exists!!"});
      }
      else {
        next();
      }
    }
  }
  catch(err){
    res.status(404).send(err);
  }
  
};

// Validation for Agents Create

export const agentCreateValidate = (req: Request, res: Response, next: NextFunction)=>{
  try{
    if(req.body.user.agents.length < 20){
      next();
    }
    else {
      res.status(404).send({message: "Not Possible"});
    }
  }
  catch(err){
    res.status(404).send(err);
  }
}

// Validation for Agents Pair

export const agentPairValidate = async(req: Request, res: Response, next: NextFunction) => {
  try{
    const agents = req.body.agents;
    console.log(agents);
    if(agents && agents.length===2){
      console.log(1);
      try{
        const tempAgent1 = await Agent.findOne({_id: req.body.agents[1]});
        const tempAgent2 = await Agent.findOne({_id: req.body.agents[1]});
        if(tempAgent1 && tempAgent2 && tempAgent1.level === tempAgent2.level){
          req.body.tempAgent = tempAgent2;
          next();
        }
        else{
          res.status(400).send({message: "Invalid Info"});
        }
      }
      catch(err){
        res.status(404).send(err);
      }
    }
    else{
      console.log(2);
      res.status(400).send({message: "Invalid Info"});
    }
  }
  catch(err){
    res.status(404).send(err);
  }
};

// Validation for Add Friend

export const addFriendValidate = async(req: Request, res: Response, next: NextFunction) => {
  try{
    const tempUser = await User.findOne({_id: req.body.requestedUser});
    if(tempUser && req.body.user.candidateFriends.includes(req.body.requestedUser) &&!req.body.user.friends.includes(req.body.requestedUser)){
      next();
    }
    else{
      res.status(404).send({message: "Invalid Info"});
    }
  }
  catch(err){
    res.status(200).send(err);
  }
}

export const removeFriendValidate = async(req: Request, res: Response, next: NextFunction) => {
  try{
    const tempUser = await User.findOne({_id: req.body.requestedUser});
    if(tempUser && req.body.user.friends.includes(req.body.requestedUser)){
      next();
    }
    else{
      res.status(404).send({message: "Invalid Info"});
    }
  }
  catch(err){
    res.status(200).send(err);
  }
}

// Validation for Agents Pairing

export const jobValidate = async(req: Request, res: Response, next: NextFunction) => {
  try{
    const job = await Job.findOne({_id: req.body.jobId});
    if(job){
      req.body.job = job;
      next();
    }
    else{
      res.status(400).send({message: "Not available"});
    }
  }
  catch(err){
    res.status(404).send(err);
  }
  
}

export const agentValidate = async(req: Request, res: Response, next: NextFunction) => {
  try{
    const agent = await Agent.findOne({_id: req.body.agentId});
    if(agent){
      req.body.agent = agent;
      next();
    }
    else{
      res.status(400).send({message: "Not available"});
    }
  }
  catch(err){
    res.status(400).send(err);
  }
}

export const taskValidate = async(req: Request, res: Response, next: NextFunction) => {
  try{
    const task = await Task.findOne({_id: req.body.taskId});
    if(task){
      req.body.task = task;
      next();
    }
    else{
      res.status(400).send({message: "No Task"});
    }
  }
  catch(err){
    res.status(404).send(err);
  }
}

// Validation for coin Process

export const coinValidate = (req: Request, res: Response, next: NextFunction)=> {
  try{
    if(req.body.coins){
      next();
    }
    else{
      res.status(400).send({message: "Invalid Info"});
    }
  }
  catch(err){
    res.status(404).send(err);
  }
}