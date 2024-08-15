import { Request, Response} from "express";

export const home = (req: Request, res: Response) => {  
    res.json([{ id: 1, title: 'Sample Post', content: 'This is a sample post.' }]);  
};