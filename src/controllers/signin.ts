import {User} from "../models"
import { Request, Response} from "express"
import {generateToken} from "../utils"

export const signin = async(req: Request, res: Response) => {
    console.log(req.body)
    const user = await User.findOne({userId: req.body.userId});
    if(!user){
        res.status(202).send({message: "No User"});
    }
    else {
        res.status(200).send({token: generateToken(req.body.userId),user});
    }
};