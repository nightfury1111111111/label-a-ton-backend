import {User} from "../models"
import { Request, Response} from "express"
import {generateToken} from "../middlewares"

export const signin = async(req: Request, res: Response) => {
    console.log(req.body)
    let user = await User.findOne({userId: req.body.userId});
    if(!user){
        const user = new User({userId: req.body.userId});
        await user.save();
        console.log("successfully signup");
        res.status(200).send({token: generateToken(req.body.userId),user});
    }
    else {
        res.status(200).send({user});
    }
    
};