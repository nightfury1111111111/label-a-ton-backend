import {User} from "../models"
import { Request, Response} from "express"
import {generateToken} from "../utils"
import {generateRefferalCode} from "../utils"

export const signup = async(req: Request, res: Response) => {
    console.log(req.body);
    try{
        const tuser = await User.findOne({userId: req.body.userId});
        if(tuser){
            res.status(400).send({message: "Already Exists!!"});
        }
        else {
            if(req.body.refferalCode){
                const refferaluser = await User.findOne({refferalCode: req.body.refferalCode});
                if(refferaluser){
                    const user = new User({userId: req.body.userId,coins: 100, refferalCode: generateRefferalCode()});
                    await user.save();
                    await User.updateOne({_id: refferaluser._id},{$inc: {coins: 500, $push: {referrals: user._id}}});
                    console.log("Refferal User", refferaluser._id);
                }
                else{
                    console.log("Wrong Refferal User");
                }
                const user = new User({userId: req.body.userId,coins: 100, refferalCode: generateRefferalCode()});
                await user.save();
                console.log("successfully signup");
                res.status(200).send({token: generateToken(req.body.userId),user});
            }
            else{
                console.log("No Refferal User");
                const user = new User({userId: req.body.userId,coins: 100, refferalCode: generateRefferalCode()});
                await user.save();
                console.log("successfully signup");
                res.status(200).send({token: generateToken(req.body.userId),user});
            }
        }
    }
    catch(err){
        res.status(404).send(err);
    }
};