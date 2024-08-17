import { Request, Response, NextFunction } from 'express';  

export const loginValidate = (req: Request, res: Response, next: NextFunction) => {

  if(!req.body.userId){
    res.status(400).send({message: "UserId must be filled"});
  }
  else{
    next();
  }
};