import {User} from "../models"
import { Request, Response} from "express"
import {generateToken} from "../utils"
import {generateRefferalCode} from "../utils"

export const signin = async(req: Request, res: Response) => {
    try{
        const user = await User.findOne({userId: req.body.userId});
        if(!user){
            res.status(404).send({message: "No User"});
        }
        else {
            res.status(200).send({token: generateToken(user.userId),user});           
        }
    }
    catch(err){
        res.status(404).send(err)
    }
};

export const signup = async(req: Request, res: Response) => {
    try{
        const referralUser = await User.findOne({refferalCode: req.body.refferalCode});
        if(req.body.refferalCode && referralUser){
            const user = new User({userId: req.body.userId,coins: 100, refferalCode: generateRefferalCode(), referrals: referralUser._id});
            await user.save();
            await User.updateOne({_id: referralUser._id},{$inc: {coins: 500}});
            console.log("User Who referraled", referralUser._id);
            res.status(200).send({token: generateToken(req.body.userId)});
        }
        else{
            console.log("Common Case");
            const user = new User({userId: req.body.userId,coins: 100, refferalCode: generateRefferalCode()});
            await user.save();
            res.status(200).send({token: generateToken(req.body.userId)});
        }
    }
    catch(err){
        res.status(404).send(err);
    }
};