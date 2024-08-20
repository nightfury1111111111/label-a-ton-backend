import { Request, Response} from "express";
import {User} from "../models";
import {generateLootBox} from "../utils";

export const leaderBoard = async(req: Request, res: Response) => {   
  try {  
    const userProfile = await User.find({}).select("_id").select("userId").select("coins").select("friends");  
    res.status(200).send({userProfile});  
  } catch (err) {  
    res.status(404).send(err);
  }
};

export const addFriend = async(req: Request, res: Response) => {
  try{
    await User.findByIdAndUpdate({_id: req.body.user._id},{$push:{friends: req.body.requestedUser},$pull: {candidateFriends: req.body.requestedUser}});
    if(req.body.user.friends.length()%10 === 9){
      const lootBox = generateLootBox(req.body.user.friends.length()%10);
      res.status(200).send({message: "Success",lootBox});
    }
    res.status(200).send({message: "Success"});
  }
  catch (err){
    res.status(404).send(err);
  }
}
