import mongoose, { Schema } from 'mongoose';
import {generateRefferalCode} from "../utils";
const userSchema = new Schema({
        userId: { type: String, required: true },
        avatar: { type: String, default: ""},  
        coins: { type: Number, default: 0 },  
        power: { type: Number, default: 1000 },  
        data: { type: Number, default: 0 },  
        gpus: { type: Number, default: 0 },  
        levels: { type: Number, default: 0 },
        passiveIncome: {type: Number, default: 0},
        referralIncome: {type: Number, default: 0},
        agents: [
            {  
                type: mongoose.Schema.Types.ObjectId,
                ref: 'Agent' // Update this to your Agent schema reference  
            }  
        ],  
        referralUser: {type: mongoose.Schema.Types.ObjectId, ref: 'User'} // User who referraled
        ,
        tasks: [
            {  
                type: mongoose.Schema.Types.ObjectId,  
                ref: 'Task'  
            }
        ],
        friends: [
            {  
                type: mongoose.Schema.Types.ObjectId,  
                ref: 'User'  
            }
        ],
        candidateFriends:[
            {  
                type: mongoose.Schema.Types.ObjectId,  
                ref: 'User'  
            } 
        ],
        refferalCode: { type: String, required: true, default: generateRefferalCode() }
    },
    {  
        timestamps: { createdAt: 'created_at', updatedAt: 'updated_at' }
  }
);  

const User = mongoose.model('User', userSchema);  

export default User;