import { Request, Response} from "express";
import {User} from "../models";

export const home = async(req: Request, res: Response) => {
    const user= await User.findOne({_id: req.body.user._id});
    res.status(200).json(user);
};

export const increaseCoins = async(req: Request,res: Response)=> {
    const createdAt = req.body.user.created_at;
    const currentDateTime = new Date();
    const accountAgeInDays = Math.floor((currentDateTime.getTime() - createdAt.getTime())/(1000*60*60*24));
    if(accountAgeInDays<30){
        await User.findByIdAndUpdate({_id: req.body.user.referralUser},{$inc:{referralIncome: Math.floor(req.body.coins/20)}});
    }
    // if(req.body.user.referralIncome>0){
    await User.findByIdAndUpdate({_id: req.body.user._id}, {$inc:{coins: req.body.coins + req.body.user.referralIncome}});
    res.status(200).send({message: "Success Increase Coin",referralIncome:req.body.user.referralIncome });
    // }
    // else{
    //     await User.findByIdAndUpdate({_id: req.body.user._id}, {$inc:{coins: req.body.coins}});
    //     res.status(200).send({message: "Success Increase Coin"});
    // }
}

export const decreaseCoins = async(req: Request, res: Response)=> {
    if(req.body.user.coins >= req.body.coins){
        const createdAt = req.body.user.created_at;
        const currentDateTime = new Date();
        const accountAgeInDays = Math.floor((currentDateTime.getTime() - createdAt.getTime())/(1000*60*60*24));
        if(accountAgeInDays<30){
            await User.findByIdAndUpdate({_id: req.body.user.referralUser},{$inc:{referralIncome: Math.floor(req.body.coins/20)}});
        }
        // if(req.body.user.referralIncome>0){
        await User.findByIdAndUpdate({_id: req.body.user._id}, {$inc:{coins: req.body.user.referralIncome - req.body.coins}});
        res.status(200).send({message: "Success Decrease Coin",referralIncome : req.body.user.referralIncome});
        // }
        // else{
        //     await User.findByIdAndUpdate({_id: req.body.user._id}, {$inc:{coins: - req.body.coins}});
        //     res.status(200).send({message: "Success Decrease Coin"});
        // }
    }
    else{
        res.status(400).send({message: "Not Possible"});
    }
}