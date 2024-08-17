// src/middleware/authenticate.ts  

import { Request, Response, NextFunction } from 'express';  
import jwt, { JwtPayload } from 'jsonwebtoken';  
import {User} from "../models";

const secretKey = process.env.JWT_SECRET || 'your-secret-key';  

export const authenticate = async (req: Request, res: Response, next: NextFunction) => {  
  try {  
    const token = req.headers.authorization?.split(' ')[1]; // "Bearer TOKEN_STRING"  
    console.log(token);
    if (!token) {  
      return res.status(401).send({ message: 'NoToken'});  
    }  

    const decoded = jwt.verify(token, secretKey) as JwtPayload;
    req.body.user = await User.findOne({userId: decoded.userId}); 

    next();  
  } catch (error) {  
    res.status(401).send({ message: 'Invalid token' });  
  }  
};