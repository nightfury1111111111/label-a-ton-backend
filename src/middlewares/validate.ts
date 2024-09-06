import { Request, Response, NextFunction } from 'express';
import {Agent, User, Job, Task} from "../models";


// Validation for User Login

export const loginValidate = async(req: Request, res: Response, next: NextFunction) => {
  try{
    if(req.body.userId){
      req.body.user = await User.findOne({userId: req.body.userId});
      if (req.body.user){
        next();
      }
      else{
        res.status(401).send({message: "No User"});
      }
    }
    else{
      res.status(400).send({message: "UserId must be filled"});
    }
  }
  catch(err){
    res.status(404).send(err);
  }
};

// Validation for User SignUp

export const signUpValidate = async(req: Request, res: Response, next: NextFunction) => {
  try{
    if(!req.body.userId || req.body.userId.trim()){
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

// Validation for Agent Upgrade

export const agentUpgradeValidate = async(req: Request, res: Response, next: NextFunction) => {
  try{
    const agent = await Agent.findOne({_id: req.body.aget});
    if(agent){
      if(req.body.coins && req.body.coins.type === 'number'){
        req.body.data.agentName = req.body.agentName && req.body.agentName.type === 'string' ? req.body.name : agent.agentName;
        req.body.data.level = req.body.level && req.body.level.type === 'number' ? req.body.level : agent.level;
        req.body.data.passiveIncome = req.body.passiveIncome && req.body.passiveIncome.type === 'number' ? req.body.passiveIncome : agent.passiveIncome;
        req.body.data.strength = req.body.strength && req.body.strength.type === 'number' ? req.body.strength : agent.strength;
        req.body.data.agility = req.body.agility && req.body.agility.type === 'number' ? req.body.agility : agent.agility;
        req.body.data.survivability = req.body.survivability && req.body.survivability.type === 'number' ? req.body.survivability : agent.survivability;
        req.body.data.healthPoint = req.body.healthPoint && req.body.healthPoint.type === 'number' ? req.body.healthPoint : agent.healthPoint;
        req.body.data.coins = req.body.coins;
        next();
      }
      else{
        res.status(400).send({message: "Incorrect Coins"});
      }
    }
    else{
      res.status(400).send({message: "Invalid agent"});
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

// Validation for Request Friend
export const requestFriendValidate = async(req: Request, res: Response, next: NextFunction) => {
  try{
    const tempUser = await User.findOne({_id: req.body.requestedUser});
    if(tempUser && !req.body.user.friends.includes(req.body.requestedUser) && !req.body.user.candidateFriends.includes(req.body.requestedUser)){
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

// Validation for Decline Friend
export const declineFriendValidate = async(req: Request, res: Response, next: NextFunction) => {
  try{
    const tempUser = await User.findOne({_id: req.body.requestedUser});
    if(tempUser && !req.body.user.friends.includes(req.body.requestedUser) && req.body.user.candidateFriends.includes(req.body.requestedUser)){
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

// Validation for Remove Friend

export const removeFriendValidate = async(req: Request, res: Response, next: NextFunction) => {
  try{
    const tempUser = await User.findOne({_id: req.body.requestedUser});
    if(tempUser && req.body.user.friends.includes(req.body.requestedUser) && !req.body.user.candidateFriends.includes(req.body.requestedUser)){
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
    if(req.body.coins && req.body.coins.type === 'number'){
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

export const clickValidate = (req: Request, res: Response, next: NextFunction)=> {
  try{
    if(req.body.clickCount && req.body.clickCount.type === 'number'){
      next();
    }
  }
  catch(err){
    res.status(404).send(err);
  }
}
// Missions Validate

export const missionsValidate = (req: Request, res: Response, next: NextFunction)=> {
  try{
    // To add some features
    if(req.body.coins && req.body.coins.type === 'number'){
      next();
    }
  }
  catch(err){

  }
}