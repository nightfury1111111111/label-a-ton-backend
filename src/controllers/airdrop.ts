import { Request, Response} from "express";

export const airdrop = (req: Request, res: Response) => {  
    res.json([{ id: 1, title: 'Sample Post', content: 'This is a sample post.' }]);  
};