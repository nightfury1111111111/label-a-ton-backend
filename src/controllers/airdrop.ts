import { Request, Response} from "express";
import {User} from "../models";

export const airdrop = async(req: Request, res: Response) => {   
  try {  
    const userProfile = await User.find({}).select("userId").select("coins").select("friends");  
    if (userProfile) {  
      res.status(200).send(userProfile);  
    } else {  
      res.status(404).send('User not found');
    }  
  } catch (error) {  
    res.status(500).send({msg: error});
  }
};

