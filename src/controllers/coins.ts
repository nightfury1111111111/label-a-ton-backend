import { Request, Response} from "express";
import {User} from "../models";

export const increaseCoins = async(req: Request,res: Response)=> {
    try{
        await User.findOneAndUpdate({userId: req.body.userId}, {$inc:{coins: req.body.addCoins}});
        res.status(200).send({message: "Success Increase Coin"});
    }
    catch(err){
        res.status(404).send(err);
    }
}

export const decreaseCoins = async(req: Request, res: Response)=> {
    try{
        await User.findOneAndUpdate({userId: req.body.userId}, {$inc:{coins: req.body.addCoins}});
        res.status(200).send({message: "Success Increase Coin"});
    }
    catch(err){
        res.status(404).send(err);
    }
}