// src/utils/generateToken.ts  

import jwt from 'jsonwebtoken';  

const secretKey = process.env.JWT_SECRET || 'your-secret-key'; // Keep your secret key safe and use environment variables  

export const generateToken = (userId: string) => {  
  const token = jwt.sign({ userId }, secretKey, { expiresIn: '12h' }); // Expires in 12 hour  
  return token;  
};